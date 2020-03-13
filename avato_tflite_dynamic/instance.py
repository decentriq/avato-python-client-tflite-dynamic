from enum import IntEnum
import re
import numpy as np
from avato import Instance
from .proto.tflite_dynamic_pb2 import (
    UploadModelRequest,
    GetModelFormatRequest,
    InferenceRequest,
    TfliteResponse,
    TfliteRequest,
)


class TFLITEDYNAMIC_Instance(Instance):
    @classmethod
    def get_type(cls):
        return "TFLITE_DYNAMIC"

    @Instance._secret_required
    @Instance._valid_fatquote_required
    def upload_model(self, model):
        request = TfliteRequest()
        request.uploadModel.model = model
        response = self._send_and_parse_message(request)
        if not response.HasField("uploadModel"):
            raise Exception(
                "Expected uploadModel response, got "
                + response.WhichOneof("tflite_response")
            )

    @Instance._secret_required
    @Instance._valid_fatquote_required
    def get_model_format(self):
        request = TfliteRequest()
        request.getModelFormat.SetInParent()
        response = self._send_and_parse_message(request)
        if not response.HasField("getModelFormat"):
            raise Exception(
                "Expected getModelFormat response, got "
                + response.WhichOneof("tflite_response")
            )
        return response.getModelFormat.modelFormat

    @Instance._secret_required
    @Instance._valid_fatquote_required
    # TODO: add docstring
    def predict(self, x):
        if isinstance(x, np.ndarray):
            x = x.tolist()

        model_format = self.get_model_format()

        assert (
            len(model_format.inputTensorFormats) == 1
        ), "Only a single Input Tensor allowed."
        input_format = model_format.inputTensorFormats[0]
        assert input_format.valueType == "float32le", "Only float32 is supported."

        assert (
            len(model_format.outputTensorFormats) == 1
        ), "Only a single Ouput Tensor allowed."
        output_format = model_format.outputTensorFormats[0]
        assert output_format.valueType == "float32le", "Only float32 is supported."

        x_bytes = _serialize_tensors(x, input_format)
        predicion_bytes = self._request_inference(x_bytes)
        prediction = _deserialize_tensors(predicion_bytes, output_format)

        return np.array(prediction)

    @Instance._secret_required
    @Instance._valid_fatquote_required
    def _request_inference(self, inference_inputs):
        request = TfliteRequest()
        request.inference.input = inference_inputs
        response = self._send_and_parse_message(request)
        if not response.HasField("inference"):
            raise Exception(
                "Expected inference response, got "
                + response.WhichOneof("tflite_response")
            )
        return response.inference.output

    def _send_and_parse_message(self, message):
        response = self._send_message(message)
        tflite_response = TfliteResponse()
        tflite_response.ParseFromString(bytes(response))
        if tflite_response.HasField("failure"):
             raise Exception(tflite_response.failure)
        return tflite_response


# TODO:
#  should at some point be part of a "RemoteModel" class


def _serialize_tensors(data, tensor_format):
    assert len(data) == 1, "No batching support. Use a single sample."

    #  TODO: use regex here to also have support for other value types
    # type_search = re.search("([a-z]+)([0-9]+)([a-z]+)", tesor_format.valueType)
    # currently hard-coded to `float32le` - which is mostly used.
    dt = np.dtype("f4")  # 32-bit floating-point number
    dt = dt.newbyteorder("<")  # little-endianness

    data_np = np.array(data)
    data_np_byteorderd = data_np.astype(dt, order="C")  #  use C-style alignment
    bytes_array = data_np_byteorderd.tobytes()
    assert len(bytes_array) == tensor_format.size
    return bytes_array


def _deserialize_tensors(data, tensor_format):
    dt = np.dtype("f4")  # 32-bit floating-point number
    dt = dt.newbyteorder("<")  # little-endianness

    result = np.frombuffer(data, dtype=dt).reshape(tensor_format.dimensions)
    return result

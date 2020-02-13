import os
import numpy as np
from avato import Client
from avato import Secret
from avato_tflite_dynamic import TFLITEDYNAMIC_Instance

tests_root = os.path.dirname(__file__)
fixtures_dir = os.path.join(tests_root, "fixtures")

with open(os.path.join(fixtures_dir, "cifar10-dataset-small.bin"), "rb") as f:
    dataset = f.read()

with open(os.path.join(fixtures_dir, "cifar10-model.fb"), "rb") as f:
    model = f.read()

inference_requestor = Client(username=os.environ["TEST_USER_ID"], password=os.environ["TEST_USER_PASSWORD"], instance_types=[TFLITEDYNAMIC_Instance])
inference_requestor_secret = Secret()


def test_tflite_dynamic_complete():
    # inference requestor creates instance and includes model provider
    inference_requestor_instance = inference_requestor.create_instance(
        "Tensorflow Lite Dynamic", TFLITEDYNAMIC_Instance.type, [inference_requestor.user.email]
    )
    assert inference_requestor_instance.id in inference_requestor.get_instances()

    # inference requestor validates fatquote and get enclave pubkey
    inference_requestor_instance.validate_fatquote(
        accept_debug=True, accept_group_out_of_date=True
    )
    inference_requestor_instance.set_secret(inference_requestor_secret)

    # Upload model
    inference_requestor_instance.upload_model(model)

    # Get the model format
    model_format = inference_requestor_instance.get_model_format()
    print(model_format)
    assert len(model_format.inputTensorFormats) == 1
    input_format = model_format.inputTensorFormats[0]
    print(input_format.size)

    # Request inferences
    offset = 0
    while offset < len(dataset):
        dt = np.dtype("f4")  # 32-bit floating-point number
        dt = dt.newbyteorder("<")  # little-endianness
        data = np.frombuffer(dataset[offset : offset + input_format.size], dtype=dt).reshape(input_format.dimensions)
        result = inference_requestor_instance.predict(
            data
        )
        print(result)
        offset += input_format.size

    # cleanup
    inference_requestor_instance.delete()
    assert inference_requestor_instance.id not in inference_requestor.get_instances()

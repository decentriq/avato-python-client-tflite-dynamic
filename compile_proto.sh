#!/bin/bash

for proto_file in proto/*.proto; do
    protoc -I=proto --python_out=avato_tflite_dynamic/proto $proto_file
done

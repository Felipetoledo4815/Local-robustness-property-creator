#!/usr/bin/bash

mkdir -p experiments

for tool in "neurify" "verinet"; do
    for degree in 15 45; do
        mkdir -p experiments/$degree
        mkdir -p experiments/$degree/verifiers/
        python dnnv_pipeline.py \
            onnx/dave_small.onnx \
            generated_properties \
            experiments/$degree/verifiers/$tool/ \
            1800 \
            $degree \
            $tool
    done
done
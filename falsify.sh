#!/usr/bin/bash

mkdir -p experiments

for tool in "BIM" "PGD"; do
    for degree in 15 45; do
        mkdir -p experiments/$degree
        mkdir -p experiments/$degree/falsifiers
        python dnnf_pipeline.py \
            onnx/dave_small.onnx \
            generated_properties \
            experiments/$degree/falsifiers/$tool/ \
            1800 \
            $degree \
            $tool
    done
done
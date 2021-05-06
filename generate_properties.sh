#!/usr/bin/bash

mkdir -p generated_properties
for ((i = 0 ; i < 10 ; i++)); do
    python pipeline.py --img original_images/img$i.jpg --output generated_properties --name $i
done
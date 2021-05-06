#!/usr/bin/bash

### Local
# cd /Data/PhD/Frameworks/DNNV/
# . .env.d/openenv.sh
# cd /Data/PhD/2nd\ Semester/CPS/final_project/robustness_properties_pipeline/

### Remote
cd /bigtemp/ft8bn/DNNV/
. .env.d/openenv.sh
cd /bigtemp/ft8bn/pipeline/

timeout=${1:-3600}

for ((i = 0; i < 5; i++)); do
    sbatch --job-name=Falsifiers --wrap="python experiment/resmonitor.py -T ${timeout} dnnf generated_properties/property${i}.py --network N onnx/dave_small.onnx --backend cleverhans.ProjectedGradientDescent --save-violation counter_examples/img_ce${i}_test.npy >> experiment/logs/log_PGD.out 2>> experiment/logs/log_PGD.err"
done
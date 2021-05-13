# Assisted Generation of Meaningful Robustness Properties for Adversarial Attacks and Verification

## Pipeline
### <span>pipeline.py</span>
Receives 3 arguments:
- `--img` Image that is going to be used for generating the property
- `--output` Output directory where everything is going to be saved
- `--name` Name of the property. Needed to save the generated files

### <span>generate_properties.sh</span>
Shell script to iterate over all images in a folder and automatize the execution of `pipeline.py` for more than one image.

## Experiment
For this project, we did an experiment consisting in creating 10 properties with 10 images of the [DAVE](https://github.com/udacity/self-driving-car) test dataset. After creating the properties, we used [DNNV](https://github.com/dlshriver/DNNV) to run `Neurify` and `Verinet`, and [DNNF](https://github.com/dlshriver/DNNF) to run `Basic Iterative Method (BIM)` and `Projected Gradient Descent (PGD)`. For each tool we selected 2 different steering angles, `15` and `45` degrees. In order to reproduce the study, you will need to follow these steps:
1. Execute `install.sh` script in order to install DNNV, DNNF and other python packages needed.
2. The script above will create a python environment that will need to be active to carry out the experiments. To activate it, move to `DNNV` folder that will be created and execute `.env.d/openenv.sh`.
3. To run the experiment with the verifiers (`Neurify` and `Verinet`), execute `verify.sh`.
4. To run the experiment with the falsifiers (`Basic Iterative Method (BIM)` and `Projected Gradient Descent (PGD)`), execute `falsify.sh`.
5. After executing the experiments scripts mentioned above, a `experiment` folder will be created, inside of it, you will find two folders `15` and `45` representing the two different alpha values that we used for the experiments. Inside those folders there will be two more folders `falsifiers` and `verifiers` which will contain folders for the tools used. Lastly inside the tools folder, you will see a file called `result_summary.md` which contains the result of each property and an image of the counter-example in case the property was violated.
6. To create the plots from our paper, you will need to open the `results.ipynb` notebook and run all the cells.

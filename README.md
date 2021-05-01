# Assisted Generation of Meaningful Robustness Properties for Adversarial Attacks and Verification

## <span>pipeline.py</span>
Receives 3 arguments:
- `--img` Image that is going to be used for generating the property
- `--output` Output directory where everything is going to be saved
- `--name` Name of the property. Needed to save the generated files

## <span>generate_properties.sh</span>
Shell script to iterate over all images in a folder and automatize the execution of `pipeline.py`
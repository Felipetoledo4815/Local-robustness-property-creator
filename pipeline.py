import argparse
import os

import mousepoints
import property_creator

parser = argparse.ArgumentParser(description='Robustness Properties for Images from Dave Data Set')

parser.add_argument('--img', type=str, help='location of the image file', required=True)
parser.add_argument('--output', type=str, help='output directory', required=True)
parser.add_argument('--name', type=str, help='name of the property', required=True)

args = parser.parse_args()

if args.output[-1] != '/':
    args.output = args.output + '/'

if not os.path.exists(args.img):
    raise AssertionError("The image does not exist")
if not os.path.exists(args.output):
    raise AssertionError("The output folder does not exist")

mousepoints.main(args)
property_creator.main(args)
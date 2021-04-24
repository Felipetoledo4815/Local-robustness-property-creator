import argparse


parser = argparse.ArgumentParser(description='Robustness Properties for Images from Dave Data Set')

parser.add_argument('--img', type=str, help='location of the image file')

parser.add_argument('--o', type=str, help='output directory')

args = parser.parse_args()
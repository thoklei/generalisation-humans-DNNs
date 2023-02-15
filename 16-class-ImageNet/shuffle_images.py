"""
The image-names in the directory image_names are not shuffled, but ordered class-by-class.
This script duplicates the folder, but shuffles the .txt files so that image-names are in truly random order, all drawn from different classes.
We can then, to generate experiment i, take the 80 images from that class as imgs[i*80:(i+1)*80], then shuffle their order.
"""

import os
import re
import sys
import json
from argparse import ArgumentParser

import numpy as np

def main(args):
    """ Read files, shuffle them, write to new location. """

    # abort if target location exists
    os.makedirs(args.target_location, exist_ok=False)

    _root, _dirs, files = next(os.walk(args.source_location))

    for file in files:
        source_name = os.path.join(args.source_location, file)
        target_name = os.path.join(args.target_location, file)

        with open(source_name, "r") as f:
            lines = f.readlines()

        np.random.shuffle(lines)

        with open(target_name, "w") as f:
            for line in lines:
                f.write(line)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--target_location", "-t", type=str, default="shuffled_image_names")
    arguments = parser.parse_args()

    arguments.source_location = "image_names"

    main(arguments)

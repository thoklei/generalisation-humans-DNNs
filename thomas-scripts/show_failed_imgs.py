"""
This script takes a csv-file and extracts all images on which the subject failed, plotting them with the actual label and subject's response.
"""

import os
import re
import sys
import json
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision

from download_imgs import get_imagenet_img


def get_wrong_images(df):
    """ Gets a list of tuples (response, label, img) of wrong responses. """
    wrong_df = df[df['object_response'] != df['category']]
    return [(line['object_response'], line['category'], line['imagename']) for _, line in wrong_df.iterrows()]


def get_img(location, img):
    loc = os.path.join(location, img)
    img = Image.open(loc)
    return img


def download_wrong_images(imgs, location, imagenet_path):
    """ Walks over list of images, extracts normal name and downloads it to location. """

    os.makedirs(location, exist_ok=True)

    for img in imgs:
        name = img[img.rfind('n'):]
        image = get_imagenet_img(name, imagenet_path)
        image.save(os.path.join(location, img))


def main(args):

    # read CSV
    df = pd.read_csv(args.file)

    # get list of wrong images
    wrongs = get_wrong_images(df)

    # download all images where subjects gave wrong responses
    download_wrong_images([img for _, _, img in wrongs], args.img_location, args.imagenet_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="The csv file to be analyzed.")
    parser.add_argument("--img_location", type=str, required=True, help="Path to directory with images.")
    parser.add_argument("--imagenet_path", type=str, default="/imagenet/train/")

    args = parser.parse_args()

    main(args)

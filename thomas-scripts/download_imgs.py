"""
To generate the actual stimuli for the experiment, the ImageNet images need to be downloaded, processed and renamed to their proper names.
"""

import os
import json
from argparse import ArgumentParser

from tqdm import tqdm
from torchvision.transforms import Compose, Resize, CenterCrop
from PIL import Image

# using the same transforms we would use when passing this to a model?
img_transforms = Compose([
    Resize(256),
    CenterCrop(224)
])


def get_imagenet_img(img_name, imagenet_path):
    """ Loads an image with name img_name from imagenet dataset. """
    directory = img_name.split("_")[0]
    img = Image.open(os.path.join(imagenet_path, directory, img_name))
    img = img_transforms(img) # TODO figure out if images should be transformed
    return img


def main(args):
    """ Reads from the config which images should be loaded, then loads them all and renames them properly. """

    os.makedirs(args.target_location, exist_ok=False)

    with open(args.config, "r", encoding="utf-8") as config_file:
        experiment = json.load(config_file)

    for trial in tqdm(experiment['trials']):

        img_in = trial['image_name']
        img_out = os.path.join(args.target_location, trial['full_image_name'])

        img = get_imagenet_img(img_in, args.imagenet_path)

        img.save(img_out)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--imagenet_path", type=str, default="/imagenet/train/")
    parser.add_argument("--config", type=str, required=True, help="Path to config file that defines the experiment.")
    parser.add_argument("--target_location", type=str, required=True, help="Path to directory where images should be stored.")
    arguments = parser.parse_args()

    main(arguments)

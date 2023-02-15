"""
Writes the json file that completely defines one experiment.
"""

import os
import json
from argparse import ArgumentParser

import numpy as np

VERSION = 1.0

def get_img_name(trial_idx, subject, category, seed, img_name):
    """ Generates the new image name according to Robert's specification. """
    return f"{trial_idx:04d}_cl_s{subject:01d}_cr_{category}_{seed}_{img_name}"


def main(args):
    """ Generates one experiment-json as desired by the CLI-args. """

    # make sure that at target location, there is no file we overwrite
    os.makedirs(args.target_location, exist_ok=True)

    exp_name = f"exp_{args.experiment_id}_subject_{args.subject_id}.json"
    exp_name = os.path.join(args.target_location, exp_name)
    assert not os.path.exists(exp_name), f"ERROR: file {exp_name} exists already, won't overwrite!"

    exp = {}
    exp["version"] = VERSION
    exp["subject_id"] = args.subject_id
    exp["experiment_id"] = args.experiment_id
    exp["random_seed"] = args.seed
    exp["num_trials_per_class"] = args.n_images

    trials = []
    _root, _dirs, files = next(os.walk(args.image_name_path))

    # append trials for each class
    for file in files:

        # extract category name from filename, removing .txt
        category = file[:-4]

        with open(os.path.join(args.image_name_path, file), "r", encoding="utf-8") as class_file:
            names = class_file.readlines()

        # select the appropriate n_images images
        names = names[args.experiment_id * args.n_images : (args.experiment_id + 1) * args.n_images]

        for name in names:
            trial = {}
            trial['image_name'] = str.strip(name)
            trial['category'] = category

            trials.append(trial)

    # trials are now un-numbered and not shuffled, so let's do that
    np.random.shuffle(trials)
    for idx, trial in enumerate(trials):
        trial['trial_id'] = idx + 1 # Robert seems to have started his trial count at 1
        trial['full_image_name'] = get_img_name(idx, args.subject_id, trial['category'], args.seed, trial['image_name'])

    # add trials to experiment, then write to json
    exp["trials"] = trials
    exp["num_total_trials"] = len(trials)
    with open(exp_name, "w", encoding="utf-8") as outfile:
        json.dump(exp, outfile)

    print(f"Dumped experiment-json to {exp_name}")
    print("DONE")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--subject_id", "-sid", type=int, required=True)
    parser.add_argument("--experiment_id", "-eid", type=int, required=True)
    parser.add_argument("--n_images", type=int, default=80, help="How many images should be shown from each class.")
    parser.add_argument("--image_name_path", type=str, default="../16-class-ImageNet/shuffled_image_names/")
    parser.add_argument("--target_location", type=str, default="basic_experiment")
    arguments = parser.parse_args()

    np.random.seed(arguments.seed)

    main(arguments)

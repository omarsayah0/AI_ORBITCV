import os
import random
import numpy as np
import pandas as pd
import torch
import yaml


def load_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def create_dirs(config):
    os.makedirs(config["paths"]["model_dir"], exist_ok=True)


def create_checkpoint_dir(config):
    os.makedirs(config["paths"]["checkpoint_dir"], exist_ok=True)


def prepare_dataframe(csv_path):
    df = pd.read_csv(csv_path)

    image_class = df["Image_Label"].str.rsplit("_", n=1, expand=True)

    df["image"] = image_class[0]
    df["class"] = image_class[1]

    return df
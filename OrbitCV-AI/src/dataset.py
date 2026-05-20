import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
from src.rle import rle_decode

class CloudDataset(Dataset):
    def __init__(self, df, data_dir, image_size, classes, transform=None):
        self.df = df
        self.data_dir = data_dir
        self.image_size = image_size
        self.classes = classes
        self.transform = transform

        self.image_ids = self.df['image'].unique()

    def __len__(self):
        return (len(self.image_ids))
    
    def __getitem__(self, inx):
        image_id = self.image_ids[inx]
        image_path = os.path.join(self.data_dir, image_id)

        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"did not read the image: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        h, w = image.shape[:2]

        mask = np.zeros((h, w, len(self.classes)), dtype=np.float32)

        rows = self.df[self.df['image'] == image_id]

        for i, value in enumerate(self.classes):
            class_rows = rows[rows["class"] == value]
            if len(class_rows) == 0:
                rle = np.nan
            else:
                rle = class_rows["EncodedPixels"].values[0]

            mask[:, :, i] = rle_decode(rle, (h, w))

        image = cv2.resize(image, (self.image_size, self.image_size))
        mask = cv2.resize(mask, (self.image_size, self.image_size), interpolation=cv2.INTER_NEAREST)

        if self.transform:
            aug = self.transform(image=image, mask=mask)
            image = aug['image']
            mask = aug['mask']
        
        image = torch.tensor(image)
        image = image.permute(2, 0, 1)
        image = image.float()
        image = image / 255.0

        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        image = (image - mean) / std
        
        mask = torch.tensor(mask)
        mask = mask.permute(2, 0, 1)
        mask = mask.float()

        return image, mask
        

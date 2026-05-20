import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import albumentations as A
from src.dataset import CloudDataset
from src.model import build_model
from src.utils import prepare_dataframe, seed_everything, create_dirs


def dice_loss(outputs, masks, smooth=1.0):
    outputs = torch.sigmoid(outputs)

    intersection = (outputs * masks).sum(dim=(0, 2, 3))

    union = outputs.sum(dim=(0, 2, 3)) + masks.sum(dim=(0, 2, 3))

    dice = (2.0 * intersection + smooth) / (union + smooth)

    return 1.0 - dice.mean()

def calculate_loss(seg_outputs, cls_outputs, masks):
    bce_seg = nn.BCEWithLogitsLoss()(seg_outputs, masks)
    seg_loss = bce_seg + dice_loss(seg_outputs, masks)

    cls_targets = (masks.sum(dim=(2, 3)) > 0).float()
    cls_loss = nn.BCEWithLogitsLoss()(cls_outputs, cls_targets)

    return seg_loss + 0.5 * cls_loss

def train_one_epoch(model, loader, optimizer, device):
    model.train()
    total_loss = 0.0

    for images, masks in loader:
        images = images.to(device)
        masks = masks.to(device)

        optimizer.zero_grad()
        seg_outputs, cls_outputs = model(images)
        loss = calculate_loss(seg_outputs, cls_outputs, masks)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / max(len(loader), 1)

def validate_one_epoch(model, loader, device, classes, threshold=0.5):
    model.eval()
    total_loss = 0.0
    num_classes = len(classes)
    dice_per_class = np.zeros(num_classes)
    cls_correct = np.zeros(num_classes)
    cls_total = 0
    n_batches = 0

    with torch.no_grad():
        for images, masks in loader:
            images = images.to(device)
            masks = masks.to(device)
            seg_outputs, cls_outputs = model(images)
            loss = calculate_loss(seg_outputs, cls_outputs, masks)
            total_loss += loss.item()

            seg_probs = torch.sigmoid(seg_outputs)
            cls_probs = torch.sigmoid(cls_outputs)

            cls_gate = (cls_probs > threshold).float().unsqueeze(-1).unsqueeze(-1)
            preds = (seg_probs * cls_gate > threshold).float()
            intersection = (preds * masks).sum(dim=(0, 2, 3)).cpu().numpy()
            union = (preds.sum(dim=(0, 2, 3)) + masks.sum(dim=(0, 2, 3))).cpu().numpy()
            dice_per_class += (2.0 * intersection) / (union + 1e-6)

            cls_targets = (masks.sum(dim=(2, 3)) > 0).float()
            cls_preds = (cls_probs > threshold).float()
            cls_correct += (cls_preds == cls_targets).float().sum(dim=0).cpu().numpy()
            cls_total += images.shape[0]
            n_batches += 1

    return (
        total_loss / max(n_batches, 1),
        dice_per_class / max(n_batches, 1),
        cls_correct / max(cls_total, 1),
    )


def tune_thresholds(model, val_loader, device, classes):
    model.eval()
    thresholds = np.arange(0.3, 0.71, 0.05)
    num_classes = len(classes)
    intersections = np.zeros((len(thresholds), num_classes))
    unions = np.zeros((len(thresholds), num_classes))

    with torch.no_grad():
        for images, masks in val_loader:
            images = images.to(device)
            masks = masks.to(device)
            seg_outputs, cls_outputs = model(images)
            seg_probs = torch.sigmoid(seg_outputs)
            cls_probs = torch.sigmoid(cls_outputs)
            for ti, t in enumerate(thresholds):
                cls_gate = (cls_probs > t).float().unsqueeze(-1).unsqueeze(-1)
                preds = (seg_probs * cls_gate > t).float()
                inter = (preds * masks).sum(dim=(0, 2, 3)).cpu().numpy()
                union = (preds.sum(dim=(0, 2, 3)) + masks.sum(dim=(0, 2, 3))).cpu().numpy()
                intersections[ti] += inter
                unions[ti] += union

    best_thresholds = {}
    print("\nPer-class threshold tuning:", flush=True)
    for ci, cls in enumerate(classes):
        dice_scores = (2.0 * intersections[:, ci]) / (unions[:, ci] + 1e-6)
        best_ti = int(np.argmax(dice_scores))
        best_thresholds[cls] = float(thresholds[best_ti])
        print(f"  {cls}: best threshold = {thresholds[best_ti]:.2f}, dice = {dice_scores[best_ti]:.4f}", flush=True)

    return best_thresholds

def safe_torch_load(path, map_location=None):

    try:
        checkpoint = torch.load(
            path,
            map_location=map_location,
            weights_only=False
        )

    except TypeError:
        checkpoint = torch.load(
            path,
            map_location=map_location
        )

    # fix DataParallel keys
    if "model_state" in checkpoint:

        new_state_dict = {}

        for k, v in checkpoint["model_state"].items():

            if k.startswith("module."):
                k = k[len("module."):]

            new_state_dict[k] = v

        checkpoint["model_state"] = new_state_dict

    return checkpoint

def run_training(config):
    seed_everything(config["data"]["seed"])
    create_dirs(config)
    print("Starting training setup...", flush=True)

    if torch.cuda.is_available():
        device_name = "cuda"
    else:
        device_name = "cpu"

    device = torch.device(device_name)
    print(f"Using device: {device_name}", flush=True)

    df = prepare_dataframe(config["paths"]["data_csv"])
    print("Data loaded.", flush=True)

    image_ids = df["image"].unique()

    train_val_ids, test_ids = train_test_split(
        image_ids,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["seed"]
    )

    train_ids, val_ids = train_test_split(
        train_val_ids,
        test_size=config["data"]["val_size"],
        random_state=config["data"]["seed"]
    )

    train_df = df[df["image"].isin(train_ids)]
    val_df = df[df["image"].isin(val_ids)]
    test_df = df[df["image"].isin(test_ids)]

    train_transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.Rotate(limit=20, p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.Affine(translate_percent=0.05, scale=(0.9, 1.1), rotate=(-15, 15), p=0.5),
        A.ElasticTransform(p=0.3),
        A.GridDistortion(p=0.3),
        A.CoarseDropout(num_holes_range=(1, 8), hole_height_range=(8, 32), hole_width_range=(8, 32), p=0.3),
    ])

    val_transform = None
    test_transform = None

    train_dataset = CloudDataset(
        df=train_df,
        data_dir=config["paths"]["data_dir"],
        image_size=config["data"]["image_size"],
        classes=config["data"]["classes"],
        transform=train_transform
    )

    val_dataset = CloudDataset(
        df=val_df,
        data_dir=config["paths"]["data_dir"],
        image_size=config["data"]["image_size"],
        classes=config["data"]["classes"],
        transform=val_transform
    )

    test_dataset = CloudDataset(
        df=test_df,
        data_dir=config["paths"]["data_dir"],
        image_size=config["data"]["image_size"],
        classes=config["data"]["classes"],
        transform=test_transform
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=True,
        num_workers=config["data"]["num_workers"],
        pin_memory=torch.cuda.is_available()
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=False,
        num_workers=config["data"]["num_workers"],
        pin_memory=torch.cuda.is_available()
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=False,
        num_workers=config["data"]["num_workers"],
        pin_memory=torch.cuda.is_available()
    )

    print("Building model...", flush=True)
    model = build_model(config)
    model.to(device)
    print("Model ready.", flush=True)

    checkpoint_path = config["paths"]["checkpoint_path"]
    freeze_epochs = config["train"].get("freeze_epochs", 5)

    start_epoch = 0
    best_loss = float("inf")

    if os.path.exists(checkpoint_path):
        checkpoint = safe_torch_load(checkpoint_path, map_location=device)
        model.load_state_dict(checkpoint["model_state"])
        start_epoch = checkpoint["epoch"] + 1
        best_loss = checkpoint["best_loss"]
        print(f"Resuming from epoch {start_epoch}", flush=True)

    def make_phase1_optimizer():
        for param in model.encoder.parameters():
            param.requires_grad = False
        trainable = [p for p in model.parameters() if p.requires_grad]
        return torch.optim.Adam(
            trainable,
            lr=config["train"]["learning_rate"],
            weight_decay=config["train"]["weight_decay"]
        )

    def make_phase2_optimizer():
        for param in model.parameters():
            param.requires_grad = True
        return torch.optim.Adam([
            {"params": model.encoder.parameters(), "lr": 1e-4},
            {"params": model.decoder.parameters(), "lr": 1e-3},
            {"params": model.segmentation_head.parameters(), "lr": 1e-3},
            {"params": model.classifier.parameters(), "lr": 1e-3},
        ], weight_decay=config["train"]["weight_decay"])

    if start_epoch < freeze_epochs:
        print("Phase 1: encoder frozen, training decoder only.", flush=True)
        optimizer = make_phase1_optimizer()
    else:
        print("Phase 2: all layers unfrozen (resuming past freeze point).", flush=True)
        optimizer = make_phase2_optimizer()

    if os.path.exists(checkpoint_path):
        checkpoint = safe_torch_load(checkpoint_path, map_location=device)
        try:
            optimizer.load_state_dict(checkpoint["optimizer_state"])
        except Exception:
            print("Optimizer state mismatch (phase changed), starting fresh optimizer.", flush=True)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=2
    )

    if os.path.exists(checkpoint_path) and "scheduler_state" in checkpoint:
        try:
            scheduler.load_state_dict(checkpoint["scheduler_state"])
        except Exception:
            pass

    total_epochs = config["train"]["epochs"]
    print(f"Starting training for {total_epochs} epochs...", flush=True)
    
    early_stop_counter = 0

    for epoch in range(start_epoch, total_epochs):

        if epoch == freeze_epochs:
            print("Phase 2: unfreezing all layers for fine-tuning...", flush=True)
            optimizer = make_phase2_optimizer()
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer,
                mode="min",
                factor=0.5,
                patience=2
            )


        print(f"\nEpoch {epoch + 1}/{total_epochs}", flush=True)
        train_loss = train_one_epoch(model, train_loader, optimizer, device)
        val_loss, val_dice, val_cls_acc = validate_one_epoch(
            model, val_loader, device, config["data"]["classes"]
        )
        scheduler.step(val_loss)
        print(f"  Train Loss: {train_loss:.4f}", flush=True)
        print(f"  Val Loss:   {val_loss:.4f}", flush=True)
        for cls, d, acc in zip(config["data"]["classes"], val_dice, val_cls_acc):
            print(f"  {cls}: Dice={d:.4f}  ClsAcc={acc:.4f}", flush=True)

        current_lr = optimizer.param_groups[0]["lr"]
        if val_loss < best_loss:
            best_loss = val_loss
            early_stop_counter = 0

            torch.save(
                model.state_dict(),
                config["paths"]["best_model_path"]
            )

        else:
            if current_lr < 1e-5:
                early_stop_counter += 1

        if early_stop_counter >= 5:
            print("Early stopping triggered.", flush=True)
            break

        if (epoch + 1) % config["train"]["checkpoint_every"] == 0:
            torch.save({
                "epoch": epoch,
                "model_state": model.state_dict(),
                "optimizer_state": optimizer.state_dict(),
                "scheduler_state": scheduler.state_dict(),
                "best_loss": best_loss
            }, checkpoint_path)

    best_ckpt = safe_torch_load(config["paths"]["best_model_path"], map_location=device)
    if isinstance(best_ckpt, dict) and "model_state" in best_ckpt:
        model.load_state_dict(best_ckpt["model_state"])
    else:
        model.load_state_dict(best_ckpt)

    best_thresholds = tune_thresholds(model, val_loader, device, config["data"]["classes"])

    test_loss, test_dice, test_cls_acc = validate_one_epoch(
        model, test_loader, device, config["data"]["classes"]
    )
    print(f"\nTest Loss:      {test_loss:.4f}", flush=True)
    print(f"Mean Test Dice: {test_dice.mean():.4f}", flush=True)
    print("Per-class results:", flush=True)
    for cls, d, acc in zip(config["data"]["classes"], test_dice, test_cls_acc):
        print(f"  {cls}: Dice={d:.4f}  ClsAcc={acc:.4f}", flush=True)
    print(f"Best thresholds: {best_thresholds}", flush=True)
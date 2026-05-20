import torch
import numpy as np
import matplotlib.pyplot as plt

from src.model import build_model
from src.postprocess import postprocess_masks


def load_trained_model(config, device):
    model = build_model(config)
    model.load_state_dict(torch.load(config["paths"]["best_model_path"], map_location=device))
    model.to(device)
    model.eval()
    return model


def predict_mask(model, image, device):
    """TTA (4 flips) returning (seg_probs, cls_probs)."""
    model.eval()
    seg_preds = []
    cls_preds = []
    flip_dims = [[], [-1], [-2], [-1, -2]]

    with torch.no_grad():
        for dims in flip_dims:
            inp = image.clone()
            if dims:
                inp = torch.flip(inp, dims=dims)
            inp = inp.unsqueeze(0).to(device)
            seg_out, cls_out = model(inp)
            seg_out = torch.sigmoid(seg_out).squeeze(0)
            cls_out = torch.sigmoid(cls_out).squeeze(0)
            if dims:
                seg_out = torch.flip(seg_out, dims=dims)
            seg_preds.append(seg_out.cpu())
            cls_preds.append(cls_out.cpu())

    seg_probs = torch.stack(seg_preds).mean(dim=0).numpy()  # (C, H, W)
    cls_probs = torch.stack(cls_preds).mean(dim=0).numpy()  # (C,)
    return seg_probs, cls_probs


def show_prediction(image, true_mask, seg_probs, cls_probs, classes, seg_threshold, cls_threshold=0.5):
    image_np = image.permute(1, 2, 0).cpu().numpy()
    true_mask_np = true_mask.cpu().numpy()

    cls_gate = (cls_probs > cls_threshold)
    pred_mask = np.zeros_like(seg_probs)
    for i in range(len(classes)):
        if cls_gate[i]:
            pred_mask[i] = (seg_probs[i] > seg_threshold).astype(float)

    plt.figure(figsize=(16, 8))
    plt.subplot(2, len(classes) + 1, 1)
    plt.imshow(image_np)
    plt.title("Image")
    plt.axis("off")

    for i, cls in enumerate(classes):
        status = f"({'present' if cls_gate[i] else 'absent'} {cls_probs[i]:.2f})"
        plt.subplot(2, len(classes) + 1, i + 2)
        plt.imshow(pred_mask[i], cmap="gray")
        plt.title(f"Pred: {cls}\n{status}")
        plt.axis("off")

        plt.subplot(2, len(classes) + 1, len(classes) + 2 + i)
        plt.imshow(true_mask_np[i], cmap="gray")
        plt.title(f"GT: {cls}")
        plt.axis("off")

    plt.tight_layout()
    plt.show()

    print("Classification results:", flush=True)
    for cls, prob, present in zip(classes, cls_probs, cls_gate):
        print(f"  {cls}: {'PRESENT' if present else 'absent'} (confidence: {prob:.3f})", flush=True)


def run_inference(config, dataset, index=0):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_trained_model(config, device)

    image, true_mask = dataset[index]
    seg_probs, cls_probs = predict_mask(model, image, device)

    seg_threshold = config["post_processing"]["threshold"]
    seg_probs = postprocess_masks(
        seg_probs,
        threshold=seg_threshold,
        min_area=config["post_processing"]["min_area"],
        kernel_size=config["post_processing"]["kernel_size"],
    )

    show_prediction(
        image=image,
        true_mask=true_mask,
        seg_probs=seg_probs,
        cls_probs=cls_probs,
        classes=config["data"]["classes"],
        seg_threshold=0.5,
    )

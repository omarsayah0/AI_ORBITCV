import os
import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    multilabel_confusion_matrix,
)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.utils import load_config, prepare_dataframe, seed_everything
from src.dataset import CloudDataset
from src.model import build_model
from src.train import safe_torch_load


# ── constants ─────────────────────────────────────────────────────────────────
NUM_EXAMPLES = 5
MASK_ALPHA   = 0.45

CLASS_RGB = [
    [1.00, 0.27, 0.27],   # Fish    – red
    [0.18, 0.80, 0.44],   # Flower  – green
    [0.20, 0.55, 1.00],   # Gravel  – blue
    [1.00, 0.82, 0.18],   # Sugar   – yellow
]
BAR_COLORS = ["#e74c3c", "#2ecc71", "#3498db", "#f1c40f"]


# ── image helpers ─────────────────────────────────────────────────────────────
def denormalize(tensor):
    """Undo ImageNet normalisation; return H×W×3 numpy in [0, 1]."""
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std  = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    return (tensor.cpu() * std + mean).clamp(0, 1).permute(1, 2, 0).numpy()


def overlay_masks(image_np, masks_np):
    """Blend per-class coloured masks over image.  masks_np: (C, H, W)."""
    result = image_np.copy()
    for c, color in enumerate(CLASS_RGB):
        if c >= masks_np.shape[0]:
            break
        binary = masks_np[c] > 0.5
        if not binary.any():
            continue
        solid = np.zeros_like(result)
        for ch, v in enumerate(color):
            solid[:, :, ch] = v
        result = np.where(
            binary[:, :, np.newaxis],
            result * (1 - MASK_ALPHA) + solid * MASK_ALPHA,
            result,
        )
    return result


# ── data ──────────────────────────────────────────────────────────────────────
def build_test_split(config):
    """Reproduce the exact test split used during training."""
    seed_everything(config["data"]["seed"])
    df  = prepare_dataframe(config["paths"]["data_csv"])
    ids = df["image"].unique()

    _, test_ids = train_test_split(
        ids,
        test_size=config["data"]["test_size"],
        random_state=config["data"]["seed"],
    )

    test_df = df[df["image"].isin(test_ids)]
    dataset = CloudDataset(
        df=test_df,
        data_dir=config["paths"]["data_dir"],
        image_size=config["data"]["image_size"],
        classes=config["data"]["classes"],
        transform=None,
    )
    loader = DataLoader(
        dataset,
        batch_size=config["train"]["batch_size"],
        shuffle=False,
        num_workers=config["data"]["num_workers"],
        pin_memory=torch.cuda.is_available(),
    )
    return dataset, loader


# ── model ─────────────────────────────────────────────────────────────────────
def load_model(config, device):
    model = build_model(config)
    model.to(device)

    path = config["paths"]["final_model"]

    ckpt  = safe_torch_load(path, map_location=device)
    # final_model.pth is a raw state dict (no wrapper dict)
    state = ckpt["model_state"] if isinstance(ckpt, dict) and "model_state" in ckpt else ckpt
    model.load_state_dict(state)
    print(f"[INFO] Model loaded from: {path}")
    model.eval()
    return model


# ── evaluation loop ───────────────────────────────────────────────────────────
def evaluate(model, loader, device, classes, threshold):
    n = len(classes)
    seg_int   = np.zeros(n)
    dice_den  = np.zeros(n)
    iou_int   = np.zeros(n)
    iou_union = np.zeros(n)
    cls_true_list, cls_pred_list = [], []

    print(f"[INFO] Evaluating on {len(loader)} batches …")
    with torch.no_grad():
        for step, (images, masks) in enumerate(loader):
            print(f"\r  batch {step + 1:>4}/{len(loader)}", end="", flush=True)
            images = images.to(device)
            masks  = masks.to(device)

            mask_logits, class_logits = model(images)
            seg_probs = torch.sigmoid(mask_logits)
            cls_probs = torch.sigmoid(class_logits)

            gate      = (cls_probs > threshold).float().unsqueeze(-1).unsqueeze(-1)
            seg_preds = (seg_probs * gate > threshold).float()

            inter    = (seg_preds * masks).sum(dim=(0, 2, 3)).cpu().numpy()
            pred_sum = seg_preds.sum(dim=(0, 2, 3)).cpu().numpy()
            true_sum = masks.sum(dim=(0, 2, 3)).cpu().numpy()

            seg_int   += inter
            dice_den  += pred_sum + true_sum
            iou_int   += inter
            iou_union += pred_sum + true_sum - inter

            cls_targets = (masks.sum(dim=(2, 3)) > 0).float().cpu().numpy()
            cls_preds   = (cls_probs > threshold).float().cpu().numpy()
            cls_true_list.append(cls_targets)
            cls_pred_list.append(cls_preds)

    print()
    cls_true = np.vstack(cls_true_list)
    cls_pred = np.vstack(cls_pred_list)

    dice_pc = (2.0 * seg_int) / (dice_den  + 1e-6)
    iou_pc  = iou_int         / (iou_union + 1e-6)
    acc_pc  = (cls_pred == cls_true).mean(axis=0)

    return dict(
        dice_pc   = dice_pc,
        mean_dice = float(dice_pc.mean()),
        iou_pc    = iou_pc,
        mean_iou  = float(iou_pc.mean()),
        acc_pc    = acc_pc,
        mean_acc  = float(acc_pc.mean()),
        prec_pc   = precision_score(cls_true, cls_pred, average=None, zero_division=0),
        rec_pc    = recall_score   (cls_true, cls_pred, average=None, zero_division=0),
        f1_pc     = f1_score       (cls_true, cls_pred, average=None, zero_division=0),
        mean_f1   = float(f1_score(cls_true, cls_pred, average="macro", zero_division=0)),
        conf_mat  = multilabel_confusion_matrix(cls_true, cls_pred.astype(int)),
    )


# ── console summary ───────────────────────────────────────────────────────────
def print_metrics(metrics, classes):
    w = max(len(c) for c in classes)
    print("\n" + "=" * 55)
    print("  SEGMENTATION METRICS")
    print("=" * 55)
    print(f"  {'Class':<{w}}  {'Dice':>7}  {'IoU':>7}")
    print("  " + "-" * (w + 18))
    for cls, d, iou in zip(classes, metrics["dice_pc"], metrics["iou_pc"]):
        print(f"  {cls:<{w}}  {d:>7.4f}  {iou:>7.4f}")
    print("  " + "-" * (w + 18))
    print(f"  {'Mean':<{w}}  {metrics['mean_dice']:>7.4f}  {metrics['mean_iou']:>7.4f}")

    print("\n" + "=" * 55)
    print("  CLASSIFICATION METRICS")
    print("=" * 55)
    print(f"  {'Class':<{w}}  {'Acc':>6}  {'Prec':>6}  {'Rec':>6}  {'F1':>6}")
    print("  " + "-" * (w + 28))
    for cls, a, p, r, f in zip(classes,
                                metrics["acc_pc"], metrics["prec_pc"],
                                metrics["rec_pc"], metrics["f1_pc"]):
        print(f"  {cls:<{w}}  {a:>6.4f}  {p:>6.4f}  {r:>6.4f}  {f:>6.4f}")
    print("  " + "-" * (w + 28))
    print(f"  {'Mean':<{w}}  {metrics['mean_acc']:>6.4f}  {'—':>6}  {'—':>6}  {metrics['mean_f1']:>6.4f}")
    print("=" * 55 + "\n")


# ── plot helpers ──────────────────────────────────────────────────────────────
def _styled_bar(ax, values, labels, title, mean_val=None):
    bars = ax.bar(labels, values, color=BAR_COLORS[: len(labels)],
                  width=0.55, edgecolor="white", linewidth=0.7)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.012,
                f"{val:.3f}", ha="center", va="bottom", fontsize=9, color="white")
    suffix = f"  (mean = {mean_val:.3f})" if mean_val is not None else ""
    ax.set_title(title + suffix, fontsize=11, fontweight="bold", color="white", pad=8)
    ax.set_ylim(0, 1.18)
    ax.set_ylabel("Score", color="white")
    ax.tick_params(colors="white")
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color("#444466")
    ax.set_facecolor("#12122a")


def _draw_label_panel(ax, classes, present, true_labels=None):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ys = np.linspace(8.0, 2.0, len(classes))
    for i, (cls, is_present) in enumerate(zip(classes, present)):
        if true_labels is not None:
            correct = bool(is_present) == bool(true_labels[i])
            dot_c   = "#2ecc71" if correct else "#e74c3c"
        else:
            dot_c = "#2ecc71" if is_present else "#666677"

        ax.add_patch(plt.Circle((1.2, ys[i]), 0.4, color=dot_c, zorder=3))
        label_c = "white" if is_present else "#888899"
        ax.text(2.2, ys[i],
                f"{cls}  –  {'Present' if is_present else 'Absent'}",
                va="center", ha="left", fontsize=10, color=label_c,
                fontweight="bold" if is_present else "normal")


# ── figures ───────────────────────────────────────────────────────────────────
def fig_seg_metrics(metrics, classes):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor="#0d0d1a")
    fig.suptitle("Segmentation Metrics", fontsize=14, fontweight="bold", color="white")
    _styled_bar(axes[0], metrics["dice_pc"], classes, "Dice Score per Class", metrics["mean_dice"])
    _styled_bar(axes[1], metrics["iou_pc"],  classes, "IoU per Class",        metrics["mean_iou"])
    plt.tight_layout()


def fig_cls_metrics(metrics, classes):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0d0d1a")
    fig.suptitle("Classification Metrics", fontsize=14, fontweight="bold", color="white")

    x = np.arange(len(classes))
    w = 0.35

    def _grouped(ax, a_vals, b_vals, a_label, b_label, a_color, b_color, title):
        bars_a = ax.bar(x - w / 2, a_vals, w, label=a_label,
                        color=a_color, edgecolor="white", linewidth=0.7)
        bars_b = ax.bar(x + w / 2, b_vals, w, label=b_label,
                        color=b_color, edgecolor="white", linewidth=0.7)
        for bar, val in zip(bars_a, a_vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=8, color="white")
        for bar, val in zip(bars_b, b_vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=8, color="white")
        ax.set_xticks(x)
        ax.set_xticklabels(classes, color="white")
        ax.tick_params(colors="white")
        ax.set_ylim(0, 1.18)
        ax.set_title(title, fontsize=11, fontweight="bold", color="white", pad=8)
        ax.set_ylabel("Score", color="white")
        ax.legend(framealpha=0.3, labelcolor="white", facecolor="#1a1a30")
        ax.spines[["top", "right"]].set_visible(False)
        for spine in ax.spines.values():
            spine.set_color("#444466")
        ax.set_facecolor("#12122a")

    _grouped(axes[0], metrics["acc_pc"], metrics["f1_pc"],
             "Accuracy", "F1 Score", "#3498db", "#e67e22",
             "Accuracy & F1 per Class")
    _grouped(axes[1], metrics["prec_pc"], metrics["rec_pc"],
             "Precision", "Recall", "#9b59b6", "#1abc9c",
             "Precision & Recall per Class")
    plt.tight_layout()


def fig_confusion_matrix(metrics, classes):
    n   = len(classes)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4.5), facecolor="#0d0d1a")
    fig.suptitle("Multilabel Confusion Matrix (per class)",
                 fontsize=13, fontweight="bold", color="white", y=1.01)

    for i, (cls, cm) in enumerate(zip(classes, metrics["conf_mat"])):
        ax = axes[i]
        ax.set_facecolor("#12122a")
        ax.imshow(cm, cmap="Blues", vmin=0)
        ax.set_title(cls, fontsize=11, fontweight="bold", color="white")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Pred: No", "Pred: Yes"], color="white", fontsize=9)
        ax.set_yticklabels(["True: No", "True: Yes"], color="white", fontsize=9)
        thresh = cm.max() / 2.0
        for row in range(2):
            for col in range(2):
                ax.text(col, row, str(cm[row, col]),
                        ha="center", va="center", fontsize=13,
                        color="white" if cm[row, col] > thresh else "#111122")
    plt.tight_layout()


def fig_summary(metrics, classes):
    fig, ax = plt.subplots(figsize=(11, 5.5), facecolor="#0d0d1a")
    ax.set_facecolor("#0d0d1a")
    ax.axis("off")
    fig.suptitle("Test Evaluation Summary", fontsize=15,
                 fontweight="bold", color="white", y=0.97)

    col_labels = ["Metric"] + list(classes) + ["Mean"]
    rows = [
        ["Dice Score"] + [f"{v:.3f}" for v in metrics["dice_pc"]] + [f"{metrics['mean_dice']:.3f}"],
        ["IoU"]        + [f"{v:.3f}" for v in metrics["iou_pc"]]  + [f"{metrics['mean_iou']:.3f}"],
        ["Accuracy"]   + [f"{v:.3f}" for v in metrics["acc_pc"]]  + [f"{metrics['mean_acc']:.3f}"],
        ["Precision"]  + [f"{v:.3f}" for v in metrics["prec_pc"]] + ["—"],
        ["Recall"]     + [f"{v:.3f}" for v in metrics["rec_pc"]]  + ["—"],
        ["F1 Score"]   + [f"{v:.3f}" for v in metrics["f1_pc"]]   + [f"{metrics['mean_f1']:.3f}"],
    ]

    table = ax.table(cellText=rows, colLabels=col_labels,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.25, 2.2)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#333366")
        if r == 0:
            cell.set_facecolor("#252550")
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#1a1a3e" if r % 2 == 0 else "#0f0f2e")
            cell.set_text_props(color="#cce0ff")
    plt.tight_layout()


# ── visual examples ───────────────────────────────────────────────────────────
def show_visual_examples(model, dataset, device, classes, threshold):
    indices = np.linspace(0, len(dataset) - 1, NUM_EXAMPLES, dtype=int)
    legend_patches = [
        mpatches.Patch(color=CLASS_RGB[i], label=classes[i])
        for i in range(len(classes))
    ]

    for fig_num, ds_idx in enumerate(indices):
        image_t, mask_t = dataset[int(ds_idx)]

        with torch.no_grad():
            inp               = image_t.unsqueeze(0).to(device)
            mask_logits, class_logits = model(inp)
            seg_probs         = torch.sigmoid(mask_logits)
            cls_probs         = torch.sigmoid(class_logits)
            gate              = (cls_probs > threshold).float().unsqueeze(-1).unsqueeze(-1)
            seg_preds         = (seg_probs * gate > threshold).float()

        image_np     = denormalize(image_t)
        true_mask_np = mask_t.numpy()
        pred_mask_np = seg_preds.squeeze(0).cpu().numpy()

        true_labels  = (mask_t.sum(dim=(1, 2)) > 0).numpy().astype(bool)
        pred_labels  = (cls_probs.squeeze(0).cpu() > threshold).numpy().astype(bool)

        all_match = np.array_equal(true_labels, pred_labels)
        accent_c  = "#2ecc71" if all_match else "#e74c3c"

        pred_overlay = overlay_masks(image_np, pred_mask_np)

        fig, axes = plt.subplots(2, 2, figsize=(11, 9.5), facecolor="#0d0d1a")
        for ax in axes.flat:
            ax.set_facecolor("#0d0d1a")

        # top-left: original image
        axes[0, 0].imshow(image_np)
        axes[0, 0].set_title("Original Image", fontsize=11,
                              fontweight="bold", color="white", pad=6)
        axes[0, 0].axis("off")

        # top-right: true labels panel
        axes[0, 1].set_facecolor("#12122a")
        axes[0, 1].set_title("True Labels", fontsize=11,
                              fontweight="bold", color="white", pad=6)
        _draw_label_panel(axes[0, 1], classes, true_labels)

        # bottom-left: predicted segmentation overlay
        axes[1, 0].imshow(pred_overlay)
        axes[1, 0].set_title("Predicted Segmentation Overlay", fontsize=11,
                              fontweight="bold", color="white", pad=6)
        axes[1, 0].axis("off")
        axes[1, 0].legend(handles=legend_patches, loc="lower right",
                          fontsize=8, framealpha=0.65,
                          facecolor="#0d0d1a", labelcolor="white")

        # bottom-right: predicted labels panel  (title/border = green or red)
        axes[1, 1].set_facecolor("#12122a")
        axes[1, 1].set_title("Predicted Labels", fontsize=11,
                              fontweight="bold", color=accent_c, pad=6)
        _draw_label_panel(axes[1, 1], classes, pred_labels, true_labels=true_labels)

        for spine in axes[1, 1].spines.values():
            spine.set_edgecolor(accent_c)
            spine.set_linewidth(2.5)
            spine.set_visible(True)

        result_label = "All Correct" if all_match else "Mismatch Detected"
        fig.suptitle(f"Example {fig_num + 1}  ·  {result_label}",
                     fontsize=13, fontweight="bold", color=accent_c, y=0.99)
        plt.tight_layout(rect=[0, 0, 1, 0.97])


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    config    = load_config("configs/config.yaml")
    classes   = config["data"]["classes"]
    threshold = config["post_processing"]["threshold"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Device: {device}")

    print("[INFO] Building test split …")
    test_dataset, test_loader = build_test_split(config)
    print(f"[INFO] Test set size: {len(test_dataset)} images  "
          f"({len(test_loader)} batches)")

    model = load_model(config, device)

    metrics = evaluate(model, test_loader, device, classes, threshold)
    print_metrics(metrics, classes)

    print("[INFO] Building metric figures …")
    fig_seg_metrics     (metrics, classes)
    fig_cls_metrics     (metrics, classes)
    fig_confusion_matrix(metrics, classes)
    fig_summary         (metrics, classes)

    print(f"[INFO] Building {NUM_EXAMPLES} visual prediction examples …")
    show_visual_examples(model, test_dataset, device, classes, threshold)

    print("[INFO] Displaying all figures …")
    plt.show()


if __name__ == "__main__":
    main()

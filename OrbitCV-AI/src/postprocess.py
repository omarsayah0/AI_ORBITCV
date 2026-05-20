import cv2
import numpy as np


def remove_small_masks(binary_mask, min_area):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_mask)
    result = np.zeros_like(binary_mask)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            result[labels == i] = 1
    return result


def postprocess_masks(pred_masks, threshold=0.5, min_area=500, kernel_size=3):
    """
    pred_masks: np.ndarray (C, H, W) float probabilities
    returns:    np.ndarray (C, H, W) binary uint8
    """
    result = np.zeros_like(pred_masks, dtype=np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

    for i in range(pred_masks.shape[0]):
        binary = (pred_masks[i] > threshold).astype(np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = remove_small_masks(binary, min_area)
        result[i] = binary

    return result

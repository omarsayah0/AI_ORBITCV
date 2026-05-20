# OrbitCV

## Satellite Signal Acquisition, Classical Computer Vision, and Deep Learning Analysis

OrbitCV is a complete end-to-end satellite imaging system. It covers the full pipeline from building a reception antenna and capturing live satellite signals via SDR, through interactive classical computer vision preprocessing and feature-based image alignment in C++/OpenCV, to deep learning-based cloud pattern segmentation and multi-label classification using a custom shared-encoder dual-head neural network.

Every stage of the pipeline operates on real satellite imagery captured from the **Meteor-M N2-4** Russian weather satellite using hand-built antennas and an SDR-based RF reception setup.

---

## Table of Contents

- [Introduction](#introduction)
- [System Overview](#system-overview)
- [Antenna and Signal Acquisition](#antenna-and-signal-acquisition)
- [Classical CV Pipeline — OrbitCV-Core](#classical-cv-pipeline--orbitcv-core)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [File Descriptions](#file-descriptions)
  - [Keyboard Controls](#keyboard-controls)
  - [SIFT vs ORB Comparison](#sift-vs-orb-comparison)
- [Deep Learning AI Pipeline — OrbitCV-AI](#deep-learning-ai-pipeline--orbitcv-ai)
  - [Dataset](#dataset)
  - [Model Architecture](#model-architecture)
  - [AI Features](#ai-features)
  - [AI Project Structure](#ai-project-structure)
  - [AI File Descriptions](#ai-file-descriptions)
  - [AI Results](#ai-results)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [How to Use](#how-to-use)
- [Example Outputs](#example-outputs)
- [Technical Notes](#technical-notes)
- [Conclusion](#conclusion)
- [Contributors](#contributors)
- [License](#license)

---

## Introduction

Satellite images require careful preprocessing and intelligent analysis before they can yield scientific or operational value. OrbitCV was built to demonstrate and implement this complete processing chain — from the physical act of receiving a satellite signal, to the final automated analysis of the image content using a trained neural network.

The project begins at the hardware level: a reception antenna is pointed at the sky, a satellite signal is captured using a software-defined radio, and that raw RF stream is decoded into a visual satellite image. That image then enters a classical CV preprocessing stage implemented in C++ and OpenCV, where geometric transformations, filtering, and feature-based image alignment can be applied interactively. Finally, the processed imagery feeds into a deep learning pipeline built in Python and PyTorch, which performs simultaneous semantic segmentation and multi-label classification of cloud formation patterns using a custom dual-head neural architecture.

OrbitCV connects hardware, classical signal processing, classical computer vision, and deep learning into one coherent workflow grounded in real satellite data.

---

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  1. Signal Acquisition                                           │
│     Hand-built V-dipole / QFH antenna                           │
│     Software-Defined Radio (SDR) receiver                       │
│     Meteor-M N2-4 signal reception at 137.9 MHz                 │
│     Raw RF stream decoded → satellite image                      │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│  2. Classical CV Module  (OrbitCV-Core — C++ / OpenCV 4)         │
│     Interactive geometric transformations                        │
│     Filtering and edge detection techniques                      │
│     SIFT & ORB feature matching, homography, image alignment     │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│  3. Deep Learning AI Module  (OrbitCV-AI — Python / PyTorch)     │
│     EfficientNet-b4 shared encoder                               │
│     UNet segmentation head — per-class cloud region masks        │
│     Classification head — multi-label cloud type prediction      │
│     4-flip TTA · classifier gate · morphological post-processing │
└──────────────────────────────────────────────────────────────────┘
```

---

## Antenna and Signal Acquisition

<table>
  <tr>
    <td width="50%" valign="top">
      <img src="https://github.com/user-attachments/assets/e0b4d0cb-4690-4d6f-bd3c-74f123e0f2e4" width="100%">
    </td>
    <td width="50%" valign="top">
      <img src="https://github.com/user-attachments/assets/83e79cd4-8039-4142-8307-70facb8e3e59" width="100%">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img width="900" height="1600" alt="6" src="https://github.com/user-attachments/assets/89a1050b-c5bd-40d8-aea7-054c8c8bb06e" width="100%">
    </td>
    <td width="50%" valign="top">
      <img width="900" height="1600" alt="5" src="https://github.com/user-attachments/assets/736d9865-c5f4-4030-a3a4-8688bfbb3bc8" width="100%">
    </td>
  </tr>
</table>

OrbitCV is grounded in a real RF-to-image reception workflow. Two antenna setups were used during the experiments:

- A **QFH (Quadrifilar Helix) antenna** built by a colleague at Al Hussein Technical University, used as the primary reception setup for the satellite signal experiments.
- A **V-dipole antenna** hand-built with my father, also used for satellite image reception and experiments.

Signals were received from the **Meteor-M N2-4** Russian weather satellite, which broadcasts imagery in the LRPT format at approximately **137.9 MHz**. An SDR receiver captured the raw RF signal, which was then decoded and reconstructed into a visual satellite image. That image is the direct input to the OrbitCV processing pipeline.

This hardware-to-software connection makes OrbitCV different from typical computer vision demos: every image processed by the system is a real photograph of Earth taken from orbit.

---

## Classical CV Pipeline — OrbitCV-Core

The OrbitCV-Core module is an interactive C++/OpenCV application that takes a satellite image as input and allows the user to apply three families of classical image processing operations through keyboard-driven interaction.

### Features

#### Geometric Transformations

- Reset to the original image
- Center crop
- Mouse-based ROI crop and region selection
- Horizontal flip
- Scale / resize image
- Rotate image
- Affine transformation
- Perspective transformation

#### Filtering Techniques

- Gaussian blur (smoothing and noise reduction)
- Median filter (impulse / salt-and-pepper noise removal)
- Bilateral filter (edge-preserving smoothing)
- Sharpening filter (detail enhancement using a Laplacian-style kernel)
- Sobel edge detection (gradient-based edges in X and Y directions)
- Laplacian edge detection (second-derivative edges with Gaussian pre-smoothing)

#### Feature Matching and Image Alignment

- **SIFT** (Scale-Invariant Feature Transform) — float descriptors, `NORM_L2` matching
- **ORB** (Oriented FAST and Rotated BRIEF) — binary descriptors, `NORM_HAMMING` matching, up to 2000 features
- Brute-force KNN descriptor matching with Lowe's ratio test (`0.75`) for both pipelines
- Homography estimation using `cv::findHomography` with RANSAC
- Perspective warping that aligns a second image onto the reference image plane
- Side-by-side visualisation of feature matches and the aligned result for each descriptor
- Direct SIFT vs ORB comparison — keypoints, good matches, RANSAC inliers, and runtime printed to the terminal

#### Interaction

- Keyboard-based interaction
- On-image control menu
- Terminal control menu

---

### Project Structure

```
OrbitCV-Core/
├── includes/
│   └── image.hpp
├── src/
│   ├── main.cpp
│   ├── draw.cpp
│   ├── print.cpp
│   ├── geometric_transformations/
│   │   ├── crop.cpp
│   │   ├── mouse.cpp
│   │   ├── flip.cpp
│   │   ├── scale.cpp
│   │   ├── rotate.cpp
│   │   ├── affine.cpp
│   │   └── perspective.cpp
│   ├── filtering_techniques/
│   │   ├── gaussian_blur.cpp
│   │   ├── median_blur.cpp
│   │   ├── bilateral_filter.cpp
│   │   ├── sharpening_filter.cpp
│   │   ├── sobel_edge.cpp
│   │   └── laplacian_edge.cpp
│   └── feature_matching/
│       ├── sift_descriptor/
│       │   ├── image_loader.cpp
│       │   ├── sift_features.cpp
│       │   ├── matcher.cpp
│       │   ├── homography.cpp
│       │   ├── display.cpp
│       │   └── sift_align_images.cpp
│       └── orb_descriptor/
│           ├── image_loader.cpp
│           ├── orb_features.cpp
│           ├── matcher.cpp
│           ├── homography.cpp
│           ├── display.cpp
│           └── orb_align_images.cpp
└── input/
    ├── image.jpeg
    └── second.jpg
```

The `src/` directory is split into three logical groups: `geometric_transformations/` for shape and position-based operations, `filtering_techniques/` for pixel-intensity-based operations, and `feature_matching/` for keypoint-based image alignment. The feature matching group is itself split into two parallel sub-pipelines — `sift_descriptor/` (float descriptors, L2 matching) and `orb_descriptor/` (binary descriptors, Hamming matching) — running the same workflow (load → grayscale → detect/describe → match → RANSAC homography → warp → display) so both descriptors can be compared side-by-side.

---

### File Descriptions

| File | Description |
|---|---|
| `Makefile` | Builds the core CV project using `g++`, `pkg-config`, and OpenCV 4. Final executable name is `image`. |
| `includes/image.hpp` | Main header file. Includes OpenCV and declares all image processing functions used across the project. |
| `src/main.cpp` | Program entry point. Loads `input/image.jpeg`, resizes to `1200×800`, displays the image, and handles keyboard interaction. |
| `src/draw.cpp` | Draws the control menu directly on the image window (geometric controls in green, filtering/feature-matching controls in orange). |
| `src/print.cpp` | Prints the available keyboard controls to the terminal. |
| `src/geometric_transformations/crop.cpp` | Fixed center crop using `cv::Rect`. |
| `src/geometric_transformations/mouse.cpp` | Mouse-based ROI selection. Drag to select, confirm, and receive the cropped result. |
| `src/geometric_transformations/flip.cpp` | Horizontal flip. |
| `src/geometric_transformations/scale.cpp` | Resize to `400×400` using linear interpolation. |
| `src/geometric_transformations/rotate.cpp` | Rotation by `30` degrees around the centre. |
| `src/geometric_transformations/affine.cpp` | Affine transformation using three source/destination point pairs. |
| `src/geometric_transformations/perspective.cpp` | Perspective transformation using four source/destination point pairs. |
| `src/filtering_techniques/gaussian_blur.cpp` | Gaussian blur with a `5×5` kernel. |
| `src/filtering_techniques/median_blur.cpp` | Median filter with kernel size `5`. |
| `src/filtering_techniques/bilateral_filter.cpp` | Bilateral filter (`d=9`, `sigmaColor=75`, `sigmaSpace=75`). |
| `src/filtering_techniques/sharpening_filter.cpp` | Sharpening via a `3×3` Laplacian-style kernel with `cv::filter2D`. |
| `src/filtering_techniques/sobel_edge.cpp` | Sobel edge detection in X and Y, combined with `cv::addWeighted`. |
| `src/filtering_techniques/laplacian_edge.cpp` | Laplacian edge detection after Gaussian pre-smoothing. |
| `src/feature_matching/sift_descriptor/sift_features.cpp` | `cv::SIFT` detector with default parameters; computes float descriptors. |
| `src/feature_matching/sift_descriptor/matcher.cpp` | BFMatcher (`NORM_L2`, `k=2`) with Lowe's ratio test at `0.75`. Requires ≥ 4 good matches. |
| `src/feature_matching/sift_descriptor/homography.cpp` | RANSAC homography estimation and `cv::warpPerspective` alignment. |
| `src/feature_matching/sift_descriptor/display.cpp` | Side-by-side SIFT match visualisation and aligned image display. |
| `src/feature_matching/sift_descriptor/sift_align_images.cpp` | Full SIFT pipeline orchestration. Times the run; prints keypoints / matches / inliers / runtime. Triggered by `x`. |
| `src/feature_matching/orb_descriptor/orb_features.cpp` | `cv::ORB::create(2000)` detector; computes binary descriptors. |
| `src/feature_matching/orb_descriptor/matcher.cpp` | BFMatcher (`NORM_HAMMING`, `k=2`) with Lowe's ratio test at `0.75`. Requires ≥ 4 good matches. |
| `src/feature_matching/orb_descriptor/homography.cpp` | Converts to grayscale, computes ORB features, runs KNN matching and RANSAC homography. |
| `src/feature_matching/orb_descriptor/display.cpp` | Side-by-side ORB match visualisation and aligned image display. |
| `src/feature_matching/orb_descriptor/orb_align_images.cpp` | Full ORB pipeline orchestration. Times the run; prints keypoints / matches / inliers / runtime. Triggered by `z`. |
| `input/image.jpeg` | Reference satellite image loaded by the application. |
| `input/second.jpg` | Second satellite image used by the SIFT and ORB feature matching workflows. |

---

### Keyboard Controls

After running `./image`, an OpenCV window appears with the satellite image and an on-screen control menu. Use the keyboard shortcuts below.

#### Geometric Transformations

| Key | Action |
|---|---|
| `o` | Reset to the original image |
| `c` | Apply centre crop |
| `m` | Select ROI using the mouse |
| `f` | Flip the image horizontally |
| `s` | Scale the image to `400×400` |
| `r` | Rotate the image by `30` degrees |
| `a` | Apply affine transformation |
| `p` | Apply perspective transformation |

#### Filtering Techniques

| Key | Action |
|---|---|
| `g` | Apply Gaussian blur (`5×5` kernel) |
| `n` | Apply median filter (kernel size `5`) |
| `b` | Apply bilateral filter (edge-preserving smoothing) |
| `h` | Apply sharpening filter (`3×3` Laplacian-style kernel) |
| `e` | Apply Sobel edge detection (X + Y gradients) |
| `l` | Apply Laplacian edge detection (with Gaussian pre-smoothing) |

#### Feature Matching and Image Alignment

| Key | Action |
|---|---|
| `x` | Run SIFT-based matching between the two input images, estimate homography with RANSAC, display matches and aligned result, print stats to terminal |
| `z` | Run ORB-based matching between the two input images, estimate homography with RANSAC, display matches and aligned result, print stats to terminal |

> Both `x` and `z` require `input/image.jpeg` and `input/second.jpg` to exist and do not modify the current interactive image. Running both on the same pair makes the SIFT vs ORB comparison directly observable.

#### General

| Key | Action |
|---|---|
| `q` / `ESC` | Quit |

#### Mouse ROI Selection

When pressing `m`, a new window appears for ROI selection:

| Action | Description |
|---|---|
| Drag mouse | Select a rectangular ROI |
| `c` | Confirm the selected ROI |
| `r` | Reset the selection |
| `q` / `ESC` | Cancel and return without changing the image |

---

### SIFT vs ORB Comparison

To evaluate the two descriptors fairly, the same `input/image.jpeg` and `input/second.jpg` pair was processed through both pipelines using identical downstream settings: brute-force KNN matching with `k=2`, Lowe's ratio test at `0.75`, and `cv::findHomography` with RANSAC. The only differences are the detector/descriptor and the matching norm (`NORM_L2` for SIFT float descriptors, `NORM_HAMMING` for ORB binary descriptors). ORB is capped at `2000` features per image; SIFT uses OpenCV's default parameters.

| Metric | ORB | SIFT |
|---|---|---|
| Image 1 keypoints | 2000 | 10304 |
| Image 2 keypoints | 2000 | 10950 |
| Good matches (Lowe 0.75) | 1180 | 7540 |
| RANSAC inliers | 1021 | 7471 |
| Runtime | **379.553 ms** | 1209.39 ms |
| Inlier ratio (inliers / good matches) | ~86.5% | ~99.1% |

**Key observations:**

- **Keypoint density** — SIFT detects roughly 5× more keypoints per image than ORB on this satellite pair. ORB is hard-capped to `2000` features; SIFT's default detector finds over `10,000` keypoints per image.
- **Match volume** — SIFT produces roughly 6× more good matches after Lowe's ratio test (`7540` vs `1180`), giving RANSAC far more correspondences to work with.
- **Match quality** — SIFT's RANSAC inlier ratio is ~99.1% vs ~86.5% for ORB. SIFT's float descriptors are more discriminative on this content.
- **Speed** — ORB is about 3.2× faster end-to-end (~380 ms vs ~1210 ms). Binary descriptors with Hamming distance are dramatically cheaper to compute and match than SIFT's high-dimensional float descriptors.
- **Trade-off** — On this satellite pair, SIFT is the clear accuracy winner. ORB is the clear performance winner and still produces over a thousand RANSAC inliers, which is more than sufficient for a stable homography — so ORB is preferable when latency matters and SIFT is preferable when alignment quality is the priority.

> Both pipelines print a stats block (`=== SIFT Results ===` / `=== ORB Results ===`) to the terminal each time they are run, so the comparison can be reproduced on any image pair.

---

## Deep Learning AI Pipeline — OrbitCV-AI

OrbitCV-AI is the deep learning component of the system. It performs simultaneous semantic segmentation and multi-label classification of four cloud formation types from satellite imagery using a single shared-encoder dual-head architecture built in Python and PyTorch.

### Dataset

This module uses the dataset from the **Understanding Cloud Organization** Kaggle competition.

> **Dataset:** [https://www.kaggle.com/competitions/understanding_cloud_organization/data](https://www.kaggle.com/competitions/understanding_cloud_organization/data)

The task is to identify regions in satellite images that contain one or more of four distinct cloud formation types: **Fish**, **Flower**, **Gravel**, and **Sugar**. Each image contains at least one formation and may contain all four. For each image–label pair the target is a segmentation mask encoded as a run-length encoded (RLE) string.

Images were captured by the MODIS instrument aboard the TERRA and AQUA polar-orbiting satellites. Labels were created through a crowd-sourcing activity at the **Max-Planck-Institut für Meteorologie** (Hamburg, Germany) and the **Laboratoire de météorologie dynamique** (Paris, France), with each image independently annotated by approximately three scientists from a team of 68.

| File | Description |
|---|---|
| `train.csv` | RLE-encoded segmentation masks for the training set |
| `train_images.zip` | Training satellite images |
| `test_images.zip` | Test satellite images |
| `sample_submission.csv` | Correctly formatted submission template |

> Predicted masks must be scaled down to **350 × 525 px** before submission.

---

### Model Architecture

OrbitCV-AI uses a custom dual-head model called **`UnetWithClassifier`** built on top of `segmentation_models_pytorch`. A single EfficientNet-b4 encoder is shared by both heads, meaning features are extracted only once per forward pass regardless of the number of tasks.

#### Segmentation Head

The encoder features pass through a standard UNet decoder, which progressively upsamples and merges skip connections from the encoder to recover spatial resolution. The final 1×1 convolution produces raw logits of shape `(B, 4, H, W)` — one channel per cloud class.

#### Classification Head

In parallel, the deepest encoder feature map (bottleneck) is passed through:

```
AdaptiveAvgPool2d(1)   →   spatial features collapsed to a single vector
Flatten                →   shape: (B, encoder_channels)
Dropout(p=0.5)         →   regularisation
Linear(encoder_channels → 4)   →   raw logits (B, 4)
```

This head predicts which cloud classes are present in the image without any spatial information, using only the richest abstract features from the encoder bottleneck.

#### Classifier Gate

At inference time, the classification probabilities gate the segmentation output. If the classifier predicts a class as absent (probability ≤ threshold), the entire segmentation mask for that class is zeroed out. This eliminates false-positive mask regions for cloud types that are not present in the image.

```
Satellite Image  (3 × 768 × 768)
        │
        ▼
EfficientNet-b4 Encoder  (shared)
        │
   ┌────┴────┐
   │         │
   ▼         ▼
UNet      AdaptiveAvgPool2d(1)
Decoder   → Flatten
   │       → Dropout(0.5)
   │       → Linear
   │         │
   ▼         ▼
Seg Logits  Cls Logits
(4 × H × W)   (4,)
        │
        ▼
   sigmoid on both
        │
        ▼
  Classifier Gate
  (zero absent-class masks)
        │
        ▼
  Final Predictions
```

#### Loss Function

The two heads are trained jointly with a combined loss:

```
Total Loss = (BCE_seg + Dice_seg) + 0.5 × BCE_cls
```

The segmentation loss is the sum of binary cross-entropy and Dice loss computed per class. The classification targets are derived automatically from the masks: a class is considered present if any pixel of its mask is active. The 0.5 weighting balances the two tasks without the classification signal overwhelming the segmentation gradients.

---

### AI Features

- **Dual-head architecture** — segmentation and classification from a single encoder in one forward pass
- **EfficientNet-b4 encoder** — pretrained on ImageNet; strong feature extraction with low parameter count
- **Classifier gate** — classification output suppresses false-positive segmentation masks for absent classes
- **Two-phase training** — encoder frozen in phase 1 (decoder learning), fully unfrozen in phase 2 (fine-tuning) with discriminative learning rates
- **Combined loss** — BCE + Dice for segmentation; BCE for classification; weighted sum
- **Per-class threshold tuning** — best threshold per class swept on the validation set after training
- **Test-time augmentation (TTA)** — four flip combinations averaged to improve prediction stability
- **Mask post-processing** — morphological closing followed by connected-component filtering to remove small noise regions
- **Early stopping** — triggered when the learning rate drops below `1e-5` and validation loss stops improving
- **Checkpoint saving and resuming** — training can be interrupted and resumed at any epoch
- **Full evaluation script** — `test.py` computes Dice, IoU, accuracy, precision, recall, F1, confusion matrix, and displays 5 visual prediction examples

---

### AI Project Structure

```
OrbitCV-AI/
├── configs/
│   └── config.yaml          # All hyperparameters, paths, and post-processing settings
├── src/
│   ├── dataset.py           # CloudDataset: image loading, RLE decoding, augmentation
│   ├── model.py             # UnetWithClassifier: dual-head model
│   ├── train.py             # Loss functions, training loop, validation, threshold tuning
│   ├── inference.py         # TTA-based single-image inference and visualisation
│   ├── postprocess.py       # Morphological closing and small-component removal
│   ├── rle.py               # RLE mask encoding and decoding
│   └── utils.py             # Config loading, seeding, directory creation, dataframe prep
├── data/
│   └── *.jpg                # Satellite images
├── outputs/
│   └── models/
│       ├── best_model.pth   # Saved whenever validation loss improves
│       ├── checkpoint.pth   # Full checkpoint (model + optimiser + scheduler + epoch)
│       └── final_model.pth  # Final model state after training completes
├── data.csv                 # Dataset labels (Image_Label, EncodedPixels columns)
├── main.py                  # Entry point: select train or inference mode
├── test.py                  # Evaluation script: metrics + interactive plots
└── pyproject.toml           # Python package definition and dependencies
```

---

### AI File Descriptions

| File | Description |
|---|---|
| `configs/config.yaml` | Central configuration: data paths, image size, class names, train/val/test splits, batch size, epochs, learning rate, backbone name, threshold, min mask area, morphology kernel size |
| `src/dataset.py` | `CloudDataset` — loads images with OpenCV, decodes per-class RLE masks, resizes to target resolution, applies Albumentations transforms, normalises with ImageNet statistics, returns `(image_tensor, mask_tensor)` |
| `src/model.py` | `UnetWithClassifier` — wraps `smp.Unet` with EfficientNet-b4 encoder; adds a classification head (AdaptiveAvgPool → Flatten → Dropout → Linear) on the encoder bottleneck; both heads share the encoder in a single forward pass |
| `src/train.py` | Dice loss, combined loss function, per-epoch train and validate functions, per-class threshold tuning, `safe_torch_load` with DataParallel key fixing, full `run_training` pipeline with two-phase optimiser and early stopping |
| `src/inference.py` | `predict_mask` with 4-flip TTA, `show_prediction` visualisation, `run_inference` end-to-end for a single dataset sample |
| `src/postprocess.py` | `postprocess_masks` — applies threshold, morphological closing with elliptical kernel, connected-component filtering by minimum area |
| `src/rle.py` | `rle_decode` — converts competition-format RLE strings to binary mask arrays using column-major ordering |
| `src/utils.py` | `load_config`, `seed_everything`, `create_dirs`, `prepare_dataframe` (splits `Image_Label` column into `image` and `class` columns) |
| `data.csv` | Labels file with `Image_Label` (format: `imagename_ClassName`) and `EncodedPixels` columns |
| `main.py` | Sets `mode = "train"` or `"inference"`, loads config, and dispatches to the appropriate pipeline |
| `test.py` | Rebuilds the exact test split, loads `final_model.pth`, runs full evaluation, prints a metric table to the terminal, and opens interactive matplotlib windows showing segmentation metrics, classification metrics, confusion matrices, a summary table, and 5 visual prediction examples |

---

### AI Results

Results measured on the held-out test split (10% of the dataset, 555 images) using `final_model.pth` with a threshold of 0.5.

#### Segmentation Metrics

| Class | Dice | IoU |
|---|---|---|
| Fish | 0.5277 | 0.3584 |
| Flower | 0.6966 | 0.5344 |
| Gravel | 0.5724 | 0.4010 |
| Sugar | 0.6277 | 0.4574 |
| **Mean** | **0.6061** | **0.4378** |

#### Classification Metrics

| Class | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Fish | 0.7189 | 0.7500 | 0.6522 | 0.6977 |
| Flower | 0.8342 | 0.8086 | 0.8280 | 0.8182 |
| Gravel | 0.6991 | 0.7291 | 0.7171 | 0.7231 |
| Sugar | 0.7640 | 0.8476 | 0.8010 | 0.8237 |
| **Mean** | **0.7541** | — | — | **0.7656** |

---

## Requirements

### Core CV Module (OrbitCV-Core)

- C++ (`g++` compiler)
- OpenCV 4
- `pkg-config`
- Make

### AI Module (OrbitCV-AI)

- Python 3.10 or higher
- PyTorch 2.0 or higher (CUDA recommended)
- All other Python dependencies are declared in `OrbitCV-AI/pyproject.toml` and installed automatically during the setup step

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/omarsayah0/AI_ORBITCV.git
cd AI_ORBITCV
```

---

### 2. Core CV Module Setup

The core C++ module does not require a Python environment. No `pip install` step is needed.

#### Install C++ Dependencies (Ubuntu/Debian)

```bash
make setup
```

This runs `sudo apt install g++ pkg-config libopencv-dev`. You can also install them manually:

```bash
sudo apt update
sudo apt install g++ pkg-config libopencv-dev
```

#### Build the Core Module

```bash
make
```

The Makefile compiles all source files under `OrbitCV-Core/src/` and produces an executable named `image` in the repository root.

#### Place the Input Image

Ensure `OrbitCV-Core/input/image.jpeg` exists. For feature matching, `OrbitCV-Core/input/second.jpg` is also required. If your image has a different name, update the path in `OrbitCV-Core/src/main.cpp`:

```cpp
cv::Mat pre_image = cv::imread("input/image.jpeg");
```

#### Run the Core Module

```bash
./image
```

---

### 3. AI Module Setup

#### Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

#### Install the AI Module

From the repository root:

```bash
make install
```

This is equivalent to:

```bash
cd OrbitCV-AI && pip install -e .
```

The editable install reads `OrbitCV-AI/pyproject.toml` and installs all declared dependencies automatically.

> If PyTorch does not detect your CUDA version, install it manually before running `make install`:
> ```bash
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```

#### Prepare the Data

Place satellite images in `OrbitCV-AI/data/` and place `data.csv` in `OrbitCV-AI/`. The CSV must have two columns: `Image_Label` (format: `imagename_ClassName`) and `EncodedPixels` (RLE string or empty).

The dataset is available from the [Understanding Cloud Organization Kaggle competition](https://www.kaggle.com/competitions/understanding_cloud_organization/data).

#### Configure

Edit `OrbitCV-AI/configs/config.yaml` to set paths, batch size, epochs, and any other settings before running.

| Key | Description |
|---|---|
| `data.image_size` | Input resolution (default: 768) |
| `data.classes` | List of cloud class names |
| `data.val_size` | Fraction of data used for validation |
| `data.test_size` | Fraction of data used for testing |
| `data.seed` | Random seed for reproducible splits |
| `train.epochs` | Maximum training epochs |
| `train.batch_size` | Batch size |
| `train.learning_rate` | Initial learning rate |
| `train.freeze_epochs` | Epochs to keep encoder frozen (default: 5) |
| `train.checkpoint_every` | Save a full checkpoint every N epochs |
| `model.backbone` | Encoder name passed to `smp.Unet` (default: `efficientnet-b4`) |
| `model.pretrained` | Load ImageNet pretrained weights for the encoder |
| `post_processing.threshold` | Default classification and segmentation threshold |
| `post_processing.min_area` | Minimum connected-component area (pixels) to keep |
| `post_processing.kernel_size` | Kernel size for morphological closing |

---

## How to Use

### Core CV Module

Run the compiled executable from the repository root:

```bash
./image
```

An OpenCV window will appear with the satellite image and an on-screen control menu. Use the keyboard shortcuts described in the [Keyboard Controls](#keyboard-controls) section above.

Transformations and filters are applied to the current image, so operations can be chained (for example: rotate, then sharpen, then apply Sobel edge detection). Press `o` at any time to reset to the original. The SIFT (`x`) and ORB (`z`) alignment workflows operate on the two input files on disk and do not modify the current interactive image.

---

### AI Module

#### Training

```bash
make train
```

This runs `python main.py` from within `OrbitCV-AI/` with `mode = "train"`. Training will:

1. Split the data into train / validation / test sets
2. Run phase 1 (encoder frozen) for `freeze_epochs` epochs
3. Switch to phase 2 (full fine-tuning) for the remaining epochs
4. Save `best_model.pth` whenever validation loss improves
5. Save `checkpoint.pth` every `checkpoint_every` epochs for resuming
6. Tune per-class thresholds on the validation set after training completes

To resume an interrupted run, simply re-run `make train` — the checkpoint is detected automatically.

#### Single-Image Inference

Open `OrbitCV-AI/main.py`, change `mode = "train"` to `mode = "inference"`, then run:

```bash
make train
```

This runs 4-flip TTA on a single image from the dataset, applies post-processing, and displays the predicted masks alongside the ground truth.

#### Evaluation (Full Test Set)

```bash
make test
```

This runs `python test.py` from within `OrbitCV-AI/`. It will:

- Rebuild the exact held-out test split (same seed as training)
- Load `final_model.pth`
- Run the full test set through the model
- Print segmentation and classification metrics to the terminal
- Open interactive matplotlib windows for all metric charts and 5 visual prediction examples

---

## Example Outputs

<img width="1413" height="873" alt="image" src="https://github.com/user-attachments/assets/deaa3793-e732-4f26-9f70-6aaca0717964" />

*Original satellite image displayed inside the interactive C++/OpenCV preprocessing window with keyboard controls.*

---

<img width="1411" height="876" alt="image" src="https://github.com/user-attachments/assets/6d266a3f-8679-424b-a3a3-013d67cb6077" />

*Pixel-level view of the received satellite image, showing RGB intensity values used for basic image inspection and analysis.*

---

<img width="1407" height="876" alt="image" src="https://github.com/user-attachments/assets/bc427c3e-258b-4ef4-9947-b2830efd77e6" />

*Satellite image after applying a 30° rotation transformation.*

---

<img width="1468" height="971" alt="image" src="https://github.com/user-attachments/assets/71630d89-d292-472d-823f-9b7ff84ed88b" />

*Mouse-based ROI selection mode (`m`), with the user manually selecting a region of interest from the satellite image.*

---

<img width="1417" height="869" alt="image" src="https://github.com/user-attachments/assets/050ea104-4514-4370-a7c3-fff8b441e6a1" />

*Gaussian blur applied to smooth noise and reduce small unwanted details before further analysis.*

---

<img width="1400" height="876" alt="image" src="https://github.com/user-attachments/assets/308f969a-9491-40db-a717-3c90e9d16e9d" />

*Sharpening filter applied to enhance edges and fine structures, making visual details clearer and more distinguishable.*

---

<img width="1407" height="875" alt="image" src="https://github.com/user-attachments/assets/2e7c5f70-be03-404d-9fdf-02cc1e0e92ba" />

*Laplacian edge detection highlighting rapid intensity changes and structural boundaries within the satellite image.*

---

<img width="1917" height="999" alt="image" src="https://github.com/user-attachments/assets/9d193bca-9f97-4b75-93d9-c9e412723081" />

*Reference satellite image used as the baseline for SIFT feature detection, matching, and automatic geometric alignment.*

---

<img width="1918" height="1012" alt="image" src="https://github.com/user-attachments/assets/6603f388-8d62-479b-bee7-9179f1f6ee96" />

*Rotated and transformed satellite image used as the second input for SIFT-based feature matching and alignment.*

---

<img width="1919" height="999" alt="image" src="https://github.com/user-attachments/assets/4d18d883-a11e-4fdc-93a6-f0942c1cd37e" />

*SIFT feature matching visualisation showing automatically detected correspondences between two transformed satellite images before geometric alignment.*

---

<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/76574cf8-b33c-493b-9708-0ac6c96003c4" />

*Automatically aligned satellite image produced after SIFT feature matching, homography estimation, and perspective-based geometric correction.*

---

## Technical Notes

### Core CV Module

- All image processing operations are deterministic and classical — no trained model is involved.
- OpenCV functions are used for image loading, resizing, display, mouse interaction, geometric transformations, and filtering.
- The input image is resized to `1200×800` at the start of the program for consistent display.
- Transformations and filters apply to the current image, not always the original, so operations can be chained. Press `o` to reset.
- Edge detection operators (Sobel and Laplacian) internally convert the image to grayscale, then convert the result back to BGR to maintain a consistent 3-channel display format.
- Filtering parameters are fixed in source:
  - **Gaussian blur** — `5×5` kernel, `sigma = 0` (auto-computed by OpenCV).
  - **Median filter** — kernel size `5`.
  - **Bilateral filter** — `d = 9`, `sigmaColor = 75`, `sigmaSpace = 75`.
  - **Sharpening** — `3×3` Laplacian-style kernel: `[[0,-1,0], [-1,5,-1], [0,-1,0]]`.
  - **Sobel** — `3×3` kernel, X and Y gradients combined with equal `0.5` weights.
  - **Laplacian** — `3×3` kernel after a `3×3` Gaussian pre-smoothing step.
- Feature matching parameters are fixed in source:
  - **SIFT** — default OpenCV parameters via `cv::SIFT::create()`; float descriptors.
  - **ORB** — `cv::ORB::create(2000)` (up to `2000` features per image); binary descriptors.
  - **Matcher** — `cv::BFMatcher` with `knnMatch(k=2)`; `NORM_L2` for SIFT, `NORM_HAMMING` for ORB.
  - **Lowe's ratio test** — threshold `0.75` for both pipelines.
  - **Minimum good matches** — at least `4` good matches required to estimate a homography.
  - **Homography** — `cv::findHomography` with `cv::RANSAC` for both descriptors.
  - **Warping** — `cv::warpPerspective` produces the aligned image at the reference image size.
  - Both pipelines time themselves with `std::chrono::high_resolution_clock` and print stats to stdout.

### AI Module

- **Dual-head single-pass design** — Both the segmentation decoder and the classification head read from the same encoder feature pyramid. The encoder runs exactly once per image. The classification head uses only the deepest feature map via global average pooling; the segmentation decoder uses all encoder levels through skip connections.
- **Classifier gate** — At inference, if the classifier score for a class is below the threshold, the entire predicted mask for that class is zeroed. This eliminates false-positive mask blobs for cloud types that are genuinely absent from the image, which is a common failure mode for pure segmentation models.
- **Two-phase training** — Phase 1 freezes all encoder parameters and trains only the decoder and classifier head from scratch. This prevents the untrained decoder from corrupting the pretrained encoder weights early on. Phase 2 unfreezes the full model with a lower encoder learning rate (`1e-4`) and a higher decoder/classifier rate (`1e-3`), allowing fine-tuning without catastrophic forgetting.
- **Combined loss** — The segmentation loss is BCE + Dice. BCE focuses on per-pixel accuracy while Dice directly optimises the overlap metric used for evaluation. The classification loss is plain BCE with targets derived from the masks. The total loss is `seg_loss + 0.5 × cls_loss`; the 0.5 weight prevents the simpler classification task from dominating the gradient signal.
- **Test-time augmentation** — Four flip variants of each image are run through the model independently. Segmentation probability maps are unflipped before averaging. This typically adds 1–2% Dice without additional training.
- **Mask post-processing** — After thresholding, morphological closing fills small gaps within predicted regions. Connected-component analysis then removes blobs smaller than `min_area` pixels. Both operations run on CPU with OpenCV after inference.
- **Threshold tuning** — After the main training loop, the best threshold for each class is found independently by sweeping 0.30–0.70 in steps of 0.05 on the validation set, selecting the value that maximises per-class Dice.
- **Limitations** — Resizing from the original 1400×2100 px to 768×768 px causes some loss of fine spatial detail for small cloud regions. The model is trained for four specific cloud classes and is not designed to generalise to other segmentation tasks without retraining.

---

## Conclusion

OrbitCV demonstrates the complete path from satellite signal reception to intelligent image analysis. Starting with hand-built antennas and SDR reception of a live weather satellite signal, the system produces real satellite imagery that is then processed through two tightly integrated stages.

The classical CV stage — implemented in C++/OpenCV — provides a practical, interactive toolkit covering **geometric transformations** (crop, flip, scale, rotate, affine, perspective), **filtering techniques** (Gaussian blur, median filter, bilateral filter, sharpening, Sobel and Laplacian edge detection), and **feature matching** using parallel SIFT and ORB pipelines with RANSAC-based homography warping. The side-by-side stats make the classic accuracy-vs-speed trade-off between the two descriptors directly observable on real satellite imagery.

The deep learning stage — implemented in Python and PyTorch — extends that foundation into automated analysis. A shared EfficientNet-b4 encoder feeds both a UNet segmentation decoder and a lightweight classification head, producing cloud formation masks and presence labels in a single forward pass. The classifier gate, two-phase training strategy, combined loss function, per-class threshold tuning, and 4-flip TTA together form a robust training and inference pipeline that achieves a mean Dice of 0.61 and mean classification F1 of 0.77 on the held-out test set.

Together, the two modules form a coherent end-to-end system that spans hardware, signal processing, classical computer vision, and deep learning — using real data from orbit at every stage.

---

## 👥 Contributors

- **Omar Al-Ethamat** — *AI Engineer*

Feel free to open issues or pull requests to contribute.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

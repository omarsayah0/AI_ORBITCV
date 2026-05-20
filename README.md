# OrbitCV
# Interactive Satellite Image Processing Tool

## Short Description

This project is an interactive **Computer Vision image preprocessing tool** built with **C++** and **OpenCV**.

It represents a practical end-to-end workflow, starting from the hardware side by preparing and using satellite reception antennas, capturing real signals from the Russian weather satellite **Meteor-M N2-4** through an **SDR-based RF setup**, converting the received data into a satellite image, and then analyzing and preprocessing that image inside this OpenCV application.

The tool allows the user to apply three main families of classical image preprocessing operations:

- **Geometric transformations**: crop, mouse-based ROI selection, flip, scale, rotation, affine transformation, and perspective transformation.
- **Filtering techniques**: Gaussian blur, median filter, bilateral filter, sharpening filter, Sobel edge detection, and Laplacian edge detection.
- **Feature matching & image alignment**: both **SIFT** and **ORB** keypoint detectors/descriptors, descriptor matching with Lowe's ratio test, RANSAC-based homography estimation, and perspective warping to align a second image onto a reference image. The two descriptors are implemented side-by-side so they can be compared on the same input pair.

Rather than being only a software demo, this project connects the complete path from **antenna-based satellite signal reception** to **interactive satellite image preprocessing and analysis**.

---

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [How to Use](#how-to-use)
- [Example Outputs / Results](#example-outputs--results)
- [SIFT vs ORB Comparison](#sift-vs-orb-comparison)
- [Technical Notes](#technical-notes)
- [Conclusion](#conclusion)
- [Contributors](#-contributors)
- [License](#-license)

---

## Introduction

Satellite images often need preprocessing before they can be used for analysis, visualization, enhancement, or later AI-based processing.

This project demonstrates an early practical stage in a satellite image processing pipeline. A satellite image is first received through a real RF workflow using an antenna and SDR, then loaded into a C++ OpenCV application where different preprocessing operations can be applied interactively.

The goal of this project is to help users understand how classical Computer Vision operations can be used as a foundation before moving into more advanced satellite image analysis tasks.

---

## Project Overview

The main workflow of the project is:

```text
Satellite signal / satellite image source
                ↓
Input image: input/image.jpeg
                ↓
C++ OpenCV preprocessing tool
                ↓
Interactive transformed image display
```

The application opens the input satellite image, resizes it for display, and allows the user to apply transformations using keyboard commands.

---

## Features

The project includes the following features based on the actual source code:

### Geometric Transformations
- Reset to the original image
- Center crop
- Mouse-based ROI crop / region selection
- Horizontal flip
- Scale / resize image
- Rotate image
- Affine transformation
- Perspective transformation

### Filtering Techniques
- Gaussian blur (smoothing / noise reduction)
- Median filter (impulse / salt-and-pepper noise removal)
- Bilateral filter (edge-preserving smoothing)
- Sharpening filter (detail enhancement using a Laplacian-style kernel)
- Sobel edge detection (gradient-based edges in X and Y directions)
- Laplacian edge detection (second-derivative edges with Gaussian pre-smoothing)

### Feature Matching & Image Alignment
- **SIFT** (Scale-Invariant Feature Transform) keypoint detection and descriptor extraction (float descriptors, `NORM_L2` matching)
- **ORB** (Oriented FAST and Rotated BRIEF) keypoint detection and descriptor extraction (binary descriptors, `NORM_HAMMING` matching, up to `2000` features)
- Brute-force KNN descriptor matching with Lowe's ratio test (`0.75`) for good-match filtering, used by both pipelines
- Homography estimation between two images using RANSAC (`cv::findHomography`)
- Perspective warping that aligns a second image onto the reference image
- Side-by-side visualization of feature matches and the aligned result for each descriptor
- Direct **SIFT vs ORB** comparison (keypoints, good matches, RANSAC inliers, runtime) printed to the terminal

### Interaction
- Keyboard-based interaction
- On-image control menu
- Terminal control menu

---

## Project Structure

Based on the provided project files and Makefile, the expected project structure is:

```text
.
├── Makefile
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

The `src/` directory is split into three logical groups: `geometric_transformations/` for shape/position-based operations, `filtering_techniques/` for pixel-intensity-based operations, and `feature_matching/` for keypoint-based image alignment. The `feature_matching/` group is itself split into two parallel sub-pipelines — `sift_descriptor/` (float descriptors, L2 matching) and `orb_descriptor/` (binary descriptors, Hamming matching) — so the same workflow (load → grayscale → detect/describe → match → RANSAC homography → warp → display) can be run with either descriptor and the results compared side-by-side.

### File Descriptions

| File | Description |
|---|---|
| `Makefile` | Builds the project using `g++`, `pkg-config`, and OpenCV 4. Compiles sources from `src/`, `src/geometric_transformations/`, `src/filtering_techniques/`, `src/feature_matching/sift_descriptor/`, and `src/feature_matching/orb_descriptor/`. The final executable name is `image`. |
| `includes/image.hpp` | Main header file. Includes OpenCV and declares all image processing functions used across the project — geometric transformations, filtering, the full SIFT pipeline, and the full ORB pipeline. |
| `src/main.cpp` | Program entry point. Loads `input/image.jpeg`, resizes it to `1200x800`, displays the image, and handles keyboard interaction for geometric transformations, filtering techniques, SIFT alignment (`x`), and ORB alignment (`z`). |
| `src/draw.cpp` | Draws the control menu directly on the image window (geometric controls in green, filtering/feature-matching controls in orange — including both `x: align_sift` and `z: align_orb`). |
| `src/print.cpp` | Prints the available keyboard controls in the terminal. |
| `src/geometric_transformations/crop.cpp` | Performs a fixed center crop using an OpenCV `cv::Rect` region. |
| `src/geometric_transformations/mouse.cpp` | Implements mouse-based ROI selection. The user drags over the image, confirms the selection, and receives the cropped result. |
| `src/geometric_transformations/flip.cpp` | Flips the image horizontally using OpenCV. |
| `src/geometric_transformations/scale.cpp` | Resizes the image to `400x400` using linear interpolation. |
| `src/geometric_transformations/rotate.cpp` | Rotates the image by `30` degrees around the center. |
| `src/geometric_transformations/affine.cpp` | Applies an affine transformation using three source points and three destination points. |
| `src/geometric_transformations/perspective.cpp` | Applies a perspective transformation using four source points and four destination points. |
| `src/filtering_techniques/gaussian_blur.cpp` | Applies a Gaussian blur with a `5x5` kernel for smoothing and noise reduction. |
| `src/filtering_techniques/median_blur.cpp` | Applies a median filter with kernel size `5`, useful for removing impulse / salt-and-pepper noise. |
| `src/filtering_techniques/bilateral_filter.cpp` | Applies a bilateral filter (`d=9`, `sigmaColor=75`, `sigmaSpace=75`) for edge-preserving smoothing. |
| `src/filtering_techniques/sharpening_filter.cpp` | Sharpens the image using a `3x3` Laplacian-style kernel via `cv::filter2D`. |
| `src/filtering_techniques/sobel_edge.cpp` | Detects edges using the Sobel operator in X and Y directions, then combines them with `cv::addWeighted`. |
| `src/filtering_techniques/laplacian_edge.cpp` | Detects edges using the Laplacian operator after a Gaussian pre-smoothing step to reduce noise. |
| `src/feature_matching/sift_descriptor/image_loader.cpp` | Loads the two input images (`input/image.jpeg` and `input/second.jpg`) and provides a grayscale-conversion helper used by the SIFT pipeline. |
| `src/feature_matching/sift_descriptor/sift_features.cpp` | Creates a `cv::SIFT` detector (default OpenCV parameters) and computes SIFT keypoints and float descriptors for a grayscale image using `detectAndCompute`. |
| `src/feature_matching/sift_descriptor/matcher.cpp` | Performs brute-force KNN descriptor matching (`cv::BFMatcher`, `NORM_L2`, `k=2`) and filters good matches using Lowe's ratio test with a `0.75` threshold. Requires at least 4 good matches. |
| `src/feature_matching/sift_descriptor/homography.cpp` | Estimates the homography matrix between matched SIFT keypoints using `cv::findHomography` with RANSAC, and warps the second image onto the reference image plane using `cv::warpPerspective`. |
| `src/feature_matching/sift_descriptor/display.cpp` | Renders the side-by-side SIFT feature matches with `cv::drawMatches` and displays the reference image and the aligned image in separate OpenCV windows. |
| `src/feature_matching/sift_descriptor/sift_align_images.cpp` | Orchestrates the full SIFT alignment pipeline: load → grayscale → SIFT features → match → homography → warp → display. Also times the run and prints **SIFT keypoints / good matches / RANSAC inliers / runtime** to the terminal. Triggered by pressing `x`. |
| `src/feature_matching/orb_descriptor/image_loader.cpp` | Loads `input/image.jpeg` and `input/second.jpg` as color images for the ORB pipeline (grayscale conversion is performed inside the ORB homography step). |
| `src/feature_matching/orb_descriptor/orb_features.cpp` | Creates a `cv::ORB` detector with `nfeatures = 2000` and computes ORB keypoints and binary descriptors for a grayscale image using `detectAndCompute`. |
| `src/feature_matching/orb_descriptor/matcher.cpp` | Performs brute-force KNN descriptor matching for ORB (`cv::BFMatcher`, `NORM_HAMMING`, `k=2`) and filters good matches using Lowe's ratio test with a `0.75` threshold. Requires at least 4 good matches. |
| `src/feature_matching/orb_descriptor/homography.cpp` | Converts both inputs to grayscale, computes ORB features, runs Hamming-distance KNN matching, and estimates the homography between matched ORB keypoints using `cv::findHomography` with RANSAC. |
| `src/feature_matching/orb_descriptor/display.cpp` | Renders the side-by-side ORB feature matches with `cv::drawMatches` and displays them along with the aligned image in separate OpenCV windows (`ORB Feature Matches`, `ORB Aligned Image`). |
| `src/feature_matching/orb_descriptor/orb_align_images.cpp` | Orchestrates the full ORB alignment pipeline: load → ORB homography (features + match + RANSAC) → warp → display. Also times the run and prints **ORB keypoints / good matches / RANSAC inliers / runtime** to the terminal. Triggered by pressing `z`. |
| `input/image.jpeg` | Required reference input image loaded by the application. |
| `input/second.jpg` | Second input image used by both the SIFT (`x`) and ORB (`z`) feature matching and alignment workflows. |

---

## Requirements

To build and run this project, you need:

- C++
- `g++` compiler
- OpenCV 4
- `pkg-config`
- Make

---

## Setup and Installation

### 1. Clone or Download the Project

```bash
git clone git@github.com:omarsayah0/AI_ORBITCV.git
cd AI_ORBITCV
```

Or download the project folder manually.

---

### 2. Install Dependencies

The Makefile includes a setup command for Ubuntu/Debian-based systems:

```bash
make setup
```

This installs:

```bash
g++
pkg-config
libopencv-dev
```

You can also install them manually:

```bash
sudo apt update
sudo apt install g++ pkg-config libopencv-dev
```

---

### 3. Place the Input Image

The code loads the image from:

```text
input/image.jpeg
```

Make sure your satellite image has this exact path and filename.

If your image has another name or extension, either rename it to `image.jpeg` or update this line in `src/main.cpp`:

```cpp
cv::Mat pre_image = cv::imread("input/image.jpeg");
```

---

### 5. Build the Project

```bash
make
```

The Makefile will compile the source files and generate an executable named:

```text
image
```

---

### 6. Run the Application

```bash
./image
```

---

## How to Use

After running the program, an OpenCV window will appear with the satellite image and an on-image control menu.

Use the keyboard controls below:

#### Geometric Transformations

| Key | Action |
|---|---|
| `o` | Reset to the original image |
| `c` | Apply center crop |
| `m` | Select ROI using the mouse |
| `f` | Flip the image horizontally |
| `s` | Scale the image to `400x400` |
| `r` | Rotate the image by `30` degrees |
| `a` | Apply affine transformation |
| `p` | Apply perspective transformation |

#### Filtering Techniques

| Key | Action |
|---|---|
| `g` | Apply Gaussian blur (`5x5` kernel) |
| `n` | Apply median filter (kernel size `5`) |
| `b` | Apply bilateral filter (edge-preserving smoothing) |
| `h` | Apply sharpening filter (`3x3` Laplacian-style kernel) |
| `e` | Apply Sobel edge detection (X + Y gradients) |
| `l` | Apply Laplacian edge detection (with Gaussian pre-smoothing) |

#### Feature Matching & Image Alignment

| Key | Action |
|---|---|
| `x` | Run **SIFT**-based feature matching between `input/image.jpeg` and `input/second.jpg`, estimate the homography with RANSAC, display the matches alongside the aligned second image, and print SIFT keypoints / good matches / inliers / runtime to the terminal |
| `z` | Run **ORB**-based feature matching between `input/image.jpeg` and `input/second.jpg`, estimate the homography with RANSAC, display the matches alongside the aligned second image, and print ORB keypoints / good matches / inliers / runtime to the terminal |

> Both `x` and `z` require `input/image.jpeg` and `input/second.jpg` to exist. The SIFT workflow opens **SIFT Feature Matches**, **Reference Image**, and **Aligned Second Image** windows. The ORB workflow opens **ORB Feature Matches** and **ORB Aligned Image** windows. Press any key inside any of those windows to return to the main view. Running both `x` and `z` on the same input pair makes the SIFT vs ORB comparison directly observable (see the [SIFT vs ORB Comparison](#sift-vs-orb-comparison) section).

#### General

| Key | Action |
|---|---|
| `q` | Quit |
| `ESC` | Quit |

### Mouse ROI Selection

When pressing `m`, a new window appears for ROI selection.

Inside the ROI window:

| Key / Action | Description |
|---|---|
| Drag mouse | Select a rectangular ROI |
| `c` | Confirm the selected ROI |
| `r` | Reset the selection |
| `q` / `ESC` | Cancel and return without changing the image |

---

## Practical Reception Setup

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

This project is connected to a real satellite reception workflow. During the experiments, two antenna setups were used:

- A **QFH antenna** used for satellite image reception. This antenna was built by one of my colleagues at Al Hussein Technical University and was used as part of the reception setup.
- A **hand-built V-dipole antenna** that I built with my father and also used for satellite image reception experiments.
- Image shows the **real satellite signal capture** process during the SDR reception workflow.
These practical reception setups helped connect the project to a real RF-to-image workflow before applying the OpenCV preprocessing operations.

---
## Example Outputs / Results

<img width="1413" height="873" alt="image" src="https://github.com/user-attachments/assets/deaa3793-e732-4f26-9f70-6aaca0717964" />

*Original satellite image displayed inside the interactive C++/OpenCV preprocessing window with keyboard controls.*

---

<img width="1411" height="876" alt="image" src="https://github.com/user-attachments/assets/6d266a3f-8679-424b-a3a3-013d67cb6077" />

*Pixel-level view of the received satellite image, showing RGB intensity values used for basic image inspection and analysis.*

---

<img width="1407" height="876" alt="image" src="https://github.com/user-attachments/assets/bc427c3e-258b-4ef4-9947-b2830efd77e6" />

*Satellite image after applying a 30° rotation transformation in the interactive OpenCV preprocessing tool.*

---

<img width="1468" height="971" alt="image" src="https://github.com/user-attachments/assets/71630d89-d292-472d-823f-9b7ff84ed88b" />

*Mouse-based ROI selection mode, where the user presses `m` and manually selects a region of interest from the satellite image.*

---

<img width="1417" height="869" alt="image" src="https://github.com/user-attachments/assets/050ea104-4514-4370-a7c3-fff8b441e6a1" />

*Satellite image after applying Gaussian Blur filtering, used to smooth noise and reduce small unwanted details before further image analysis.*

---

<img width="1400" height="876" alt="image" src="https://github.com/user-attachments/assets/308f969a-9491-40db-a717-3c90e9d16e9d" />

*Sharpening filter applied to enhance edges and fine structures in the satellite image, making visual details clearer and more distinguishable.*

---

<img width="1407" height="875" alt="image" src="https://github.com/user-attachments/assets/2e7c5f70-be03-404d-9fdf-02cc1e0e92ba" />

*Laplacian edge detection applied to highlight rapid intensity changes and emphasize boundaries and structural features within the satellite image.*

---

<img width="1917" height="999" alt="image" src="https://github.com/user-attachments/assets/9d193bca-9f97-4b75-93d9-c9e412723081" />

*Reference satellite image used as the baseline image for SIFT feature detection, matching, and automatic geometric alignment.*

---

<img width="1918" height="1012" alt="image" src="https://github.com/user-attachments/assets/6603f388-8d62-479b-bee7-9179f1f6ee96" />

*Rotated and transformed satellite image used as the second input image for SIFT-based feature matching and automatic image alignment.*

---

<img width="1919" height="999" alt="image" src="https://github.com/user-attachments/assets/4d18d883-a11e-4fdc-93a6-f0942c1cd37e" />

*SIFT feature matching visualization showing automatically detected corresponding satellite image features between two transformed images before geometric alignment.*

---

<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/76574cf8-b33c-493b-9708-0ac6c96003c4" />

*Automatically aligned satellite image produced after SIFT feature matching, homography estimation, and perspective-based geometric correction.*

---

## SIFT vs ORB Comparison

To evaluate the two descriptors fairly, the same `input/image.jpeg` and `input/second.jpg` pair was processed through both pipelines (`x` for SIFT, `z` for ORB) using identical downstream settings: brute-force KNN matching with `k = 2`, Lowe's ratio test at `0.75`, and `cv::findHomography` with RANSAC. The only differences are the detector/descriptor itself and the matching norm (`NORM_L2` for SIFT float descriptors, `NORM_HAMMING` for ORB binary descriptors). ORB is capped at `2000` features per image, while SIFT runs with OpenCV's default parameters and detects as many keypoints as it finds.

Measured results on the same image pair:

| Metric | ORB | SIFT |
|---|---|---|
| Image 1 keypoints | 2000 | 10304 |
| Image 2 keypoints | 2000 | 10950 |
| Good matches (Lowe 0.75) | 1180 | 7540 |
| RANSAC inliers | 1021 | 7471 |
| Runtime | **379.553 ms** | 1209.39 ms |
| Inlier ratio (inliers / good matches) | ~86.5% | ~99.1% |

**Observations from this run:**

- **Density of keypoints** — SIFT detects roughly `5×` more keypoints per image than ORB on this satellite pair. ORB is hard-capped to `2000` features by `cv::ORB::create(2000)`, while SIFT's default detector finds over `10,000` keypoints per image.
- **Match volume** — SIFT also produces roughly `6×` more good matches after Lowe's ratio test (`7540` vs `1180`), which gives RANSAC far more correspondences to work with.
- **Match quality** — SIFT's RANSAC inlier ratio is **~99.1%**, vs **~86.5%** for ORB. SIFT's float descriptors are more discriminative on this content, so a larger fraction of its good matches survive the geometric consistency check.
- **Speed** — ORB is about **3.2× faster** end-to-end (`~380 ms` vs `~1210 ms`). This matches the well-known trade-off: ORB's binary descriptors with Hamming distance are dramatically cheaper to compute and match than SIFT's high-dimensional float descriptors.
- **When each one wins** — On this satellite pair, SIFT is the clear accuracy winner (more inliers, higher inlier ratio, more robust homography). ORB is the clear performance winner and still produces over a thousand RANSAC inliers, which is more than enough for a stable homography — so ORB is preferable when latency matters (e.g., real-time or batch processing of many image pairs) and SIFT is preferable when alignment quality is the priority.

> The exact numbers depend on the input pair, ORB's `nfeatures` cap, and the Lowe ratio threshold. Both pipelines print their own stats block (`=== SIFT Results ===` / `=== ORB Results ===`) to the terminal each time they are run, so the comparison can be reproduced on any image pair.

---


## Technical Notes

- The project uses deterministic image processing operations.
- It is based on classical Computer Vision, not a trained AI model.
- OpenCV functions are used for image loading, resizing, display, mouse interaction, geometric transformations, and filtering.
- The input image is resized to `1200x800` at the start of the program for consistent display.
- Transformations and filters are applied interactively to the current image, not always to the original image, so operations can be chained (for example: rotate, then sharpen, then apply Sobel edge detection). Press `o` at any time to reset to the original.
- Filtering parameters are fixed in the source code:
  - **Gaussian blur** — `5x5` kernel, `sigma = 0` (auto-computed by OpenCV).
  - **Median filter** — kernel size `5`.
  - **Bilateral filter** — `d = 9`, `sigmaColor = 75`, `sigmaSpace = 75`.
  - **Sharpening** — `3x3` Laplacian-style kernel: `[[0,-1,0], [-1,5,-1], [0,-1,0]]`.
  - **Sobel** — `3x3` kernel, X and Y gradients combined with equal `0.5` weights.
  - **Laplacian** — `3x3` kernel applied after a `3x3` Gaussian pre-smoothing step.
- Feature matching and alignment parameters are fixed in the source code:
  - **SIFT detector** — default OpenCV parameters via `cv::SIFT::create()`; float descriptors.
  - **ORB detector** — `cv::ORB::create(2000)` (up to `2000` features per image); binary descriptors.
  - **Descriptor matcher** — `cv::BFMatcher` with `knnMatch` (`k = 2`); `NORM_L2` for SIFT, `NORM_HAMMING` for ORB.
  - **Lowe's ratio test** — threshold `0.75` for both pipelines (a match is kept when the best distance is below `0.75 ×` the second-best).
  - **Minimum good matches** — at least `4` good matches are required to estimate a homography in both pipelines.
  - **Homography estimation** — `cv::findHomography` with `cv::RANSAC` for both SIFT and ORB.
  - **Warping** — `cv::warpPerspective` produces the aligned image at the reference image size.
  - **Reported stats** — both pipelines time themselves with `std::chrono::high_resolution_clock` and print `keypoints / good matches / RANSAC inliers / runtime (ms)` to stdout.
- The SIFT (`x`) and ORB (`z`) alignment workflows operate directly on the two input files on disk and do **not** modify the current interactive image, so they can be triggered at any time without affecting chained geometric/filtering operations.
- Edge detection operators (Sobel and Laplacian) internally convert the image to grayscale, then convert the result back to BGR so that the displayed image keeps a consistent 3-channel format.
- The project can be extended later with AI models for classification, segmentation, denoising, or satellite image analysis.

---

## Conclusion

This project provides a practical demonstration of how a satellite image captured through an RF and SDR workflow can be processed using classical Computer Vision techniques, covering **geometric transformations** (crop, flip, scale, rotate, affine, perspective), **filtering techniques** (Gaussian blur, median filter, bilateral filter, sharpening, Sobel and Laplacian edge detection), and **feature matching with image alignment** using two parallel descriptor pipelines — **SIFT** (float descriptors, `NORM_L2`) and **ORB** (binary descriptors, `NORM_HAMMING`) — both running through ratio-tested KNN matching and RANSAC-based homography warping. Side-by-side stats make the classic SIFT-vs-ORB **accuracy-vs-speed trade-off** directly observable on real satellite imagery.

It is a useful educational step between satellite image acquisition and more advanced image analysis. By combining real satellite imagery with OpenCV preprocessing — reshaping the geometry of the image, enhancing or extracting features through filtering, and aligning multiple captures via both SIFT- and ORB-based registration — the project creates a strong foundation for future satellite image enhancement, segmentation, multi-pass registration, or AI-based analysis.

---

## 👥 Contributors

- **Omar Al ethamat** – *AI Engineer*

Feel free to open issues or pull requests to contribute.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


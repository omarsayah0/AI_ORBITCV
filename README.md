# OrbitCV
# Interactive Satellite Image Processing Tool

## Short Description

This project is an interactive **Computer Vision image preprocessing tool** built with **C++** and **OpenCV**.

It represents a practical end-to-end workflow, starting from the hardware side by preparing and using satellite reception antennas, capturing real signals from the Russian weather satellite **Meteor-M N2-4** through an **SDR-based RF setup**, converting the received data into a satellite image, and then analyzing and preprocessing that image inside this OpenCV application.

The tool allows the user to apply three main families of classical image preprocessing operations:

- **Geometric transformations**: crop, mouse-based ROI selection, flip, scale, rotation, affine transformation, and perspective transformation.
- **Filtering techniques**: Gaussian blur, median filter, bilateral filter, sharpening filter, Sobel edge detection, and Laplacian edge detection.
- **Feature matching & image alignment**: SIFT keypoint detection, descriptor matching with Lowe's ratio test, RANSAC-based homography estimation, and perspective warping to align a second image onto a reference image.

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
- SIFT (Scale-Invariant Feature Transform) keypoint detection and descriptor extraction
- Brute-force KNN descriptor matching with Lowe's ratio test (`0.75`) for good-match filtering
- Homography estimation between two images using RANSAC
- Perspective warping that aligns a second image onto the reference image
- Side-by-side visualization of feature matches, the reference image, and the aligned result

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
│       ├── image_loader.cpp
│       ├── sift_features.cpp
│       ├── matcher.cpp
│       ├── homography.cpp
│       ├── display.cpp
│       └── sift_align_images.cpp
└── input/
    ├── image.jpeg
    └── second.jpg
```

The `src/` directory is split into three logical groups: `geometric_transformations/` for shape/position-based operations, `filtering_techniques/` for pixel-intensity-based operations, and `feature_matching/` for SIFT-based keypoint detection, descriptor matching, and homography-based image alignment.

### File Descriptions

| File | Description |
|---|---|
| `Makefile` | Builds the project using `g++`, `pkg-config`, and OpenCV 4. Compiles sources from `src/`, `src/geometric_transformations/`, `src/filtering_techniques/`, and `src/feature_matching/`. The final executable name is `image`. |
| `includes/image.hpp` | Main header file. Includes OpenCV and declares all image processing functions used across the project (geometric and filtering). |
| `src/main.cpp` | Program entry point. Loads `input/image.jpeg`, resizes it to `1200x800`, displays the image, and handles keyboard interaction for both geometric transformations and filtering techniques. |
| `src/draw.cpp` | Draws the control menu directly on the image window (geometric controls in green, filtering controls in orange). |
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
| `src/feature_matching/image_loader.cpp` | Loads the two input images (`input/image.jpeg` and `input/second.jpg`) and converts them to grayscale for SIFT processing. |
| `src/feature_matching/sift_features.cpp` | Creates a `cv::SIFT` detector and computes SIFT keypoints and descriptors for a grayscale image using `detectAndCompute`. |
| `src/feature_matching/matcher.cpp` | Performs brute-force KNN descriptor matching (`cv::BFMatcher`, `NORM_L2`, `k=2`) and filters good matches using Lowe's ratio test with a `0.75` threshold. Requires at least 4 good matches. |
| `src/feature_matching/homography.cpp` | Estimates the homography matrix between matched keypoints using `cv::findHomography` with RANSAC, and warps the second image onto the reference image plane using `cv::warpPerspective`. |
| `src/feature_matching/display.cpp` | Renders the side-by-side feature matches with `cv::drawMatches` and displays the reference image and the aligned image in separate OpenCV windows. |
| `src/feature_matching/sift_align_images.cpp` | Orchestrates the full SIFT alignment pipeline: load → grayscale → SIFT features → match → homography → warp → display. Triggered by pressing `x`. |
| `input/image.jpeg` | Required reference input image loaded by the application. |
| `input/second.jpg` | Second input image used by the SIFT feature matching and alignment workflow (`x` key). |

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
| `x` | Run SIFT-based feature matching between `input/image.jpeg` and `input/second.jpg`, estimate the homography with RANSAC, and display the matches alongside the aligned second image |

> The `x` action requires both `input/image.jpeg` and `input/second.jpg` to exist. It opens three windows: **SIFT Feature Matches** (side-by-side keypoint correspondences), **Reference Image**, and **Aligned Second Image**. Press any key inside any of these windows to return to the main view.

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
  - **SIFT detector** — default OpenCV parameters via `cv::SIFT::create()`.
  - **Descriptor matcher** — `cv::BFMatcher` with `NORM_L2` and `knnMatch` (`k = 2`).
  - **Lowe's ratio test** — threshold `0.75` (a match is kept when the best distance is below `0.75 ×` the second-best).
  - **Minimum good matches** — at least `4` good matches are required to estimate a homography.
  - **Homography estimation** — `cv::findHomography` with `cv::RANSAC`.
  - **Warping** — `cv::warpPerspective` produces the aligned image at the reference image size.
- The SIFT alignment workflow (`x`) operates directly on the two input files on disk and does **not** modify the current interactive image, so it can be triggered at any time without affecting chained geometric/filtering operations.
- Edge detection operators (Sobel and Laplacian) internally convert the image to grayscale, then convert the result back to BGR so that the displayed image keeps a consistent 3-channel format.
- The project can be extended later with AI models for classification, segmentation, denoising, or satellite image analysis.

---

## Conclusion

This project provides a practical demonstration of how a satellite image captured through an RF and SDR workflow can be processed using classical Computer Vision techniques, covering **geometric transformations** (crop, flip, scale, rotate, affine, perspective), **filtering techniques** (Gaussian blur, median filter, bilateral filter, sharpening, Sobel and Laplacian edge detection), and **feature matching with image alignment** (SIFT keypoints, ratio-tested descriptor matching, and RANSAC-based homography warping).

It is a useful educational step between satellite image acquisition and more advanced image analysis. By combining real satellite imagery with OpenCV preprocessing — reshaping the geometry of the image, enhancing or extracting features through filtering, and aligning multiple captures via SIFT-based registration — the project creates a strong foundation for future satellite image enhancement, segmentation, multi-pass registration, or AI-based analysis.

---

## 👥 Contributors

- **Omar Al ethamat** – *AI Engineer*

Feel free to open issues or pull requests to contribute.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

# ORBITCV
# Interactive Satellite Image Processing Tool

## Short Description

This project is an interactive **Computer Vision image preprocessing tool** built with **C++** and **OpenCV**.

It represents a practical end-to-end workflow, starting from the hardware side by preparing and using satellite reception antennas, capturing real signals from the Russian weather satellite **Meteor-M N2-4** through an **SDR-based RF setup**, converting the received data into a satellite image, and then analyzing and preprocessing that image inside this OpenCV application.

The tool allows the user to apply classical image preprocessing operations, including crop, mouse-based ROI selection, flip, scale, rotation, affine transformation, and perspective transformation.

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

- Reset to the original image
- Center crop
- Mouse-based ROI crop / region selection
- Horizontal flip
- Scale / resize image
- Rotate image
- Affine transformation
- Perspective transformation
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
│   ├── crop.cpp
│   ├── mouse.cpp
│   ├── flip.cpp
│   ├── scale.cpp
│   ├── rotate.cpp
│   ├── affine.cpp
│   ├── perspective.cpp
│   ├── draw.cpp
│   └── print.cpp
└── input/
    └── image.jpeg
```

### File Descriptions

| File | Description |
|---|---|
| `Makefile` | Builds the project using `g++`, `pkg-config`, and OpenCV 4. The final executable name is `image`. |
| `includes/image.hpp` | Main header file. Includes OpenCV and declares all image processing functions used across the project. |
| `src/main.cpp` | Program entry point. Loads `input/image.jpeg`, resizes it to `1200x800`, displays the image, and handles keyboard interaction. |
| `src/crop.cpp` | Performs a fixed center crop using an OpenCV `cv::Rect` region. |
| `src/mouse.cpp` | Implements mouse-based ROI selection. The user drags over the image, confirms the selection, and receives the cropped result. |
| `src/flip.cpp` | Flips the image horizontally using OpenCV. |
| `src/scale.cpp` | Resizes the image to `400x400` using linear interpolation. |
| `src/rotate.cpp` | Rotates the image by `30` degrees around the center. |
| `src/affine.cpp` | Applies an affine transformation using three source points and three destination points. |
| `src/perspective.cpp` | Applies a perspective transformation using four source points and four destination points. |
| `src/draw.cpp` | Draws the control menu directly on the image window. |
| `src/print.cpp` | Prints the available keyboard controls in the terminal. |
| `input/image.jpeg` | Required input image file loaded by the application. |

> Note: The uploaded files were provided individually, but the Makefile expects the source files to be inside `src/` and the header file to be inside `includes/`.

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
      <img width="1600" height="1200" alt="1" src="https://github.com/user-attachments/assets/90e75cd6-4d4e-4517-81d5-a54a5e003181" width="100%">
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

<img width="1409" height="877" alt="image" src="https://github.com/user-attachments/assets/25ffea2c-e713-4b97-b3e8-ae5b157393ba" />

*Original satellite image displayed inside the interactive C++/OpenCV preprocessing window with keyboard controls.*

---

<img width="1411" height="876" alt="image" src="https://github.com/user-attachments/assets/6d266a3f-8679-424b-a3a3-013d67cb6077" />

*Pixel-level view of the received satellite image, showing RGB intensity values used for basic image inspection and analysis.*

---

<img width="1408" height="874" alt="image" src="https://github.com/user-attachments/assets/f1728309-15df-47b7-8849-71c67a9689b6" />

*Satellite image after applying a 30° rotation transformation in the interactive OpenCV preprocessing tool.*

---

<img width="1468" height="971" alt="image" src="https://github.com/user-attachments/assets/71630d89-d292-472d-823f-9b7ff84ed88b" />

*Mouse-based ROI selection mode, where the user presses `m` and manually selects a region of interest from the satellite image.*

---

## Technical Notes

- The project uses deterministic image processing operations.
- It is based on classical Computer Vision, not a trained AI model.
- OpenCV functions are used for image loading, resizing, display, mouse interaction, and geometric transformations.
- The input image is resized to `1200x800` at the start of the program for consistent display.
- Transformations are applied interactively to the current image, not always to the original image.
- The project can be extended later with AI models for classification, segmentation, denoising, or satellite image analysis.

---

## Conclusion

This project provides a practical demonstration of how a satellite image captured through an RF and SDR workflow can be processed using classical Computer Vision techniques.

It is a useful educational step between satellite image acquisition and more advanced image analysis. By combining real satellite imagery with OpenCV preprocessing, the project creates a strong foundation for future satellite image enhancement, segmentation, or AI-based analysis.

---

## 👥 Contributors

- **Omar Alethamat** – *AI Engineer*

Feel free to open issues or pull requests to contribute.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

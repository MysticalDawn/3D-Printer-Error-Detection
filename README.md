# 3D-Printer-Error-Detection
<h1>
  Welcome to Our Project
</h1>

## Dataset Used

### Auto-ZMJ2N Dataset
- **Title**: Auto Dataset
- **Type**: Open Source Dataset
- **Author**: TU Berlin
- **Published by**: Roboflow
- **Journal**: Roboflow Universe
- **Year**: 2023
- **Month**: September
- **URL**: [Auto-ZMJ2N Dataset](https://universe.roboflow.com/tu-berlin-pvdvq/auto-zmj2n)
- **Note**: Visited on 2024-07-30
- **License**: CC BY 4.0
- **Data Path**: `Auto-ZMJ2N/train`

### Dataset Overview
- **Total Images**: 2,158
- **Annotations**: Multi-Class Classification format for Void, Overheating, Stringing, and Gaps.

### Pre-processing Steps
- **Auto-Orientation**: Auto-Orient: Applied
- **Image Resize**: Resize: Stretch to 320x320 pixels.
- **Image Augmentations**:
  - Outputs per training example: 2
  - **Flip**: Vertical
  - **Rotation**: Between -25° and +25°
  - **Grayscale**: Apply to 25% of images
  - **Saturation**: Between -25% and +25%
  - **Brightness**: Between -25% and +25%
  - **Exposure**: Between -25% and +25%

### Additional Test Data
- **Title**: 3D Printing Errors Dataset
- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/mikulhe/3d-printing-errors)
- **Description**: This dataset is used for testing with a different distribution of 3D printing errors.
- **Data Path**: `Auto-ZMJ2N/test`

---

### 3D Printing Errors Dataset
- **Title**: 3D Printing Errors Dataset
- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/mikulhe/3d-printing-errors)
- **Description**: This dataset is used for testing with a different distribution of 3D printing errors.

### Dataset Overview
- **Total Images**: 9,046
- **Annotations**: Multi-Class Classification format for Void, Overheating, Stringing, and Gaps.

### Pre-processing Steps
- **Auto-Orientation**: Pixel data auto-oriented with EXIF-orientation stripping.
- **Image Resize**: Resized to 640x640 pixels (Stretch).
- **Image Augmentation**: No image augmentation techniques were applied.

### Additional Resource
- **3D Printing CM**: [Link to Dataset](https://universe.roboflow.com/arizonastateuniversity/3d-printing-cm)

## Generalisable 3D Printing Error Detection and Correction Dataset

- **Title**: Generalisable 3D Printing Error Detection and Correction via Multi-Head Neural Networks
- **Authors**: Douglas Brion, Sebastian Pattinson
- **Repository URI**: [Cambridge Repository](https://www.repository.cam.ac.uk/handle/1810/339869)
- **Repository DOI**: [10.17863/CAM.84082](https://doi.org/10.17863/CAM.84082)
- **License**: Attribution 4.0 International (CC BY 4.0)

### Dataset Overview
This dataset contains **1,272,273** labelled images of the extrusion 3D printing process. It was collected using a camera mounted next to the nozzle of the printer, capturing images of material deposition for **192 different printed parts** across various geometries, material colors, and lighting conditions.

### Key Features
- **Labels**: Each image is labelled with:
  - Flow rate
  - Lateral speed
  - Z offset
  - Hotend temperature
  - Hotend target temperature
  - Bed temperature
  - Timestamp
  - Nozzle tip x and y coordinates

- **Filtered Dataset**: A CSV file containing **948,396** pre-filtered images is provided, where complete failures, parameter outliers, dark images, and images taken immediately after parameter changes have been removed.

### Data Collection
The data was generated on printers running Marlin 1.1.9 firmware and collected on a Python 3 server. Python was also used for sampling parameter combinations and cleaning/filtering the dataset after collection.

## Data Sources
1. **3D Printer Defected Dataset**
   - **Link**: [3D Printer Defected Dataset](https://www.kaggle.com/datasets/justin900429/3d-printer-defected-dataset/data)

2. **Early Detection of 3D Printing Issues**
   - **Link**: [Early Detection of 3D Printing Issues Dataset](https://www.kaggle.com/competitions/early-detection-of-3d-printing-issues/data)
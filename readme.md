# Image Processing GUI

## 📌 Project Description
This **Image Processing GUI** allows users to apply various image processing techniques using **OpenCV** and **Tkinter**. Users can load an image, apply transformations, and view the processed output.

## 🎥 Video Demonstration
 
https://github.com/user-attachments/assets/ca042884-0f1d-451f-bcf4-3738dc5373d9


## 🚀 Features
- **Load & Display Image**
- **Grayscale Conversion**
- **HSV & HSL Color Space Conversion**
- **Binarization with Adjustable Threshold**
- **Image Translation & Rotation**
- **Mean & Gaussian Filtering**
- **Canny Edge Detection**
- **Intensity Range Reduction**
- **Histogram Equalization**
- **Batch Image Processing & Auto-Saving**

## 📂 Folder Structure
```
📦 ImageProcessingGUI
 ┣ 📜 README.md
 ┣ 📜 requirements.txt
 ┣ 📜 .gitignore
 ┣ 📜 assignment1.py
 ┣ 📜 filesaver.py
 ┣ 📜 report.docx
 ┣ 📜 Neelash's Machine Vision Assignment.pdf
 ┣ 📂 images/output_images

```

## 🛠️ Installation

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/neelashkannan/Machine-Vision-Assignment-1.git
cd Machine-Vision-Assignment-1
```

### 2️⃣ **Create a Virtual Environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Run the Application**
```bash
python main.py
```

---

## 🎮 Usage
1. Click **"Upload Image"** to select an image.
2. Choose a **task** from the dropdown menu.
3. Adjust the **threshold** or **kernel size** (if required).
4. Click **"Process"** to apply the transformation.
5. The processed image will be displayed alongside the original.

---

## 🔧 Batch Processing & Auto-Saving (FileSaver)
This GUI also supports **batch processing and automatic image saving** based on different threshold values and kernel sizes. The `FileSaver` functionality includes:
- **Binarization:** Saves images for **thresholds from 1 to 255**.
- **Mean Filter:** Saves filtered images for **kernel sizes 1x1 to 25x25**.
- **Gaussian Filter:** Saves filtered images for **odd kernel sizes 1x1 to 25x25**.
- **Canny Edge Detection:** Saves edge-detected images for **thresholds 1 to 255**.
- **Reduced Intensity:** Saves images for intensity ranges **from 255 to 8**.
- **Histogram Equalization:** Saves a histogram-equalized version of the image.

All processed images are **automatically saved** inside the `images/` folder and are renamed as `output images` for easy tracking.

---

## 🔧 Dependencies
This project requires **Python 3.x** and the following libraries:
- `opencv-python`
- `numpy`
- `Pillow`
- `tkinter`

To install all dependencies, run:
```bash
pip install -r requirements.txt
```

---

## 👤 Author
**Neelash Kannan Annadurai**  
📧 Email: neelashkannan@outlook.com

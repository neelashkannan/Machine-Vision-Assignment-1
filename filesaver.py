import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
import os
from PIL import Image, ImageTk
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing & Saving")
        self.root.geometry("700x500")

        self.image_path = None
        self.original_image = None
        self.setup_ui()

    def setup_ui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        upload_button = tk.Button(frame_top, text="Upload Image", command=self.upload_image)
        upload_button.pack(side=tk.LEFT, padx=5)

        self.file_label = tk.Label(frame_top, text="No file selected", fg="grey")
        self.file_label.pack(side=tk.LEFT, padx=5)

        frame_middle = tk.Frame(self.root)
        frame_middle.pack(pady=10)

        tk.Label(frame_middle, text="Choose Task:").pack(side=tk.LEFT, padx=5)

        self.task_var = tk.StringVar()
        self.task_dropdown = ttk.Combobox(frame_middle, textvariable=self.task_var, state="readonly")
        self.task_dropdown['values'] = (
            "Binarization (Thresholding)",
            "Mean Filter",
            "Gaussian Filter",
            "Canny Edge Detection",
            "Convert to Grayscale",
            "Reduce Intensity Range",
            "Histogram Equalization"
        )
        self.task_dropdown.pack(side=tk.LEFT, padx=5)

        process_button = tk.Button(frame_middle, text="Save Images", command=self.save_images)
        process_button.pack(side=tk.LEFT, padx=5)

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill=tk.BOTH, expand=True, pady=10)

        self.canvas_original = tk.Canvas(frame_bottom, width=300, height=300, bg="white")
        self.canvas_original.pack(side=tk.LEFT, padx=10, pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.file_label.config(text=self.image_path)
            self.original_image = cv2.imread(self.image_path)
            self.display_image(self.original_image, self.canvas_original)

    def save_images(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        task = self.task_var.get()
        if not task:
            messagebox.showerror("Error", "Please select a task!")
            return

        if task == "Binarization (Thresholding)":
            self.save_binarized()
        elif task == "Mean Filter":
            self.save_mean_filter()
        elif task == "Gaussian Filter":
            self.save_gaussian_filter()
        elif task == "Canny Edge Detection":
            self.save_canny_edges()
        elif task == "Convert to Grayscale":
            self.save_grayscale()
        elif task == "Reduce Intensity Range":
            self.save_reduced_intensity()
        elif task == "Histogram Equalization":
            self.save_histogram_equalization()

    def save_binarized(self):
        """ Saves binarized images for thresholds 1 to 255. """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Binarized"
        os.makedirs(save_folder, exist_ok=True)

        for threshold in range(1, 256, 1):  # Every 10 steps
            _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"{save_folder}/{threshold}.png", binary)

        messagebox.showinfo("Success", f"Binarized images saved in '{save_folder}'!")

    def save_mean_filter(self):
        """ Saves Mean Filter results for kernel sizes 1x1 to 25x25. """
        #gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Mean_Filter"
        os.makedirs(save_folder, exist_ok=True)

        for k in range(1, 26, 1):  # Odd-sized kernels only
            mean_filtered = cv2.blur(self.original_image, (k, k))
            cv2.imwrite(f"{save_folder}/{k}x{k}.png", mean_filtered)

        messagebox.showinfo("Success", f"Mean filter images saved in '{save_folder}'!")

    def save_gaussian_filter(self):
        """ Saves Gaussian Filter results for kernel sizes 1x1 to 25x25. """
        #gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Gaussian_Filter"
        os.makedirs(save_folder, exist_ok=True)

        for k in range(1, 26, 2):  # Odd-sized kernels only
            gaussian_filtered = cv2.GaussianBlur(self.original_image, (k, k), 0)
            cv2.imwrite(f"{save_folder}/{k}x{k}.png", gaussian_filtered)

        messagebox.showinfo("Success", f"Gaussian filter images saved in '{save_folder}'!")

    def save_canny_edges(self):
        """ Saves Canny edge detection results for thresholds 1 to 255. """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Canny_Edge"
        os.makedirs(save_folder, exist_ok=True)

        for t in range(0, 256, 1):  # Every 10 steps
            edges = cv2.Canny(gray, t, t * 2)
            cv2.imwrite(f"{save_folder}/{t}.png", edges)

        messagebox.showinfo("Success", f"Canny edge images saved in '{save_folder}'!")

    def save_grayscale(self):
        """ Converts to grayscale and saves the full intensity grayscale image. """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Grayscale"
        os.makedirs(save_folder, exist_ok=True)
        cv2.imwrite(f"{save_folder}/Grayscale.png", gray)

        messagebox.showinfo("Success", f"Grayscale image saved in '{save_folder}'!")

    def save_reduced_intensity(self):
        """ Reduces intensity range from 255 to 8 and saves each image. """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        save_folder = "Saved_Images/Reduced_Intensity"
        os.makedirs(save_folder, exist_ok=True)

        for N in range(255, 7, -1):  # Save images for N = 255, 239, 223, ..., 8
            reduced_intensity = ((gray / 255) * N).astype('uint8')
            cv2.imwrite(f"{save_folder}/{N}.png", reduced_intensity)

        messagebox.showinfo("Success", f"Reduced intensity images saved in '{save_folder}'!")

    def save_histogram_equalization(self):
        """ Applies histogram equalization and saves the image. """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        save_folder = "Saved_Images/Histogram_Equalization"
        os.makedirs(save_folder, exist_ok=True)
        cv2.imwrite(f"{save_folder}/Histogram_Equalized.png", equalized)

        messagebox.showinfo("Success", f"Histogram equalized image saved in '{save_folder}'!")

    def display_image(self, img, canvas):
        """ Displays an image on the given canvas. """
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        # Set window size to 550x450
        self.root.title("Image Processing GUI")
        self.root.geometry("550x450")

        self.image_path = None
        self.original_image = None
        self.processed_image = None

        self.setup_ui()

    def setup_ui(self):
        # Frame for file upload
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=5)

        upload_button = tk.Button(frame_top, text="Upload Image", command=self.upload_image)
        upload_button.pack(side=tk.LEFT, padx=5)

        self.file_label = tk.Label(frame_top, text="No file selected", fg="grey")
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Frame for controls
        frame_middle = tk.Frame(self.root)
        frame_middle.pack(pady=5)

        tk.Label(frame_middle, text="Choose Task:").pack(side=tk.LEFT, padx=5)

        self.task_var = tk.StringVar()
        task_dropdown = ttk.Combobox(frame_middle, textvariable=self.task_var, state="readonly")
        task_dropdown['values'] = (
            "Q1.1: Load and Display Image",
            "Q1.2: Convert to Grayscale",
            "Q1.2.1: HSV Conversion",
            "Q1.2.2: HSL Conversion",
            "Q1.3: Binarize Image",
            "Q2.1: Translate Image",
            "Q2.2: Rotate Image",
            "Q3.1: Mean Filter",
            "Q3.2: Gaussian Filter",
            "Q3.3: Canny Edge Detection",
            "Q4.3: Reduce Intensity Range",
            "Q4.4: Histogram Equalization",
        )
        task_dropdown.bind("<<ComboboxSelected>>", self.on_task_change)
        task_dropdown.pack(side=tk.LEFT, padx=5)

        process_button = tk.Button(frame_middle, text="Process", command=self.process_task)
        process_button.pack(side=tk.LEFT, padx=5)

        # Slider for threshold control (for tasks that need it)
        self.threshold_label = tk.Label(frame_middle, text="Threshold:")
        self.threshold_var = tk.IntVar(value=128)
        self.threshold_slider = tk.Scale(frame_middle, from_=0, to=255, orient=tk.HORIZONTAL,
                                         variable=self.threshold_var, command=self.update_threshold)

        # Slider for kernel size control (for filtering tasks)
        self.kernel_label = tk.Label(frame_middle, text="Kernel Size:")
        self.kernel_var = tk.IntVar(value=5)
        self.kernel_slider = tk.Scale(frame_middle, from_=3, to=31, orient=tk.HORIZONTAL,
                                      variable=self.kernel_var, command=self.update_threshold)

        # Initially hide extra sliders
        self.threshold_label.pack_forget()
        self.threshold_slider.pack_forget()
        self.kernel_label.pack_forget()
        self.kernel_slider.pack_forget()

        # Frame for displaying images
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill=tk.BOTH, expand=True, pady=5)

        # Left frame: original image canvas and image info label below it.
        left_frame = tk.Frame(frame_bottom)
        left_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.canvas_original = tk.Canvas(left_frame, width=250, height=250, bg="white")
        self.canvas_original.pack()
        
        # Label for displaying image information below the original image
        self.image_info_label = tk.Label(left_frame, text="", fg="blue")
        self.image_info_label.pack()

        # Right canvas for the processed image.
        self.canvas_processed = tk.Canvas(frame_bottom, width=250, height=250, bg="white")
        self.canvas_processed.pack(side=tk.LEFT, padx=5, pady=5)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.file_label.config(text=self.image_path)
            self.original_image = cv2.imread(self.image_path)
            if self.original_image is None:
                messagebox.showerror("Error", "Failed to load image!")
                return
            self.display_image(self.original_image, self.canvas_original)
            height, width, channels = self.original_image.shape
            image_details = f"Width: {width}, Height: {height}, Channels: {channels}"
            # Display image details below the left canvas.
            self.image_info_label.config(text=image_details)

    def on_task_change(self, _):
        # Hide all extra sliders initially
        self.threshold_label.pack_forget()
        self.threshold_slider.pack_forget()
        self.kernel_label.pack_forget()
        self.kernel_slider.pack_forget()

        task = self.task_var.get()
        if task in ["Q1.3: Binarize Image", "Q3.3: Canny Edge Detection", "Q4.3: Reduce Intensity Range"]:
            self.threshold_label.pack(side=tk.LEFT, padx=5)
            self.threshold_slider.pack(side=tk.LEFT, padx=5)
        elif task in ["Q3.1: Mean Filter", "Q3.2: Gaussian Filter"]:
            self.kernel_label.pack(side=tk.LEFT, padx=5)
            self.kernel_slider.pack(side=tk.LEFT, padx=5)
        # For HSV and HSL conversion, no extra parameter sliders are shown.

    def process_task(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        # Use the already loaded image for processing.
        fresh_image = self.original_image.copy()
        task = self.task_var.get()
        threshold = self.threshold_var.get()
        kernel_size = self.kernel_var.get()

        if kernel_size % 2 == 0:
            kernel_size += 1

        if task == "Q1.1: Load and Display Image":
            self.processed_image = fresh_image

        elif task == "Q1.2: Convert to Grayscale":
            gray = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = gray

        elif task == "Q1.3: Binarize Image":
            gray = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            self.processed_image = binary

        elif task == "Q2.1: Translate Image":
            rows, cols = fresh_image.shape[:2]
            translation_matrix = np.float32([[1, 0, 50], [0, 1, 30]])
            self.processed_image = cv2.warpAffine(fresh_image, translation_matrix, (cols, rows))

        elif task == "Q2.2: Rotate Image":
            rows, cols = fresh_image.shape[:2]
            center = (cols // 2, rows // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1)
            self.processed_image = cv2.warpAffine(fresh_image, rotation_matrix, (cols, rows))

        elif task == "Q3.1: Mean Filter":
            self.processed_image = cv2.blur(fresh_image, (kernel_size, kernel_size))

        elif task == "Q3.2: Gaussian Filter":
            self.processed_image = cv2.GaussianBlur(fresh_image, (kernel_size, kernel_size), 0)

        elif task == "Q3.3: Canny Edge Detection":
            gray = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.Canny(gray, threshold, threshold * 2)

        elif task == "Q4.3: Reduce Intensity Range":
            self.processed_image = (fresh_image * (threshold / 255)).astype('uint8')

        elif task == "Q4.4: Histogram Equalization":
            gray = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.equalizeHist(gray)

        elif task == "Q1.2.1: HSV Conversion":
            hsv = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            h = (h.astype(np.int32) + 10) % 180
            h = h.astype(np.uint8)
            s = cv2.add(s, 30)
            hsv_modified = cv2.merge([h, s, v])
            reddish = cv2.cvtColor(hsv_modified, cv2.COLOR_HSV2BGR)
            self.processed_image = reddish

        elif task == "Q1.2.2: HSL Conversion":
            hls = cv2.cvtColor(fresh_image, cv2.COLOR_BGR2HLS)
            h, l, s = cv2.split(hls)
            h = (h.astype(np.int32) + 10) % 180
            h = h.astype(np.uint8)
            s = cv2.add(s, 30)
            hls_modified = cv2.merge([h, l, s])
            reddish = cv2.cvtColor(hls_modified, cv2.COLOR_HLS2BGR)
            self.processed_image = reddish

        self.display_image(self.processed_image, self.canvas_processed)

    def update_threshold(self, _):
        if self.original_image is None:
            return
        self.process_task()

    def display_image(self, img, canvas):
        if img is None:
            messagebox.showerror("Error", "No image data to display!")
            return
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        max_width, max_height = 250, 250
        orig_width, orig_height = img.size
        ratio = min(max_width / orig_width, max_height / orig_height)
        new_size = (int(orig_width * ratio), int(orig_height * ratio))
        img = img.resize(new_size)
        canvas.config(width=new_size[0], height=new_size[1])
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

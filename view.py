import os
import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root, image_folder):
        self.root = root
        self.root.title("Image Viewer")

        # Get list of image files
        self.image_files = self.get_image_files(image_folder)
        if not self.image_files:
            label = tk.Label(root, text=f"No images found in {image_folder}")
            label.pack(padx=20, pady=20)
            return

        # Set up variables
        self.current_index = 0

        # Create canvas for displaying images
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create status bar
        self.status = tk.Label(
            root,
            text="Use Right Arrow → for next image | Left Arrow ← for previous image",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind keyboard events
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.prev_image)

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

        # Load and display the first image
        self.display_image()

    def get_image_files(self, folder):
        """Get a list of image files from the specified folder"""
        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
        image_files = []

        # Check if the folder exists
        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            return image_files

        # Get all image files from the folder
        for file in os.listdir(folder):
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(folder, file))

        return sorted(image_files)

    def display_image(self):
        """Display the current image"""
        if not self.image_files:
            return

        # Clear previous image
        self.canvas.delete("all")

        # Load and display the current image
        img_path = self.image_files[self.current_index]
        self.original_img = Image.open(img_path)

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Initial window might be very small, set reasonable defaults
        if canvas_width < 100:
            canvas_width = 800
        if canvas_height < 100:
            canvas_height = 600

        img = self.resize_to_fit(self.original_img, canvas_width, canvas_height)

        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(
            canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=self.photo
        )

        # Update status bar with image info
        filename = os.path.basename(img_path)
        self.status.config(
            text=f"{filename} ({self.current_index + 1}/{len(self.image_files)}) | Use Right Arrow → for next image"
        )

    def resize_to_fit(self, img, canvas_width, canvas_height):
        """Resize image to fit within the canvas while maintaining aspect ratio"""
        width, height = img.size

        # Calculate scaling factors
        width_factor = canvas_width / width
        height_factor = canvas_height / height
        factor = min(width_factor, height_factor)

        # Only resize if image is larger than canvas
        if factor < 1:
            new_width = int(width * factor)
            new_height = int(height * factor)
            return img.resize((new_width, new_height), Image.LANCZOS)

        return img

    def on_resize(self, event):
        """Handle window resize events"""
        # Only respond to main window resize, not internal events
        if event.widget == self.root and self.image_files:
            # Add a small delay to avoid excessive redraws
            self.root.after(100, self.display_image)

    def next_image(self, event=None):
        """Show the next image"""
        if not self.image_files:
            return

        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.display_image()

    def prev_image(self, event=None):
        """Show the previous image"""
        if not self.image_files:
            return

        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.display_image()


def main():
    # Specify the folder containing images
    image_folder = "images_detected"

    # Create and set up the main window
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Image Viewer")

    # Create the image viewer
    viewer = ImageViewer(root, image_folder)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()

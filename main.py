import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Global variables to store the paths of the images
image_path = ""
logo_path = ""


# Function to upload an image
def upload_img():
    global image_path, image_display
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if image_path:
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        image_display.config(image=img)
        image_display.image = img
        messagebox.showinfo("Success", "Image uploaded successfully!")
    else:
        messagebox.showwarning("Error", "No image selected.")


# Function to add text watermark to the image
def add_text_watermark():
    global image_path
    if image_path:
        # Load the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Validate font size input
        try:
            font_size = int(font_size_entry.get())
            if font_size <= 0:
                raise ValueError("Font size must be a positive integer.")
        except ValueError as e:
            messagebox.showwarning("Invalid Input", str(e))
            return

            # Set custom font and size
        font = ImageFont.truetype("arial.ttf", font_size)

        # Get the watermark text
        text = watermark_text_entry.get().strip()
        if not text:
            messagebox.showwarning("Invalid Input", "Watermark text cannot be empty.")
            return

            # Calculate text size and position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        width, height = img.size
        position = (width - text_width - 10, height - text_height - 10)

        # Add watermark text
        draw.text(position, text, (255, 255, 255), font=font)

        # Display watermarked image
        img.show()
        img.save("watermarked_image.png")
        messagebox.showinfo("Success", "Text watermark added successfully!")

    else:
        messagebox.showwarning("Error", "Please upload an image first.")


def upload_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if logo_path:
        messagebox.showinfo("Success", "Logo uploaded successfully!")
    else:
        messagebox.showwarning("Error", "No logo selected.")


# Function to add a logo watermark
def add_logo_watermark():
    global image_path, logo_path
    if image_path and logo_path:
        try:
            img = Image.open(image_path).convert("RGBA")
            logo = Image.open(logo_path).convert("RGBA")

            # Validate logo size inputs
            try:
                logo_width = int(logo_width_entry.get())
                logo_height = int(logo_height_entry.get())

                if logo_width <= 0 or logo_height <= 0:
                    raise ValueError("Logo width and height must be positive integers.")
            except ValueError as e:
                messagebox.showwarning("Invalid Input", str(e))
                return

            # Resize logo based on user input
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            # Calculate position for the logo
            width, height = img.size
            logo_width, logo_height = logo.size
            position = (width - logo_width - 10, height - logo_height - 10)  # Bottom right corner

            # Paste the logo onto the image with transparency mask
            img.paste(logo, position, logo)

            # Display watermarked image
            img.show()
            img.save("watermarked_image_with_logo.png")  # Save the image
            messagebox.showinfo("Success", "Logo watermark added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    else:
        messagebox.showwarning("Error", "Please upload an image and a logo first.")


# Create GUI SETUP-------------------------------------------------------------------------

# Creating window
window = tk.Tk()
window.title("Image Watermarking Application")
window.geometry("600x500")
window.config(bg="#f0f0f0")

# Title label
title_label = tk.Label(window, text="Image Watermarking Application", font=("Helvetica", 18, "bold"), bg="#4682B4",
                       fg="white")
title_label.pack(fill=tk.X, pady=10)

# Image display area
image_display = tk.Label(window, bg="white", width=50, height=20, relief=tk.SUNKEN)
image_display.pack(pady=10)

# Frame for watermark options
watermark_frame = tk.Frame(window, bg="#f0f0f0")
watermark_frame.pack(pady=10)

# Watermark text entry
watermark_text_label = tk.Label(watermark_frame, text="Watermark Text:", font=("Arial", 12), bg="#f0f0f0")
watermark_text_label.pack(side=tk.LEFT, padx=10, pady=5)
watermark_text_entry = tk.Entry(watermark_frame, width=30, font=("Arial", 12))
watermark_text_entry.pack(side=tk.LEFT, padx=10, pady=5)

# Font size entry
font_size_label = tk.Label(watermark_frame, text="Font Size:", font=("Arial", 12), bg="#f0f0f0")
font_size_label.pack(side=tk.LEFT, padx=10, pady=5)
font_size_entry = tk.Entry(watermark_frame, width=10, font=("Arial", 12))
font_size_entry.insert(0, "36")  # Default font size
font_size_entry.pack(side=tk.LEFT, padx=10, pady=5)

# Frame for logo size options
logo_size_frame = tk.Frame(window, bg="#f0f0f0")
logo_size_frame.pack(pady=10)

# Logo width entry
logo_width_label = tk.Label(logo_size_frame, text="Logo Width:", font=("Arial", 12), bg="#f0f0f0")
logo_width_label.pack(side=tk.LEFT, padx=10, pady=5)
logo_width_entry = tk.Entry(logo_size_frame, width=5, font=("Arial", 12))
logo_width_entry.insert(0, "100")  # Default width
logo_width_entry.pack(side=tk.LEFT, padx=10, pady=5)

# Logo height entry
logo_height_label = tk.Label(logo_size_frame, text="Logo Height:", font=("Arial", 12), bg="#f0f0f0")
logo_height_label.pack(side=tk.LEFT, padx=10, pady=5)
logo_height_entry = tk.Entry(logo_size_frame, width=5, font=("Arial", 12))
logo_height_entry.insert(0, "100")  # Default height
logo_height_entry.pack(side=tk.LEFT, padx=10, pady=5)

# Frame for buttons
button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.pack(pady=10)

# Buttons for Upload and Add Watermark
upload_button = tk.Button(button_frame, text="Upload Image", command=upload_img, font=("Arial", 12, "bold"),
                          bg="#4682B4", fg="white", padx=10, pady=5)
upload_button.pack(side=tk.LEFT, padx=10)

watermark_button = tk.Button(button_frame, text="Add Text Watermark", command=add_text_watermark,
                             font=("Arial", 12, "bold"), bg="#4682B4", fg="white", padx=10, pady=5)
watermark_button.pack(side=tk.LEFT, padx=10)

# Button for Upload Logo
upload_logo_button = tk.Button(button_frame, text="Upload Logo", command=upload_logo, font=("Arial", 12, "bold"),
                               bg="#4682B4", fg="white", padx=10, pady=5)
upload_logo_button.pack(side=tk.LEFT, padx=10)

logo_watermark_button = tk.Button(button_frame, text="Add Logo Watermark", command=add_logo_watermark,
                                  font=("Arial", 12, "bold"), bg="#4682B4", fg="white", padx=10, pady=5)
logo_watermark_button.pack(side=tk.LEFT, padx=10)

# Footer label
footer_label = tk.Label(window, text="Created by Prathamesh", font=("Helvetica", 10, "italic"), bg="#f0f0f0", fg="gray")
footer_label.pack(side=tk.BOTTOM, pady=10)

window.mainloop()

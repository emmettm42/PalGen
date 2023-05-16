import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
from color_palette import generate_palette, export_palette

# Set the number of colors in the palette
NUM_COLORS = 9

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Select input files button
        self.input_button = tk.Button(self)
        self.input_button["text"] = "Select input files"
        self.input_button["command"] = self.select_input_files
        self.input_button.pack(side="top")

        # Select output directory button
        self.output_button = tk.Button(self)
        self.output_button["text"] = "Select output directory"
        self.output_button["command"] = self.select_output_directory
        self.output_button.pack(side="top")

        # Export palette button
        self.export_button = tk.Button(self)
        self.export_button["text"] = "Export palettes"
        self.export_button["state"] = "disabled"
        self.export_button["command"] = self.export_palettes
        self.export_button.pack(side="top")

    def select_input_files(self):
        # Show file dialog to select input files
        self.input_files = filedialog.askopenfilenames(
            title="Select input files",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("SVG", "*.svg")],
        )

        # Enable export palette button if input files are selected
        if self.input_files:
            self.export_button["state"] = "normal"

    def select_output_directory(self):
        # Show file dialog to select output directory
        self.output_directory = filedialog.askdirectory(title="Select output directory")

    def export_palettes(self):
        # Loop over input files and generate/export palettes
        for input_file in self.input_files:
            # Generate the palette
            palette = generate_palette(input_file)

            # Get the output file paths
            input_filename = os.path.splitext(os.path.basename(input_file))[0]
            txt_output_path = os.path.join(self.output_directory, input_filename + ".txt")
            csv_output_path = os.path.join(self.output_directory, input_filename + ".csv")
            json_output_path = os.path.join(self.output_directory, input_filename + ".json")
            png_output_path = os.path.join(self.output_directory, input_filename + "_palgen.png")

            # Create the output directory if it doesn't exist
            os.makedirs(self.output_directory, exist_ok=True)

            # Export the palette to txt, csv, and json
            export_palette(palette, txt_output_path)
            #export_palette(palette, csv_output_path, format="csv")
            #export_palette(palette, json_output_path, format="json")

            # Create an image of the palette and the original image
            image = Image.open(input_file)
            palette_image = Image.new("RGB", (256, 128), color="white")
            draw = ImageDraw.Draw(palette_image)

            # Draw the color palette in a 3x3 matrix on the left side of the image
            palette_size = 39
            margin = 2
            for i, color in enumerate(palette):
                x = margin + (i % 3) * (palette_size + margin)
                y = margin + (i // 3) * (palette_size + margin)
                draw.rectangle((x, y, x + palette_size, y + palette_size), fill=color, outline="black")

            # Resize and paste the original image on the right side of the image
            image.thumbnail((128, 128))
            palette_image.paste(image, (128, 0))

            # Save the palette image
            palette_image.save(png_output_path)

        # Show confirmation message
        tk.messagebox.showinfo("Export complete", f"{len(self.input_files)} palettes exported to {self.output_directory}")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
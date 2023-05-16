import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# Set the number of colors in the palette
NUM_COLORS = 9

def generate_palette(image_path):
    # Open the image file
    im = Image.open(image_path)

    # Convert the image to a numpy array
    im_arr = np.array(im)

    # Reshape the array to a 2D array of pixels
    pixels = im_arr.reshape((-1, im_arr.shape[-1]))

    # Use K-Means clustering to group similar colors
    kmeans = KMeans(n_clusters=NUM_COLORS)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    # Convert the colors to hexadecimal RGB values
    palette_hex = [f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}" for c in colors]

    return palette_hex

def export_palette(palette, output_path):
    # Write the palette to a text file
    with open(output_path, "w") as f:
        f.write("\n".join(palette))

# Example usage
#if __name__ == "__main__":
#    # Path to the input image file
#    image_path = "./image.jpg"
#
#    # Generate the palette
#    palette = generate_palette(image_path)
#
#    # Path to the output text file
#    output_path = "./palette1.txt"
#
#    # Export the palette
#    export_palette(palette, output_path)
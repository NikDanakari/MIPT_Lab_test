import numpy as np
from PIL import Image


# function that converts CSV file into PIL image
def csv_to_image(filepath):
    f = open(filepath, "r")
    header = f.readlines(1)[0] # label determining rgb/grayscale
    raw_data = np.genfromtxt(filepath, delimiter=';', dtype=np.uint32) # read data to NumPy array
    if np.isnan(raw_data).all():
        return "You have chosen an incorrect CSV file"
    if header.find('# rgb') != -1:
         # Split the 24-bit decimal numbers into RGB values
         r = (raw_data >> 16) & 0xFF
         g = (raw_data >> 8) & 0xFF
         b = raw_data & 0xFF
         # Combine the RGB values into a single array
         rgb_array = np.dstack((r, g, b))
         image = Image.fromarray(rgb_array.astype(np.uint8)).convert("RGB") # create RGB image
         
    else:
        image = Image.fromarray(raw_data).convert("L") # create grayscale image
    return image

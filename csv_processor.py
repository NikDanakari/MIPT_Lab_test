import numpy as np
from PIL import Image, ImageQt
# function that converts CSV file into PIL image
def csv_to_image(filepath):
    raw_data = np.genfromtxt(filepath, delimiter=';') # read data to NumPy array
    if np.isnan(raw_data).all():
         return "You have chosen incorrect CSV file"
    image = Image.fromarray(raw_data) # create an image from NumPy array using PIL.Image method
    # converts image to view it correctly (neccessary for grayscale images)
    if image.mode != "L":
         image = image.convert("L")
    return image

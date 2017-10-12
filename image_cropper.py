'''
Purpose of Code:
    Given a directory that contains image files, this library should iterate through said directory
    and convert the image files into numPy arrays.
    The numPy arrays (as of 10/9/2017) are saved in the same directory as the image files and are
    distinguihed with the tag "-array" at the end of the filename.
    Through this library, pre-processing images for the purpose of creating homogenized training
    and testing data will be standardized.
'''
import os
import sys
from PIL import Image
from PIL import ImageFilter
import numpy as np


def load_image(fname):
    '''Using a string to represent the filename, load_image attempts to create an Image object and
    open the file. If it fails (regardless of why), it will return an error and return.'''
    try:
        img = Image.open(fname)  #String refers to filename
        return img
    except FileNotFoundError:
        print("Unable to load image: " + fname + "\n")
    return


def center_crop(img, height, width):
    '''Given an image object and its desired height and width, it crops from the center of the
    image such that the resulting dimensions are the desired height and width.'''
    center_w = img.size[0] / 2
    center_h = img.size[1] / 2
    buffer_width = width / 2
    buffer_height = height / 2
    cropped_image = img.crop(
        (center_w - buffer_width, center_h - buffer_height,
         center_w + buffer_width, center_h + buffer_height))
    return cropped_image


def pad_image(img, height, width):
    '''Given an image object and its desired height and width, it pads from the center of the image
     such that the resulting dimensions are the desired height and width.'''

    image_width = img.size[0]
    image_height = img.size[1]
    if image_width < width:
        difference_width = width - image_width
        horizontal_padding = difference_width / 2
    if image_height < height:
        difference_height = height - image_height
        vertical_padding = difference_height / 2
    padded_image = img.crop(
        (-horizontal_padding, -vertical_padding,
         image_width + horizontal_padding, image_height + vertical_padding))
    return padded_image


def rotate_image(img, deg=0):
    '''Given an image object and an integer x for degrees,
     the image is rotated counter-clockwise x degrees.'''
    rotated_image = img.rotate(deg)  #This rotates counter-clockwise
    return rotated_image


def blur_image(img):
    '''Given an image object, a predefined blur function is applied onto it.'''
    blurred_image = img.filter(
        ImageFilter.BLUR
    )  # This blur is predefined; May need to create separate function
    return blurred_image


def image_to_np_array(image):
    '''Takes an image object and transforms it into a numPy array and outputs the array.'''
    data = np.asarray(image)
    print(data.shape)
    return data


def np_array_to_img(nparray):
    '''Takes a numPy array and transforms it into an image, returning said image.'''
    image = Image.fromarray(nparray)
    return image


def save_image(npdata, outfilename):
    '''Saves the image (transformed into a nuPy array) with the filename outfilename'''
    np.save(outfilename, npdata)
    return


def load_ultrasound(img, size_height=0, size_width=0):
    '''loads an image, then crops it to the desired height and width, then transorms it into a
    numPy array and saves it to disk.'''
    image = load_image(img)
    image = center_crop(image, size_height, size_width)
    data = image_to_np_array(image)
    save_image(data, img + "-array")  #Change this to fit naming convention
    return


for directory_in_str in sys.argv[1:]:
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            load_ultrasound(filename, 500, 500)
        else:
            continue

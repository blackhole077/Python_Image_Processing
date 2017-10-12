'''
Purpose of Code:
    Given a directory that contains image files, this library should iterate through said directory and convert the image files into numPy arrays.
    The numPy arrays (as of 10/9/2017) are saved in the same directory as the image files and are distinguihed with the tag "-array" at the end of the filename.
    Through this library, pre-processing images for the purpose of creating homogenized training and testing data will be standardized.
'''
import PIL
from PIL import Image,ImageFilter
import os,sys,numpy as np
from pathlib import Path

'''
Using a string to represent the filename, load_image attempts to create an Image object and open the file. If it fails (regardless of why), it will return an error
and return.
'''
def load_image(str):
    try:
        img = Image.open(str)#String refers to filename
        return img
    except:
        print("Unable to load image\n")
    return
def center_crop(img, size, height, width): #The height, width arguments refer to the (resulting) dimensions of the cropped image.
    center_w = img.size[0]/2
    center_h = img.size[1]/2
    buffer_width = width/2
    buffer_height = height/2
    cropped_image = img.crop((center_w - buffer_width, center_h - buffer_height, center_w+buffer_width, center_h+buffer_height))
    return cropped_image

def rotate_image(img,deg):# Degree is assumed to be 0 by default
    rotated_image = img.rotate(deg)#This rotates counter-clockwise
    return rotated_image

def blur_image(img):
    blurred_image = img.filter(ImageFilter.BLUR)# This blur is predefined; May need to create separate function
    return blurred_image

def image_to_np_array( image ) :
    data = np.asarray(image)
    print(data.shape)
    return data

def np_array_to_img(nparray):
    image = Image.fromarray(nparray)
    return image

def save_image( npdata, outfilename ):
    np.save(outfilename,npdata)
    return

def load_ultrasound(img, size_height=img.size[0], size_width=img.size[1],degree=0):
    image = load_image(img)
    #print(image.format, image.size, image.mode)
    test_crop = center_crop(image,image.size,size_height,size_width)
    test_rotate = rotate_image(image,degree)
    #test_blur = blur_image(image)
    data = image_to_np_array(image)
    #print(data.shape)
    save_image(data, img+"-array")#Change this to fit naming convention
    return
#Figure out how to make a subdirectory (in Linux) and then how to save image files to that subdirectory
for directory_in_str in sys.argv[1:]:
    # destination_path =
    # destination_directory = os.path.dirname(destination_path)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # if not os.path.exists(directory):
    # os.makedirs(directory)
    #print(directory_in_str)
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            load_ultrasound(filename,500,500,15)
        else:
            continue
        #print ("The size of the cropped Image is: ")

#Converter should either return numPy array or save image to disk for testing purposes
#Take image that has been cropped/transformed to a numPy array
#Save numPy array to disk as .npy
#Focus on pixel-level dropout? (i.e. don't do white noise)

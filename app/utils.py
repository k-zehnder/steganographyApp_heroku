import imghdr
import os
import base64
import numpy as np
import cv2
import imutils
import types
from PIL import Image
from flask import current_app

project_root = os.path.dirname(os.path.dirname(__file__))
UPLOADS = os.path.join(project_root, "app", current_app.config['UPLOAD_PATH'])
DOWNLOADS = os.path.join(project_root, "app", current_app.config['DOWNLOAD_PATH'])
#print(f"TEST: {(UPLOADS, DOWNLOADS)}")

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def showData(image):

    binary_data = ""
    for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel) #convert the red,green and blue values into binary format
          binary_data += r[-1] #extracting data from the least significant bit of red pixel
          binary_data += g[-1] #extracting data from the least significant bit of red pixel
          binary_data += b[-1] #extracting data from the least significant bit of red pixel
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
          break
    #print(decoded_data)
    return decoded_data[:-5] #remove the delimeter to show the original hidden message

# Function to hide the secret message into the image
def hideData(image, secret_message):

    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode: " + str(n_bytes) + "\n")

    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
      raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!\n")

    secret_message += "#####" # you can use any string as the delimeter

    data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
    binary_secret_msg = messageToBinary(secret_message)

    data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
    for values in image:
      for pixel in values:
          # convert RGB values to binary format
          r, g, b = messageToBinary(pixel)
          # modify the least significant bit only if there is still data to store
          if data_index < data_len:
              # hide the data into least significant bit of red pixel
              pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of green pixel
              pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of  blue pixel
              pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          # if data is encoded, just break out of the loop
          if data_index >= data_len:
              break

    return image

def messageToBinary(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type is not supported\n")

def my_decode_text(filename):
    # write encoded image to disk
    if filename.startswith('encoded_'):
        encoded_filepath = filename
    else:
        encoded_filepath = 'encoded_' + filename

    image_with_message = cv2.imread(os.path.join(DOWNLOADS, encoded_filepath))
    print(f"Image with message filename = {encoded_filepath}")

    text = showData(image_with_message)
    return text

def encode_text(filename, message):
    originalImage = cv2.imread(os.path.join(UPLOADS, filename)).copy()
    processed_img = hideData(originalImage, message)

    # write encoded image to disk
    encoded_filepath = 'encoded_' + filename
    cv2.imwrite(os.path.join(DOWNLOADS, encoded_filepath), processed_img)

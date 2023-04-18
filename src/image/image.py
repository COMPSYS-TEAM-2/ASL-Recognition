import datetime
import os
from PIL import Image, ImageFilter
import numpy as np
from torch import FloatTensor
from PyQt6.QtGui import QImage


def prepareImage(image: QImage):
    # Converting image to MNIST dataset format
    image = image.convertToFormat(QImage.Format.Format_RGB32)
    height = image.height()
    width = image.width()
    pointer = image.constBits()
    pointer.setsize(height * width * 4)
    arr = np.frombuffer(pointer, np.uint8).reshape((height, width, 4))
    im = Image.fromarray(arr[..., 2::-1])
    im = im.convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    # creates white canvas of 28x28 pixels
    new_image = Image.new('L', (28, 28), (255))

    if width < height:
        # check which dimension is bigger
        # Width is smaller. Width becomes 28 pixels.
        # resize height according to ratio width and crop the edges
        nheight = int(round((28.0 / width * height), 0))
        # resize and sharpen
        img = im.resize((28, nheight), Image.ANTIALIAS).filter(
            ImageFilter.SHARPEN)
        # calculate vertical position
        wtop = int(round(((28 - nheight) / 2), 0))
        # paste resized image on white canvas
        new_image.paste(img, (0, wtop))
    else:
        # Height is smaller. Height becomes 28 pixels.
        # resize width according to ratio height and crop the tops and bottoms
        nwidth = int(round((28.0 / height * width), 0))
        # resize and sharpen
        img = im.resize((nwidth, 28), Image.ANTIALIAS).filter(
            ImageFilter.SHARPEN)
        # caculate horizontal pozition
        wleft = int(round(((28 - nwidth) / 2), 0))
        # paste resized image on white canvas
        new_image.paste(img, (wleft, 0))
    # Save the photo
    try:
        os.mkdir("./output")
    except:
        pass
    try:
        os.mkdir("./output/photos")
    except:
        pass
    new_image.save(
        f"./output/photos/{datetime.datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.png")
    pixels = list(new_image.getdata())  # get pixel values
    pixels_normalized = [x / 255.0 for x in pixels]
    # Return MNIST tensor
    return FloatTensor(pixels_normalized).view(1, 1, 28, 28)

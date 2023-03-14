from PIL import Image, ImageFilter
import numpy as np
from torch import FloatTensor


def prepare_image(path: str):
    # Converting image to MNIST dataset format

    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    # creates white canvas of 28x28 pixels
    new_image = Image.new('L', (28, 28), (255))

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        # resize height according to ratio width
        nheight = int(round((28.0 / width * height), 0))
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((28, nheight), Image.ANTIALIAS).filter(
            ImageFilter.SHARPEN)
        # calculate horizontal position
        wtop = int(round(((28 - nheight) / 2), 0))
        new_image.paste(img, (0, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        # resize width according to ratio height
        nwidth = int(round((28.0 / height * width), 0))
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 28), Image.ANTIALIAS).filter(
            ImageFilter.SHARPEN)
        # caculate vertical pozition
        wleft = int(round(((28 - nwidth) / 2), 0))
        new_image.paste(img, (wleft, 0))  # paste resized image on white canvas

    pixels = list(new_image.getdata())  # get pixel values
    pixels_normalized = [(255 - x) * 1.0 / 255.0 for x in pixels]

    return FloatTensor(pixels_normalized).view(1, 28, 28)

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The RX algorithm in Python 3.6+ for image data.
"""

from typing import Generator
from PIL import Image
from contextlib import contextmanager
from math import log2

import os
import numpy as np

REFERENCE_OUT_DIR = 'compression_data' + os.sep


@contextmanager
def getImage(pathToImage: str) -> Generator[np.ndarray, None, None]:
    """
    Open an image and `yield` it as a NumPy array.
    """

    # PIL.Image provides a CM as well; I'd like to wrap this so we don't have to
    # convert to a np.ndarray later (also helps simplify type annotations).
    with Image.open(pathToImage, mode='r') as image:
        # convert to ndarray
        im = np.array(image)

    yield im


def generateRandExtreme(X:int, Y: int, channels: int =3, format: str ='png') -> int:
    """
    Generate a random image for reference. The default is PNG because this image
    format provides a built-in DEFLATE compression (eliminating the need to perform
    our own compression). This function returns the size of the resulting
    compressed data.
    """
    name = f'random_{X}x{Y}.{format}'
    if name in os.listdir(REFERENCE_OUT_DIR):
        return os.path.getsize(REFERENCE_OUT_DIR + name)
    else:
        data = np.random.randint(0, 255, size=(Y,X,channels))
        to_save = Image.fromarray(data.astype(np.uint8))
        to_save.save(REFERENCE_OUT_DIR + name)
        return os.path.getsize(name)


def generateNullExtreme(X: int, Y: int, channels: int =3, format: str ='png') -> int:
    """
    Generate a null image for reference.
    """
    name = f'zeros_{X}x{Y}.{format}'
    if name in os.listdir(REFERENCE_OUT_DIR):
        return os.path.getsize(REFERENCE_OUT_DIR + name)
    else:
        data = np.zeros((Y,X,channels))
        to_save = Image.fromarray(data.astype(np.uint8))
        to_save.save(REFERENCE_OUT_DIR + name)
        return os.path.getsize(name)


def rx(imageName: str, sparse: bool =False) -> np.ndarray:
    """
    Compute the RX algorithm on an image. This function returns an array with one
    channel, which represents the number of standard deviations a certain pixel
    lies from the mean pixel value.

    Set `sparse' to true if you're expecting the image to be largely the same color,
    or, in other words, most of the pixels to be very similar (e.g. an image of a
    field looking down from a drone will be mostly green). This produces a time
    savings, since the variance-covariance matrix may be estimated from a random
    subset of the pixels.
    """
    with getImage(imageName) as imageArray:
        Y, X, channels = imageArray.shape

        if sparse:
            # Estimate entropy
            nullSize = generateNullExtreme(X, Y)
            randSize = generateRandExtreme(X, Y)
            dataSize = os.path.getsize(imageName)
            entropy = (dataSize - nullSize) / (randSize - nullSize) * X * Y
            print(entropy)
        else:
            # Use every pixel
            entropy = X * Y
            print(entropy)


if __name__ == '__main__':
    #print(generateNullExtreme(1333, 750))
    #print(generateRandomExtreme(1333, 750))
    #print(os.path.getsize(REFERENCE_OUT_DIR + os.sep + 'example_1MP.png'))
    rx('compression_data/example_1MP.png', sparse=True)

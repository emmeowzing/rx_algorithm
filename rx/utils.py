# coding=utf-8

"""
Additional utilities unrelated to the algorithm's implementation.
"""

from matplotlib import pyplot as plt

import numpy as np


def plot(image: np.ndarray, imageName: str) -> None:
    """
    Simply plot an image.

    If running tests, save to test image subdirectory.
    """
    plt.imshow(image, interpolation='none', cmap='gist_heat')
    plt.savefig(imageName)

"""
Additional utilities unrelated to the algorithm's implementation.
"""

from typing import Generator

from contextlib import contextmanager
from PIL import Image
from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

import numpy as np


def plot(image: np.ndarray, imageName: str) -> None:
    """
    Simply plot an image and save the figure (imshow) to `imageName`.

    If running tests, save to test image subdirectory.
    """
    plt.imshow(image, interpolation='none', cmap='gist_heat')
    plt.savefig(imageName)


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
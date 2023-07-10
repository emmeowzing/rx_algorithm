"""
The RX algorithm in Python 3.6+ for image data.
"""

from typing import Optional

from PIL import Image

import os
import numpy as np

# Directory for saving generated data
REFERENCE_OUT_DIR = 'compression_data' + os.sep

if not os.path.exists(REFERENCE_OUT_DIR):
    os.mkdir(REFERENCE_OUT_DIR)


def generateRandExtreme(X: int, Y: int, channels: int =3, format: str ='png') -> int:
    """
    Generate a random image for reference. The default is PNG because this image
    format provides a built-in DEFLATE compression (eliminating the need to perform
    our own compression). This function returns the size of the resulting
    compressed data.
    """
    name = f'random_{X}x{Y}.{format}'
    if name in os.listdir(REFERENCE_OUT_DIR):
        return os.path.getsize(REFERENCE_OUT_DIR + name)

    # Generate a random image
    data = np.random.randint(0, 255, size=(Y,X,channels))
    to_save = Image.fromarray(data.astype(np.uint8))
    to_save.save(REFERENCE_OUT_DIR + name)
    return os.path.getsize(REFERENCE_OUT_DIR + name)


def generateNullExtreme(X: int, Y: int, channels: int =3, format: str ='png') -> int:
    """
    Generate a null image for reference.
    """
    name = f'zeros_{X}x{Y}.{format}'
    if name in os.listdir(REFERENCE_OUT_DIR):
        return os.path.getsize(REFERENCE_OUT_DIR + name)

    # Generate a null image
    data = np.zeros((Y,X,channels))
    to_save = Image.fromarray(data.astype(np.uint8))
    to_save.save(REFERENCE_OUT_DIR + name)
    return os.path.getsize(REFERENCE_OUT_DIR + name)


def bound(x: int, upper: int, lower: int) -> int:
    """
    Bound an integer by some upper and lower values.

    Args:
        x (int): value to bound.
        upper (int): upper bound.
        lower (int): lower bound.

    Returns:
        int: upper bound if x > upper, lower bound if x < lower. Unit function on x ∈ [lower, uppoer].
    """
    if x > upper:
        return upper
    if x < lower:
        return lower
    return x


def rx(imageArray: np.ndarray, sparse: bool =False,
       imPath: Optional[str] =None, npts: Optional[int] =None) -> np.ndarray:
    """
    Compute the RX algorithm on an image. This function returns an array with
    one channel, which represents the number of standard deviations a certain
    pixel lies from the mean pixel value.

    Set `sparse' to true if you're expecting the image to be largely the same
    color, or, in other words, most of the pixels to be very similar (e.g. an
    image of a field looking down from a drone will be mostly green). This
    produces a time savings since the covariance matrix may be estimated from
    a random subset of the pixels. If you do not explicitly state the number
    of pixels to use in this subset, then you're required to provide a path to
    the original image file for subset cardinality estimation.

    Set `sparse' and enter a number of pixels to use if you'd like to override
    the default estimate of the number of pixels to use. This of course does
    not require you to specify the image's path.
    """
    if imageArray.ndim != 3:
        raise ValueError(
            f'rx expected image with 3 axes, received {imageArray.ndim}'
        )

    Y, X, channels = imageArray.shape
    size = Y * X

    if sparse:
        ## Estimate entropy from subset

        if npts is not None:
            entropy = npts
        else:
            if imPath is None:
                raise ValueError(
                    'Must provide path to image file for entropy estimation'
                )

            nullSize = generateNullExtreme(X, Y)
            randSize = generateRandExtreme(X, Y)
            dataSize = os.path.getsize(imPath)

            # Control bounds (just in case, though it's unlikely)
            dataSize = bound(dataSize, nullSize, randSize)

            # Best determination of subset size from entropy estimate?
            entropy = int((dataSize - nullSize) / (randSize - nullSize) * size)

        # Generate a subset of the image to work with
        sample = np.random.choice(size, size=entropy)
        flatIm = imageArray.reshape(size, channels)
        flatImSubset = np.take(flatIm, sample, axis=0)

        # From here-on it's pretty much the same as the alternate method
        average = np.average(flatImSubset, axis=0)

        subtracted = imageArray - average

        covMat = np.cov(flatImSubset.T, ddof=0)
        invCovMat = np.linalg.inv(covMat)
    else:
        ## Use every pixel

        # Get the absolute average RGB vector
        average = np.average(imageArray, axis=(0, 1))

        # Compute difference between every RGB value and the mean RGB value
        # (N, M, channels) - (channels,)
        subtracted = imageArray - average

        # Compute the inverse covariance matrix
        covMat = np.cov(subtracted.reshape(size, channels).T, ddof=0)
        invCovMat = np.linalg.inv(covMat)

    # Compute mahalanobis metric on every pixel
    new_arr = np.einsum(
        'ijk,km,ijm->ij', subtracted, invCovMat, subtracted,
        optimize=True
    )
    new_arr = np.sqrt(new_arr)

    return new_arr

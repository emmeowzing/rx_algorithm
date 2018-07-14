# coding=utf-8

import unittest
import os

from rx.rx import getImage
from rx.utils import plot


class TestOpenPlotImage(unittest.TestCase):
    """
    Open an image with getImage.
    """

    IM_DIR = 'test_images' + os.sep

    def setUp(self):
        self.images = os.listdir(self.IM_DIR)

    def test_images_open(self):
        subdirLen = lambda: len(os.listdir(self.IM_DIR))

        original_length = subdirLen()

        for image in self.images:
            with getImage(self.IM_DIR + image) as im:
                plot(im, '../tests/' + self.IM_DIR + 'test_plot_' + image)

        new_length = subdirLen()

        print(original_length, new_length)

        # Clean up
        for image in os.listdir(self.IM_DIR):
            if image not in self.images:
                os.remove(self.IM_DIR + image)

        # Assert that we get more images
        self.assertEqual(original_length, new_length / 2)
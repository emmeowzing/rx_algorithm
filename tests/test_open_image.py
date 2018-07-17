# -*- coding: utf-8 -*-

import unittest
import os
import ntpath

from rx.rx import getImage
from rx.utils import plot


class TestOpenPlotImage(unittest.TestCase):
    """
    Open an image with getImage.
    """ 

    def setUp(self):
        self.IM_DIR = os.getcwd() + os.sep + 'tests' + os.sep \
                                           + 'test_images' + os.sep
        self.images = os.listdir(self.IM_DIR)
        
    def test_images_open(self):
        original_length = len(self.images)
        
        for image in self.images:
            name = self.IM_DIR + image
            rootName = ntpath.basename(name)
            with getImage(name) as im:
                plot(im, self.IM_DIR + 'fig_' + rootName)
        
        new_length = len(os.listdir(self.IM_DIR))
        
        # Clean up
        for image in os.listdir(self.IM_DIR):
            if image not in self.images:
                os.remove(self.IM_DIR + image)
        
        # Assert that we get more images
        self.assertEqual(original_length, new_length // 2)

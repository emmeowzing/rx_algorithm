#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Brandon Doyle <bjd2385@aperiodicity.com>
#
# Distributed under terms of the MIT license.

"""
Test the speed of the RX algorithm implementations.
"""

from rx.rx import rx
from rx.utils import getImage, plot

import unittest
import line_profiler
import os

IM_DIR = os.getcwd() + os.sep + 'tests' + os.sep \
              + 'test_images' + os.sep


# TODO: Finish

class TestSpeed(unittest.TestCase):

    def setUp(self) -> None:
        with getImage(IM_DIR + 'example_1MP.png') as im:
            self.arr = im

    def test_full_speed(self) -> None:
        line_profiler.LineProfiler(rx)
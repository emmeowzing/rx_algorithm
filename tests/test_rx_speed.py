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


IMAGE = 'test_images/example_1MP.png'


# TODO: Finish

class TestSpeed(unittest.TestCase):

    def setUp(self) -> None:
        with getImage(IMAGE) as im:
            self.arr = im

    def test_full_speed(self) -> None:
        with line_profiler.LineProfiler(rx) as profile:
            profile(self.arr)
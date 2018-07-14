#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np

from PIL import Image


def generateNull(X: int, Y: int, channels: int =3, format: str ='png') -> int:
    name = f'zeros_{X}x{Y}.{format}'
    if name in os.listdir('.'):
        return os.path.getsize(name)
    else:
        data = np.zeros((Y,X,channels))
        to_save = Image.fromarray(data.astype(np.uint8))
        to_save.save(name)
        return os.path.getsize(name)


if __name__ == '__main__':
    generateNull(1333, 750)

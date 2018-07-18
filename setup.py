#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os


with open('./README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='rxpy',
    version='1.0',
    author='Brandon Doyle',
    author_email='bjd2385@aperiodicity.com',
    description='A fast (experimental) RX algorithm implementation on 3-dimensional image data/tensors',
    long_description=long_description,
    url='https://github.com/bjd2385/rxpy',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3'
    )
)

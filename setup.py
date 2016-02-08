#!/usr/bin/env python

# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import ast
import os
import re

from setuptools import setup

setup_dir = os.path.abspath(os.path.dirname(__file__))


def find_version(*path_elements):
    """Search a file for `__version__ = 'version number'` and return version.

    @param path_elements: Arguments specifying file to search.

    @return: Version number string.
    """
    path = os.path.join(setup_dir, *path_elements)
    for line in open(path):
        for match in re.finditer('__version__\s*=\s(.*)$', line):
            return ast.literal_eval(match.group(1))
    raise RuntimeError("version string not found in {0}".format(path))


setup(
        name='ezoutlet',
        version=find_version("ezoutlet", "__init__.py"),
        maintainer='Joshua Pereyda',
        maintainer_email='joshua.t.pereyda@gmail.com',
        url='https://github.com/jtpereyda/ezoutlet',
        license='MIT',
        packages=['ezoutlet'],
        install_requires=['future'],
        extras_require={
            # This list is duplicated in tox.ini. Make sure to change both!
            # This can stop once tox supports installing package extras.
            'dev': ['mock', 'pytest'],
        },
)

#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages

url = "https://github.com/pycontribs/wstools.git"


def read(*rnames):
    return "\n" + open(
        os.path.join('.', *rnames)
    ).read()

long_description = """WSDL parsing services package for Web Services for Python. see """ + url \
    + read('README.txt')\
    + read('CHANGES.txt')\

from src.wstools.version import __version__

setup(
    name="wstools",
    version=__version__,
    description="wstools",
    maintainer="Gregory Warnes, kiorky, sorin",
    maintainer_email="Gregory.R.Warnes@Pfizer.com, kiorky@cryptelium.net, sorin.sbarnea+os@gmail.com",
    url=url,
    long_description=long_description,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['docutils'],
    tests_require=['virtualenv>=1.8.4', 'pytest'],
)

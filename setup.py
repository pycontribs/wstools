#!/usr/bin/env python

import os
from setuptools import setup

url = "https://github.com/pycontribs/wstools.git"


def read(*rnames):
    return "\n" + open(
        os.path.join('.', *rnames)
    ).read()

long_description = \
    "WSDL parsing services package for Web Services for Python. see" + url

from wstools.version import __version__

install_requires = [
    'docutils'
]

setup(
    name="wstools",
    version=__version__,
    description="wstools",
    maintainer="Gregory Warnes, kiorky, sorin",
    maintainer_email="Gregory.R.Warnes@Pfizer.com, "
    + " kiorky@cryptelium.net, " + "sorin.sbarnea+os@gmail.com",
    url=url,
    long_description=long_description,
    packages=['wstools'],
    install_requires=install_requires,
)

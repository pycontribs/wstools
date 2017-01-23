#!/usr/bin/env python
import sys
import setuptools
import warnings

from setuptools.command.test import test as TestCommand


# this should help getting annoying warnings from inside distutils
warnings.simplefilter('ignore', UserWarning)


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setuptools.setup(
    setup_requires=['pbr>=1.10', 'setuptools>=17.1', 'pytest-runner'],
    pbr=True,
    cmdclass={'test': PyTest},
    test_suite='tests')

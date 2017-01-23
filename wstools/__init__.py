#! /usr/bin/env python
"""WSDL parsing services package for Web Services for Python."""

ident = "$Id$"

from pbr.version import VersionInfo
from . import WSDLTools  # noqa
from . import XMLname   # noqa

_v = VersionInfo('wstools').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

__all__ = (
    'WDSLTools',
    'XMLname',
    '__version__',
    'version_info'
)

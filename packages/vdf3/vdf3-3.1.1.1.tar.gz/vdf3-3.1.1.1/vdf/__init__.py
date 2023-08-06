# -*- coding: utf-8 -*-

"""Module for deserializing/serializing to and from VDF in Python 3.7+"""

__version__ = "3.1.1.1"
__author__ = (
    "Rossen Georgiev",
    "Gobot1234",
)

from typing import NamedTuple
from multidict import USE_CYTHON_EXTENSIONS

from .exceptions import *

if USE_CYTHON_EXTENSIONS:
    from ._io import *
else:
    from .io import *


from .vdf_dict import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str


version_info = VersionInfo(major=1, minor=1, micro=0, releaselevel="full")

# not for export
del NamedTuple, VersionInfo

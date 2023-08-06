# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Generic, TypeVar

from multidict import MultiDict

__all__ = (
    "VDFDict",
)

_VT = TypeVar("_VT")


class VDFDict(MultiDict[_VT], Generic[_VT]):
    """A dictionary that supports duplicate keys. Bases MultiDict"""
    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.items())})"

    __str__ = __repr__

    def copy(self) -> VDFDict[_VT]:  # MultiDict.copy doesn't seem to use self.__class__
        return self.__class__(self.items())

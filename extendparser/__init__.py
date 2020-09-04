# -*- coding: utf-8 -*-
"""Extend parser is set of ConfigParser extensions.

All extensions are added to one final class ExtendParser.

example code:

    >>> from extendparser import ExtendParser
    >>> cp = ExtendParser()
"""

from .get import Get
from .include import Include

__author__ = "Ondřej Tůma"
__version__ = "0.3.0-dev"
__copyright__ = "Copyright 2018"
__license__ = "BSD"
__email__ = "mcbig@zeropage.cz"

__all__ = ["include", "get", "ExtendParser"]


# pylint: disable=too-many-ancestors
class ExtendParser(Get, Include):
    """Final class with all extends"""

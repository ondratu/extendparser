# -*- coding: utf-8 -*-
"""Extend parser is set of ConfigParser extensions.

All extensions are added to one final class ExtendParser.

example code:

    >>> from extendparser import ExtendParser
    >>> cp = ExtendParser()
"""

from extendparser.get import Get
from extendparser.include import Include

__author__ = "Ondřej Tůma"
__version__ = "0.1.0"
__name__ = "extendparser"
__copyright__ = "Copyright 2018"
__license__ = "BSD"
__email__ = "mcbig@zeropage.cz"

__all__ = ["extend", "include", "get", "to3", "ExtendParser"]


class ExtendParser(Get, Include):
    """Final class with all extends"""

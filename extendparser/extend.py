"""Mix of all extends from this package.

    >>> from extendparser.extend import ExtendParser
    >>> cp = ExtendParser()
"""

from extendparser.get import Get
from extendparser.include import Include


class ExtendParser(Get, Include):
    """Final class with all extends"""

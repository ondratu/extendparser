"""Python version compatibility module to right import some modules.

    >>> from config_extends.to3 import ConfigParser
    >>> from config_extends.to3 import BufferIO
"""
from sys import version_info

if version_info.major == 2:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError
    from io import BytesIO as BufferIO
else:
    from configparser import ConfigParser, NoSectionError, NoOptionError
    from io import StringIO as BufferIO

__all__ = [ConfigParser, NoSectionError, NoOptionError, BufferIO]

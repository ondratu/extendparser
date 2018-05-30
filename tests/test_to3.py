"""Test to3 python module."""
from sys import path as python_path
from os import path
from unittest import TestCase

python_path.insert(0, path.abspath(             # noqa
    path.join(path.dirname(__file__), path.pardir)))

from extendparser import to3


class TestConfigParser(TestCase):
    """ConfigParser test."""
    def test_config_parser(self):
        assert to3.ConfigParser is not None

    def test_no_section_error(self):
        assert issubclass(to3.NoSectionError, Exception)

    def test_no_option_error(self):
        assert issubclass(to3.NoOptionError, Exception)


class TestBufferIO(TestCase):
    """BufferIO test."""
    def test_read(self):
        buf = to3.BufferIO()
        assert getattr(buf, "read") is not None

    def test_write(self):
        buf = to3.BufferIO()
        assert getattr(buf, "write") is not None

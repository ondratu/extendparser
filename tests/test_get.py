"""Test for Get extension."""
from unittest import TestCase
from configparser import NoOptionError, NoSectionError

import logging

from extendparser.get import Get

LOG = []

# pylint: disable=missing-function-docstring


class ListHandler(logging.NullHandler):
    """Logging handler for log to list."""
    def handle(self, record):
        LOG.append(record.msg % record.args)


logger = logging.getLogger("extendparser")    # pylint: disable=invalid-name
logger.setLevel(logging.INFO)
logger.addHandler(ListHandler())


class TestParse(TestCase):
    """Test parsing types."""
    cfp = Get()
    cfp.add_section("test")
    cfp.set("test", "string", "value")
    cfp.set("test", "number", "42")
    cfp.set("test", "true", "on")
    cfp.set("test", "false", "off")
    cfp.set("test", "list", "a,b,c")
    cfp.set("test", "tuple", "a;b;c")

    def test_str(self):
        assert self.cfp.get_option("test", "string") == "value"

    def test_int(self):
        assert self.cfp.get_option("test", "number", target=int) == 42

    def test_true(self):
        assert self.cfp.get_option("test", "true", target=bool) is True

    def test_false(self):
        assert self.cfp.get_option("test", "false", target=bool) is False

    def test_list(self):
        assert self.cfp.get_option(
            "test", "list", target=list) == ['a', 'b', 'c']

    def test_tuple(self):
        assert self.cfp.get_option(
            "test", "tuple", target=tuple, delimiter=';') == ('a', 'b', 'c')


class TestFallback(TestCase):
    """Test getting fallback."""
    cfp = Get()

    def test_str(self):
        assert self.cfp.get_option(
            "test", "string", fallback="value") == "value"
        assert LOG.pop().endswith("[%s]::%s" % ("test", "string"))

    def test_int(self):
        assert self.cfp.get_option(
            "test", "number", target=int, fallback=42) == 42
        assert LOG.pop().endswith("[%s]::%s" % ("test", "number"))

    def test_bool(self):
        assert self.cfp.get_option(
            "test", "boolean", target=bool, fallback=True) is True
        assert LOG.pop().endswith("[%s]::%s" % ("test", "boolean"))

    def test_list(self):
        assert self.cfp.get_option(
            "test", "list", fallback=['foo'], target=list) == ['foo']
        assert LOG.pop().endswith("[%s]::%s" % ("test", "list"))


class TestNotFound(TestCase):
    """Test error states."""
    cfp = Get()
    cfp.add_section("test")

    def test_no_option(self):
        with self.assertRaises(NoOptionError):
            self.cfp.get_option("test", "option")
        assert LOG.pop().startswith("[%s]::%s" % ("test", "option"))

    def test_no_section(self):
        with self.assertRaises(NoSectionError):
            self.cfp.get_option("section", "option")
        assert LOG.pop().startswith("[%s]::%s" % ("section", "option"))


class TestSection(TestCase):
    """Test getting full section."""
    cfp = Get()
    cfp.add_section("test")
    cfp.set("test", "string", "value")
    cfp.set("test", "number", "1")
    cfp.set("test", "bool", "on")
    cfp.set("test", "list", "1;2")

    def test_all_string(self):
        kwargs = self.cfp.get_section("test", ("string", "number", "bool"))
        assert kwargs == {"string": "value", "number": "1", "bool": "on"}

    def test_mix(self):
        kwargs = self.cfp.get_section("test", ("string", ("bool", bool),
                                               ("list", list, [], ';')))
        assert kwargs == {"string": "value", "bool": True, "list": ['1', '2']}

    def test_skip(self):
        kwargs = self.cfp.get_section("new", (("string", str, "value"),
                                              ("bool", bool, False),
                                              ("number")))
        assert kwargs == {"string": "value", "bool": False}

    def test_not_skip(self):
        with self.assertRaises(NoSectionError):
            self.cfp.get_section("new", (("string", str, "value"),
                                         ("bool", bool, False),
                                         ("number")), False)

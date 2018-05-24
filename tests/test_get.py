from sys import path as python_path
from os import path

python_path.insert(0, path.abspath(             # noqa
                   path.join(path.dirname(__file__), path.pardir)))

from unittest import TestCase

from config_extends.get import Get
from config_extends.to3 import NoOptionError, NoSectionError

LOG = []


def log_fce(msg):
    LOG.append(msg)


class TestParse(TestCase):
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


class TestDefault(TestCase):
    cfp = Get()
    cfp.log_info = log_fce

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
    cfp = Get()
    cfp.log_error = log_fce
    cfp.add_section("test")

    def test_no_option(self):
        with self.assertRaises(NoOptionError):
            self.cfp.get_option("test", "option")
        assert LOG.pop().startswith("[%s]::%s" % ("test", "option"))

    def test_no_section(self):
        with self.assertRaises(NoSectionError):
            self.cfp.get_option("section", "option")
        assert LOG.pop().startswith("[%s]::%s" % ("section", "option"))

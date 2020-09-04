"""Test Include extension."""
from os import path, chdir, getcwd
from unittest import TestCase

from extendparser.include import Include

PWD = getcwd()
TEST_PATH = path.dirname(__file__)              # noqa

# pylint: disable=missing-function-docstring


class TestInclude(TestCase):
    """Test including."""
    cfp = Include()

    @classmethod
    def setUpClass(cls):
        chdir(path.join(TEST_PATH, path.pardir))
        cls.cfp.read("tests/data/test.ini")

    @classmethod
    def tearDownClass(cls):
        chdir(PWD)

    def test_include(self):
        assert self.cfp.get("main", "foo") == "bar"

    def test_include_include(self):
        assert self.cfp.get("sec", "key") == "include2 value"

    def test_include_order(self):
        assert self.cfp.get("main", "key") == "value"

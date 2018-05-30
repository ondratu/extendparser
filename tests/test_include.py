"""Test Include extension."""
from sys import path as python_path
from os import path, chdir, getcwd
from unittest import TestCase

TEST_PATH = path.dirname(__file__)              # noqa
python_path.insert(0, path.abspath(             # noqa
    path.join(TEST_PATH, path.pardir)))

from extendparser.include import Include

PWD = getcwd()


class TestInclude(TestCase):
    """Test including."""
    cfp = Include()

    @classmethod
    def setUpClass(self):
        chdir(path.join(TEST_PATH, path.pardir))
        self.cfp.read("tests/data/test.ini")

    @classmethod
    def tearDownClass(self):
        chdir(PWD)

    def test_include(self):
        assert self.cfp.get("main", "foo") == "bar"

    def test_include_include(self):
        assert self.cfp.get("sec", "key") == "include2 value"

    def test_include_order(self):
        assert self.cfp.get("main", "key") == "value"

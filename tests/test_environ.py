"""Test for environment support."""
from os import environ
from unittest import TestCase

from extendparser.environ import VarNameBuilder, EnvironFirst, EnvironLast
from extendparser.get import Get

# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
# pylint: disable=too-many-ancestors


class TestVarNameBuilder():
    """Test variable name builder."""

    def test_title(self):
        class OwnVarNameBuilder(VarNameBuilder):
            """Own VarNameBuilder."""
            def varname(self, section, option):
                return self.var_format.format(section=section.title(),
                                              option=option.title())

        assert OwnVarNameBuilder().varname('database', 'hostname') == \
            'Database_Hostname'

    def test_map(self):
        class OwnVarNameBuilder(VarNameBuilder):
            """Own VarNameBuilder."""
            remaping = {'database': 'DB'}

            def varname(self, section, option):
                section = self.remaping.get(section, section)
                return super().varname(section, option)

        assert OwnVarNameBuilder().varname('database', 'hostname') == \
            'DB_HOSTNAME'

        assert OwnVarNameBuilder().varname('user', 'name') == \
            'USER_NAME'


class TestMixin(TestCase):
    """Test EnvironFirst mixin with Get."""

    class MixinFirst(EnvironFirst, Get):
        """Testing mixin class."""
        var_format = "TEST_{section}_{option}"

    class MixinLast(EnvironLast, Get):
        """Testing mixin class."""
        var_format = "TEST_{section}_{option}"

    first = MixinFirst()
    last = MixinLast()

    @classmethod
    def setUpClass(cls):
        environ['TEST_DB_USER'] = 'john'
        environ['TEST_DB_PORT'] = '1234'
        environ['TEST_DB_KEEPALIVE'] = 'on'
        environ['TEST_TEST_BOTH'] = '1,2'

        for cfp in (cls.first, cls.last):
            cfp.add_section("test")
            cfp.set("test", "string", "value")
            cfp.set("test", "number", "42")
            cfp.set("test", "true", "on")
            cfp.set("test", "both", "5,6")

    @classmethod
    def tearDownClass(cls):
        environ.pop('TEST_DB_USER', None)
        environ.pop('TEST_DB_PORT', None)
        environ.pop('TEST_DB_KEEPALIVE', None)
        environ.pop('TEST_BOTH', None)

    def test_string(self):
        for cfp in (self.first, self.last):
            with self.subTest(cls=cfp):
                # from Config Parser
                assert cfp.get_option("test", "string") == 'value'

                # from Environment
                assert cfp.get_option("db", "user") == 'john'

                # from Fallback
                assert cfp.get_option(
                    "db", "string", fallback="value") == 'value'

    def test_int(self):
        for cfp in (self.first, self.last):
            with self.subTest(cls=cfp):
                # from Config Parser
                assert cfp.get_option("test", "number", target=int) == 42

                # from Environment
                assert cfp.get_option("db", "port", target=int) == 1234

                # from Fallback
                assert cfp.get_option(
                    "db", "number", target=int, fallback=42) == 42

    def test_bool(self):
        for cfp in (self.first, self.last):
            with self.subTest(cls=cfp):
                # from ConfigParser
                assert cfp.get_option("test", "true", target=bool) is True

                # from Environment
                assert cfp.get_option("db", "keepalive", target=bool) is True

                # from Fallback
                assert cfp.get_option(
                    "db", "true", target=bool, fallback=True) is True

    def test_section_string(self):
        for cfp in (self.first, self.last):
            with self.subTest(cls=cfp):
                # from ConfigParser
                kwargs = cfp.get_section("test", ("string", "number", "true"))
                assert kwargs == {"string": "value", "number": "42",
                                  "true": "on"}

                # from Environ
                kwargs = cfp.get_section("db", ("user", "port", "keepalive"))
                assert kwargs == {"user": "john", "port": "1234",
                                  "keepalive": "on"}

                # from fallback (skip)
                kwargs = cfp.get_section("db", ("string", "number", "true"))
                assert kwargs == {}

    def test_section_target(self):
        for cfp in (self.first, self.last):
            with self.subTest(cls=cfp):
                # from ConfigParser
                kwargs = cfp.get_section("test", ("string",
                                                  ("number", int),
                                                  ("true", bool)))
                assert kwargs == {"string": "value", "number": 42,
                                  "true": True}

                # from Environ
                kwargs = cfp.get_section("db", ("user",
                                                ("port", int),
                                                ("keepalive", bool)))
                assert kwargs == {"user": "john", "port": 1234,
                                  "keepalive": True}

                # from fallback
                kwargs = cfp.get_section("db", (("string", str, "value"),
                                                ("number", int, 42),
                                                ("true", bool, True)))
                assert kwargs == {"string": "value", "number": 42,
                                  "true": True}

    def test_environment_first(self):
        """Environment variables have accuracy."""
        assert self.first.get_option("test", "both", target=list) == ['1', '2']

    def test_environment_last(self):
        """ConfigParser variables have accuracy."""
        assert self.last.get_option("test", "both", target=list) == ['5', '6']

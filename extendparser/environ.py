"""Environment variable support.

"""
from os import environ
from configparser import ConfigParser
from logging import getLogger

# pylint: disable=too-many-ancestors

log = getLogger(__package__)  # pylint: disable=invalid-name


class VarNameBuilder():  # pylint: disable=too-few-public-methods
    """Support class for building variable name.

    Simple changing variable name building format:

        >>> from extendparser.environ import VarNameBuilder
        >>> vnb = VarNameBuilder()
        >>> vnb.var_format = 'PREFIX_{option}_{section}'
        >>> vnb.varname('database', 'hostname')
        'PREFIX_HOSTNAME_DATABASE'

    Own varname method:

    .. code:: python

        from extendparser.environ import VarNameBuilder


        class OwnVarNameBuilder(VarNameBuilder):
            def varname(self, section, option):
                return self.var_format.format(section=section.title(),
                                              option=option.title())

        # return 'Database_Hostname'
        OwnVarNameBuilder().varname('database', 'hostname')


    Section mapping:

    .. code:: python

        from extendparser.environ import VarNameBuilder


        class OwnVarNameBuilder(VarNameBuilder):
            remaping = {'database': 'DB'}

            def varname(self, section, option):
                section = self.remaping.get(section, section)
                return super().varname(section, option)

        # return 'DB_HOSTNAME'
        OwnVarNameBuilder().varname('database', 'hostname')
    """
    var_format = "{section}_{option}"

    def varname(self, section, option):
        """Return variable name in environment by section and option.

        >>> from extendparser.environ import VarNameBuilder
        >>> VarNameBuilder().varname('database', 'hostname')
        'DATABASE_HOSTNAME'
        """
        return self.var_format.format(section=section.upper(),
                                      option=option.upper())


class EnvironFirst(VarNameBuilder, ConfigParser):
    """Read values from system environment first, then from ConfigParser.

        >>> from os import environ
        >>> from configparser import ConfigParser
        >>> from extendparser.environ import EnvironFirst
        >>> cp = EnvironFirst()
        >>> cp.add_section("test")
        >>> cp.getint("test", "int_number", fallback=1)
        1
        >>> cp.set("test", "int_number", "7")
        >>> cp.getint("test", "int_number")
        7
        >>> environ["TEST_INT_NUMBER"] = "42"
        >>> cp.getint("test", "int_number")
        42
    """

    def get(self, section, option, *args, raw=False, **kwargs):
        """Try to get variable from environment.

        If variable does not exists, or raw is True, original ConfigParser get
        method will be called.
        """
        # pylint: disable=arguments-differ
        if raw:
            return super().get(section, option, *args, raw=raw, **kwargs)

        key = self.varname(section, option)
        log.debug('Try to use %s environment variable', key)
        if key in environ:
            return environ[key]

        return super().get(section, option, *args, raw=raw, **kwargs)


class EnvironLast(VarNameBuilder, ConfigParser):
    """Read values from system environment as fallback for ConfigParser.

        >>> from os import environ
        >>> from configparser import ConfigParser
        >>> from extendparser.environ import EnvironLast
        >>> cp = EnvironLast()
        >>> cp.add_section("test")
        >>> cp.getfloat("test", "float_number", fallback=1.0)
        1.0
        >>> environ["TEST_FLOAT_NUMBER"] = "42"
        >>> cp.getfloat("test", "float_number", fallback=1)
        42.0
        >>> cp.set("test", "float_number", "3.14")
        >>> cp.getfloat("test", "float_number")
        3.14
    """

    def get(self, section, option, *args, **kwargs):
        """If variable exist in environment, use it's value as fallback."""
        # pylint: disable=arguments-differ
        key = self.varname(section, option)
        if key in environ:
            log.info('Use %s environment variable as fallback', key)
            kwargs['fallback'] = environ[key]

        return super().get(section, option, *args, **kwargs)

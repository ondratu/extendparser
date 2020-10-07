"""ConfigParser with extends get method for automatics conversion..

    example code:

        >>> from extendparser.get import Get
        >>> cp = Get()
        >>> print(cp.get_option("test", "number", target=int, fallback=1))
        1
        >>> print(cp.get_option("test", "list", target=list, fallback=["a"],
        ...                      delimiter=','))
        ['a']
        >>> cp.add_section("test")
        >>> cp.set("test", "tuple", "a:b:c")
        >>> print(cp.get_option("test", "tuple", target=tuple, delimiter=':'))
        ('a', 'b', 'c')
        >>> kwargs = cp.get_section("test", (("tuple", tuple, tuple(), ':'),
        ...                                  ("string", str, "value")))
        >>> kwargs == {'tuple': ('a', 'b', 'c'), 'string': 'value'}
        True
"""

from logging import getLogger
from configparser import ConfigParser, NoSectionError, NoOptionError

__all__ = ["Get", "Nothing"]

# pylint: disable=too-many-ancestors
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

log = getLogger(__package__)  # pylint: disable=invalid-name


class Nothing:
    """Class using for get_option default parameter."""


class Get(ConfigParser):
    """Extends ConfigParser for smarter get methods."""

    def get_option(self, section, option, target=str, fallback=Nothing,
                   delimiter=','):
        """Return option in target type.

        It can parse string to tuple, list or set. Extends classes from tuple,
        list or set must have own string parser in constructor.
        """
        try:
            if issubclass(target, bool):
                return self.getboolean(section, option)

            value = self.get(section, option).strip()
            if target in (list, tuple, set):
                if not value:
                    return target()
                return target(s.strip() for s in value.split(delimiter))
            return target(value)
        except (NoSectionError, NoOptionError):
            if fallback is Nothing:
                log.warning("[%s]::%s not defined and no fallback value "
                            "specified", section, option)
                raise
            log.info("Using fallback value `%s' for [%s]::%s",
                     fallback, section, option)
            return fallback

    def get_section(self, section, options, skip=True):
        """Get full options from section.

        Params:
            section - section name
            options - list of tuples as *args fo get method
                      (option, target, fallback, delimiter) so only
                      option is required. That could be set as string item
                      in options list.
            skip    - if is true, non exist options are skiped, so
                      no error is rised.

        Return dictionary, which could be use as **kwargs. If skip is set to
        true, options without fallback values are not return if is not found
        in config.
        """
        values = {}
        for args in options:
            try:
                if not isinstance(args, (list, tuple)):
                    args = (args,)
                values[args[0]] = self.get_option(section, *args)
            except (NoSectionError, NoOptionError):
                if not skip:
                    raise
        return values

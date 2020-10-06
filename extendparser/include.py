"""ConfigParser with include support.

    .. code:: ini

        # tests/data/test.ini
        [main]
        key = value

        .include tests/data/include.ini

    .. code:: ini

        # tests/data/include.ini
        [main]
        foo = bar

    example code:

        >>> from extendparser.include import Include
        >>> from sys import stdout
        >>> cp = Include()
        >>> cp.read("tests/data/test.ini")
        ['tests/data/test.ini']
        >>> print(cp.get("main", "key"))
        value
        >>> print(cp.get("main", "foo"))
        bar
"""

from os.path import exists
from os import PathLike, fspath
from configparser import ConfigParser
from io import StringIO

__all__ = ["ConfigParser"]

# pylint: disable=too-many-ancestors
# pylint: disable=arguments-differ


class Include(ConfigParser):
    """ConfigParser which supports includes.

    Includes are provide by `.include` keyword on empty line. Including is like
    templating, so each included file expression is replaced in read config
    string.
    """

    def read_file(self, file_, source=None):
        """Overriding method which support .include expression."""
        config_string = StringIO()

        for line in file_:
            if line.startswith('.include'):
                self.read_buffer(config_string, source)

                self.read(line[8:].strip())     # read includeded ini
                config_string = StringIO()      # reset config_string
            else:
                config_string.write(line)

        self.read_buffer(config_string, source)

    def read_buffer(self, buff, source=None):
        """This method read call original methods.

        Use readfp in python2 or read_file in python3."""
        buff.seek(0)

        super().read_file(buff, source)

    def read(self, filenames, encoding=None):
        """Overriding method to call instance read_file from actual path."""
        if isinstance(filenames, (str, bytes, PathLike)):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            if exists(filename):
                with open(filename, 'r', encoding=encoding) as file_:
                    self.read_file(file_, filename)
            if isinstance(filename, PathLike):
                filename = fspath(filename)
            read_ok.append(filename)
        return read_ok

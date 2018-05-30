"""extendparser package installation."""
from setuptools import setup
from io import open

from extendparser import __name__ as name, __version__, __author__, \
    __email__, __license__


def doc():
    """Return README.rst content."""
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read().strip()


setup(
    name=name,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=(
        "ExtendParser extend stanrad ConfigParser for some functionality."),
    long_description=doc(),
    long_description_content_type="text/x-rst",
    url="https://github.com/ondratu/extendparser",
    license=__license__,
    packages=["extendparser"],
    data_files=[('share/doc/extendparser',
                 ["README.rst", "COPYING", "ChangeLog", "AUTHORS",
                  "CONTRIBUTION.rst"])],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"],
    )

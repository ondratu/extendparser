"""Loging support for any class.

    >>> from extendparser.log import Logger
    >>> log = Logger()
    >>> log.log_info("message")
    ExtendedParser: message
    >>> log.log_error("message")  # output the same to stderr
"""
import sys


class Logger():
    @staticmethod
    def log_info(msg):
        sys.stdout.write("ExtendedParser: %s\n" % msg)

    @staticmethod
    def log_error(msg):
        sys.stderr.write("ExtendedParser: %s\n" % msg)

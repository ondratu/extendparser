from sys import path as python_path
from os import path

python_path.insert(0, path.abspath(             # noqa
                   path.join(path.dirname(__file__), path.pardir)))

from unittest import TestCase
from extendparser.to3 import BufferIO
from extendparser import log

LOG = []


def own_log(msg):
    LOG.append(msg)


class TestInfo(TestCase):

    def test_std(self):
        log.sys.stdout = BufferIO()
        logger = log.Logger()
        logger.log_info("info message")
        log.sys.stdout.seek(0)
        assert log.sys.stdout.read().endswith("info message\n")

    def test_own(self):
        logger = log.Logger()
        logger.log_info = own_log
        logger.log_info("info message")
        assert LOG.pop() == "info message"


class TestError(TestCase):

    def test_std(self):
        log.sys.stderr = BufferIO()
        logger = log.Logger()
        logger.log_error("error message")
        log.sys.stderr.seek(0)
        assert log.sys.stderr.read().endswith("error message\n")

    def test_own(self):
        logger = log.Logger()
        logger.log_error = own_log
        logger.log_error("error message")
        assert LOG.pop() == "error message"

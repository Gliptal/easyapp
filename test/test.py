import sys


sys.path.append("../src")

import logging
import pathlib
import unittest

import easyapp
from easyapp import ARGS, CONFIGS


logger = logging.getLogger(__name__)


class Tester(unittest.TestCase):

    def test_log(self) -> None:
        self.assertTrue(pathlib.Path.is_file(pathlib.Path("logs/log.log")))

    def test_config(self) -> None:
        self.assertEqual(CONFIGS["config"]["configuration"].get(), "config")
        self.assertEqual(CONFIGS["default"]["configuration"].get(), "default")

    def test_arguments(self) -> None:
        self.assertEqual(ARGS.argument, "argument")
        self.assertTrue(ARGS.bool)
        self.assertEqual(ARGS.int, 1)
        self.assertEqual(ARGS.float, 1.11)
        self.assertEqual(ARGS.string, "string")


if __name__ == "__main__":
    logger.info("running tests")
    print()

    suite = unittest.TestLoader().loadTestsFromTestCase(Tester)
    unittest.TextTestRunner(verbosity=2).run(suite)

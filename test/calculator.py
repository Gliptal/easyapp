import sys
#yapf: disable
sys.path.append("../src")
#yapf: enable

import logging
import pathlib
import unittest

import easyapp
import easyapp.config
from easyapp import ARGS, CONFIGS


logger = logging.getLogger(__name__)


class Tester(unittest.TestCase):

    def test_log(self) -> None:
        self.assertTrue(pathlib.Path.is_file(pathlib.Path("logs/log.log")))

    def test_arguments(self) -> None:
        self.assertEqual(ARGS.operations, "all")
        self.assertTrue(ARGS.max, -1)

    def test_config(self) -> None:
        CONFIGS["config"]["version"] = "v2"
        easyapp.config.manager["config"].refresh()
        self.assertEqual(CONFIGS["config"]["version"], "v2")

        CONFIGS["config"]["version"] = "v1"
        easyapp.config.manager["config"].refresh()
        self.assertEqual(CONFIGS["config"]["version"], "v1")


class Calculator(unittest.TestCase):

    def test_calculator(self) -> None:
        config = CONFIGS["config"]

        operations = ARGS.operations if ARGS.operations != "all" else config["operations"].keys()

        for operation in operations:

            if operation == "sum":
                for op in config["operations/sum"]:
                    self.assertEqual(sum(op['addends']), 2 + 2)

            if operation == "division":
                for op in config["operations/division"]:
                    self.assertEqual(op['dividend'] / op['divisor'], 10 / 2)


if __name__ == "__main__":
    logger.info("running tests")

    runner = unittest.TextTestRunner(verbosity=0)

    print()
    suite = unittest.TestLoader().loadTestsFromTestCase(Tester)
    runner.run(suite)

    print()
    calculator = unittest.TestLoader().loadTestsFromTestCase(Calculator)
    runner.run(calculator)

    print()

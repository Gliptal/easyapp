from __future__ import annotations

import logging
import math
import pathlib
import unittest

import easyapp
from easyapp import ARGS, CONFIGS


logger = logging.getLogger(__name__)


class Tester(unittest.TestCase):

    def test_log(self) -> None:
        self.assertTrue(pathlib.Path("logs/log.log").is_file())

    def test_arguments(self) -> None:
        self.assertEqual(int(ARGS.value), 10)
        self.assertEqual(ARGS.mode, "approximate")

    def test_config(self) -> None:
        config = CONFIGS["config"]

        self.assertEqual(config["version"], "v1")

        config["version"] = "v2"
        config.reload()
        self.assertEqual(config["version"], "v2")

        config["version"] = "v1"
        config.reload()
        self.assertEqual(config["version"], "v1")

    def test_factorial(self) -> None:
        self.assertEqual(factorial(ARGS.value), 3598696)


def factorial_iterative(value: int) -> int:
    res = 1
    for n in range(1, value + 1):
        res *= n

    return res


def factorial_recursive(value: int) -> int:
    if value == 0:
        return 1
    else:
        return value * factorial_recursive(value - 1)


def factorial_approximate(value: int) -> int:
    return round(math.sqrt(2 * math.pi * value) * (value / math.e)**value)


def factorial(value: int) -> int:
    value = min(value, ARGS.limit)

    if ARGS.mode == "precise":
        algorithm = CONFIGS["config"]["algorithm"]

        if algorithm == "recursive":
            return factorial_recursive(value)
        elif algorithm == "iterative":
            return factorial_iterative(value)

    elif ARGS.mode == "approximate":
        return factorial_approximate(value)

    return -1


if __name__ == "__main__":
    logger.info("running tests")

    print()

    runner = unittest.TextTestRunner(verbosity=0)
    suite = unittest.TestLoader().loadTestsFromTestCase(Tester)
    runner.run(suite)

    print()

from __future__ import annotations

import logging
import math

import easyapp
from easyapp import ARGS, CONFIGS


logger = logging.getLogger(__name__)


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


def factorial(value: int) -> None:
    fact = -1

    CONFIGS["results"]["executions"] += 1

    value = min(ARGS.value, ARGS.limit)
    if value == ARGS.limit:
        logger.info(f"clamped value to {ARGS.limit}")

    logger.debug(f"using {ARGS.mode} mode")

    if ARGS.mode == "approximate":
        fact = factorial_approximate(value)
    elif ARGS.mode == "precise" and CONFIGS["config"]["algorithm"] == "recursive":
        fact = factorial_recursive(value)
    elif ARGS.mode == "precise" and CONFIGS["config"]["algorithm"] == "iterative":
        fact = factorial_iterative(value)

    CONFIGS["results"]["latest"] = f"{value}! = {fact}"

    logger.info(f"{min(ARGS.value, ARGS.limit)}! = {fact}")


if __name__ == "__main__":
    factorial(ARGS.value)

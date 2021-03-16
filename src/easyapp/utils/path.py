from __future__ import annotations

import pathlib
import sys


def shorten_path(path: pathlib.Path, depth: int = 2) -> pathlib.Path:
    parts = path.parts[slice(-depth, None)]
    return pathlib.Path(*parts)


def cwd_path(path: pathlib.Path | str) -> pathlib.Path:
    return pathlib.Path.cwd() / pathlib.Path(path)


def __get_cwd() -> pathlib.Path:
    try:
        return pathlib.Path(sys._MEIPASS)    #type: ignore
    except AttributeError:
        return __path_cwd_()


__path_cwd_ = pathlib.Path.cwd
pathlib.Path.cwd = __get_cwd

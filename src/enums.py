from enum import StrEnum, auto


class Stage(StrEnum):
    PROD = auto()
    DEV = auto()


class Color(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    MAGENTA = auto()
    CYAN = auto()

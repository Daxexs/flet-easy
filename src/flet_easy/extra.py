from dataclasses import dataclass
from re import Pattern, compile
from typing import Callable, Dict, Optional, Tuple


@dataclass
class Msg:
    method: str
    key: str = None
    value: str | dict = None


@dataclass
class Redirect:
    route: str = None


TYPE_PATTERNS: Dict[str, Tuple[Pattern[str], Callable[[str], Optional[bool]]]] = {
    "int": (compile(r"-?\d+"), int),
    "float": (compile(r"-?\d+\.\d+"), float),
    "str": (compile(r"[^/]+"), str),
    "bool": (compile(r"(true|True|false|False)"), lambda x: x in ["true", "True"]),
}

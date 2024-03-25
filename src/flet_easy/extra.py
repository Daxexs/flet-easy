from dataclasses import dataclass


@dataclass
class Msg:
    method: str
    key: str = None
    value: str = None

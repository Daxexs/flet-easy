from dataclasses import dataclass


@dataclass
class Msg:
    method: str
    key: str
    value: str = None

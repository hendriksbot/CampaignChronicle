"""this module module supports chronicle objects"""

from dataclasses import dataclass


@dataclass
class ChronicleObject:
    name: str
    id: str
    type: str

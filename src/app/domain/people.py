"""this module module supports people maintenance"""

from dataclasses import dataclass
import app.domain.chronicle_objects as chrobj


@dataclass
class Person(chrobj.ChronicleObject):
    pass

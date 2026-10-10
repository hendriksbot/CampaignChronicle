"""view models for chronicle objects"""

from dataclasses import dataclass, field
from typing import TypedDict


@dataclass
class VMChronicleObject:
    id: str
    type: str
    markdown_rendered: str
    markdown_raw: str


class ChronicleObjectOverviewItem(TypedDict):
    name: str
    id: str
    href: str


@dataclass
class VMChronicleObjectOverviewList:
    resource_type: str
    objects: list[ChronicleObjectOverviewItem] = field(default_factory=list)

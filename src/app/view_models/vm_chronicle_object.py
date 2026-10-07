"""view models for chronicle objects"""

from dataclasses import dataclass


@dataclass
class VMChronicleObject:
    id: str
    type: str
    markdown_rendered: str
    markdown_raw: str

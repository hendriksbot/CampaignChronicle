"""view models for people"""

from dataclasses import dataclass


@dataclass
class VMPerson:
    id: str
    markdown_rendered: str
    markdown_raw: str

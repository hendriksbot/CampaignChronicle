"""this moduls defines relations"""

from dataclasses import dataclass, field


@dataclass
class RelationshipDefinition:
    type: str
    display_name: str
    directed: bool
    inverse_display_name: str | None = None
    style: dict = field(default_factory=dict)


RELATIONSHIP_DEFINITIONS = {
    "child_of": {
        "display_name": "Kind von",
        "directed": True,
        "inverse_display_name": "Elternteil von",
        "style": {
            "line-color": "#4f8ef7",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "triangle",
        },
    },
    "friend": {
        "display_name": "befreundet",
        "directed": False,
        "style": {
            "line-color": "#4CAF50",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "none",
        },
    },
    "enemy": {
        "display_name": "verfeindet",
        "directed": False,
        "style": {
            "line-color": "#E53935",
            "line-style": "dashed",
            "source-arrow-shape": "none",
            "target-arrow-shape": "none",
        },
    },
}

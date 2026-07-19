"""this moduls defines relations"""

from dataclasses import dataclass, field


@dataclass
class Relation:
    type: str
    id: str
    source_id: str
    target_id: str


@dataclass
class RelationTypeDefinition:
    type: str
    display_name: str
    directed: bool
    inverse_display_name: str | None = None
    style: dict = field(default_factory=dict)


def get_relation_type_definitions() -> list[RelationTypeDefinition]:
    definitions = []
    for key, value in RELATIONSHIP_DEFINITIONS.items():
        definitions.append(RelationTypeDefinition(key, **value))
    return definitions


RELATIONSHIP_DEFINITIONS = {
    "parent_of": {
        "display_name": "Elternteil von",
        "directed": True,
        "inverse_display_name": "Kind von",
        "style": {
            "line-color": "#4f8ef7",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "triangle",
        },
    },
    "married": {
        "display_name": "verheiratet",
        "directed": False,
        "style": {
            "line-color": "#660c9b",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "none",
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

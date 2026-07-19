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
    "rival": {
        "display_name": "Rivale von",
        "directed": False,
        "style": {
            "line-color": "#F9A825",
            "line-style": "dashed",
            "source-arrow-shape": "none",
            "target-arrow-shape": "none",
        },
    },
    "mentor_of": {
        "display_name": "Mentor von",
        "directed": True,
        "inverse_display_name": "Schüler von",
        "style": {
            "line-color": "#26A69A",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "triangle",
        },
    },
    "leader_of": {
        "display_name": "Anführer von",
        "directed": True,
        "inverse_display_name": "angeführt von",
        "style": {
            "line-color": "#FB8C00",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "triangle",
        },
    },
    "works_for": {
        "display_name": "Arbeitet für",
        "directed": True,
        "inverse_display_name": "Beschäftigt",
        "style": {
            "line-color": "#FF9800",
            "line-style": "solid",
            "source-arrow-shape": "none",
            "target-arrow-shape": "triangle",
        },
    },
    "is": {
        "display_name": "ist",
        "directed": False,
        "style": {
            "line-color": "#7E57C2",
            "line-style": "solid",
            "source-arrow-shape": "diamond",
            "target-arrow-shape": "diamond",
        },
    },
}

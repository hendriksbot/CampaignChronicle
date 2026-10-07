"""presenter module"""

import markdown as md
from functools import singledispatchmethod

import app.domain.chronicle_objects as chrobj
import app.domain.relations as rel
import app.view_models.vm_chronicle_object as vm_chrobj


class Presenter:
    """presenter class"""

    def show_chronicle_object(
        self, obj: chrobj.ChronicleObject, file_content: str
    ) -> vm_chrobj.VMChronicleObject:
        return vm_chrobj.VMChronicleObject(
            id=obj.id,
            type=obj.type,
            markdown_rendered=self.render_markdown(file_content),
            markdown_raw=file_content,
        )

    def render_markdown(self, raw_str: str) -> str:
        return md.markdown(raw_str, extensions=["nl2br", "tables"])

    def create_relation_definitions(
        self, definitions: list[rel.RelationTypeDefinition]
    ) -> list[dict]:
        vm_list = []
        for rel_def in definitions:
            vm_list.append(
                {
                    "type": rel_def.type,
                    "label": rel_def.display_name,
                    "directed": rel_def.directed,
                    "style": rel_def.style,
                }
            )

        return vm_list

    def show_edge(self, relation: rel.Relation) -> dict:
        return {
            "data": {
                "id": relation.id,
                "label": rel.RELATIONSHIP_DEFINITIONS[relation.type][
                    "display_name"
                ],
                "type": relation.type,
                "source": relation.source_id,
                "target": relation.target_id,
            }
        }

    @singledispatchmethod
    def show_node(self, arg) -> dict:
        raise NotImplementedError(
            f"type {type(arg)} is not implemented for 'presenter.show_node'"
        )

    @show_node.register
    def _(self, arg: chrobj.ChronicleObject):
        return {
            "data": {
                "id": arg.id,
                "label": arg.name,
                "type": arg.type,
                "href": f"/{arg.type}/{arg.id}",
            }
        }

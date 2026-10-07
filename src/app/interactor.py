"""this module maintains the core business logic"""

from slugify import slugify
import app.domain.chronicle_objects as chrobj
import app.domain.relations as rel
import app.database as db


class InvalidChronicleObjectError(Exception):
    """invalid chronicle object id"""

    def __init__(self, type_str: str, id_str: str):
        super().__init__(f'The {type_str} with id "f{id_str}" does not exist.')


class InvalidPersonError(InvalidChronicleObjectError):
    """invalid person id"""

    def __init__(self, id_str: str):
        super().__init__("person", id_str)


class Interactor:
    """
    this class coordinates the businiess logic between the different domain
    modules and classes
    """

    _chr_objs: dict[str, dict[str, chrobj.ChronicleObject]]

    def __init__(self):
        self._chr_objs = {}
        self._relations = {}

    def register_chronicle_object_types(self, types: list[str]):
        self._chr_objs = {}
        for tp in types:
            self._chr_objs[tp] = {}

    def register_chronicle_objects(
        self, obj_type: str, chr_obj_files: list[db.MarkdownFile]
    ):
        self._chr_objs[obj_type] = {}
        for file in chr_obj_files:
            lines = file.content.splitlines()
            name = (
                lines[0][2:]
                if lines and lines[0].startswith("# ")
                else file.path.stem
            )
            self._chr_objs[obj_type][file.path.stem] = chrobj.ChronicleObject(
                name=name, id=file.path.stem, type=obj_type
            )

    def register_relations(self, relations: list[rel.Relation]):
        self._relations = {}
        for relation in relations:
            self._relations[relation.id] = relation

    def add_chronicle_object(self, obj_type: str, name: str):
        obj = chrobj.ChronicleObject(name=name, id=slugify(name), type=obj_type)
        if obj.id in self._chr_objs[obj_type]:
            return None
        self._chr_objs[obj_type][obj.id] = obj
        return obj

    def get_chronicle_object_list(self, obj_type: str):
        return list(self._chr_objs[obj_type].values())

    def get_chronicle_object(self, obj_type: str, obj_id: str):
        if not obj_id in self._chr_objs[obj_type]:
            raise InvalidChronicleObjectError(obj_type, obj_id)
        return self._chr_objs[obj_type][obj_id]

    def add_relation(self, source_id: str, target_id: str, rel_type: str):
        rel_id = slugify(source_id + "-2-" + target_id)
        self._relations[rel_id] = rel.Relation(
            rel_type, rel_id, source_id, target_id
        )

    def delete_relation(self, relation_id: str):
        self._relations.pop(relation_id)

    def get_relations(self):
        return list(self._relations.values())

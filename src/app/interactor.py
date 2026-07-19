"""this module maintains the core business logic"""

from slugify import slugify
import app.domain.people as ppl
import app.domain.relations as rel
import app.database as db


class InvalidPersonError(Exception):
    """invalid person id"""

    def __init__(self, id_str: str):
        super().__init__(f'The person with id "f{id_str}" does not exist.')


class Interactor:
    """
    this class coordinates the businiess logic between the different domain
    modules and classes
    """

    def __init__(self):
        self._people = {}
        self._relations = {}

    def register_people(self, people_files: list[db.MarkdownFile]):
        self._people = {}
        for file in people_files:
            lines = file.content.splitlines()
            name = (
                lines[0][2:]
                if lines and lines[0].startswith("# ")
                else file.path.stem
            )
            self._people[file.path.stem] = ppl.Person(
                name=name, id=file.path.stem
            )

    def register_relations(self, relations: list[rel.Relation]):
        self._relations = {}
        for relation in relations:
            self._relations[relation.id] = relation

    def add_person(self, name: str) -> ppl.Person:
        person = ppl.Person(name=name, id=slugify(name))
        if person.id in self._people:
            return None
        self._people[person.id] = person
        return person

    def get_people(self) -> list[ppl.Person]:
        return list(self._people.values())

    def get_person(self, person_id: str):
        if not person_id in self._people:
            raise InvalidPersonError(person_id)
        return self._people[person_id]

    def add_relation(self, source_id: str, target_id: str, rel_type: str):
        rel_id = slugify(source_id + "-2-" + target_id)
        self._relations[rel_id] = rel.Relation(
            rel_type, rel_id, source_id, target_id
        )

    def delete_relation(self, relation_id: str):
        self._relations.pop(relation_id)

    def get_relations(self):
        return list(self._relations.values())

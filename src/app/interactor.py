"""this module maintains the core business logic"""

from slugify import slugify
import app.domain.people as ppl
import app.database as db


class Interactor:
    """
    this class coordinates the businiess logic between the different domain
    modules and classes
    """

    def register_people(self, people_files: list[db.MarkdownFile]):
        self._people = []
        for file in people_files:
            lines = file.content.splitlines()
            name = (
                lines[0][2:]
                if lines and lines[0].startswith("# ")
                else file.stem
            )
            self._people.append(ppl.Person(name=name, id=slugify(name)))

    def add_person(self, name: str) -> ppl.Person:
        person = ppl.Person(name=name, id=slugify(name))
        self._people.append(person)
        return person

    def get_people(self) -> list[ppl.Person]:
        return self._people

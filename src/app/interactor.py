"""this module maintains the core business logic"""

import pathlib as pl

import app.domain.people as ppl


class Interactor:
    """
    this class coordinates the businiess logic between the different domain
    modules and classes
    """

    def set_campaign_path(self, campaign_dir: pl.Path):
        self._campaign_dir = campaign_dir
        self._people = []

    def register_people(self):
        people_path = self._campaign_dir / "people"
        files = list(people_path.glob("*.md"))
        for file in files:
            content = file.read_text(encoding="utf-8")
            lines = content.splitlines()
            name = (
                lines[0][2:]
                if lines and lines[0].startswith("# ")
                else file.stem
            )
            self._people.append(ppl.Person(name=name))

    def get_people(self) -> list[ppl.Person]:
        return self._people

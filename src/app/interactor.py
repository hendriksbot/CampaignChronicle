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
        self._people = [ppl.Person(name=file.stem) for file in files]

    def get_people(self) -> list[ppl.Person]:
        return self._people

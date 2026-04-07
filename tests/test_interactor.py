"""this module tests the interactor module"""

import unittest as ut
from unittest.mock import Mock, patch
import tempfile
import pathlib as pl
import app.interactor as iactr
import app.domain.people as ppl


class TestGetPeople(ut.TestCase):

    def test_set_path(self):
        self.interactor = iactr.Interactor()
        self.interactor.set_campaign_path(pl.Path("path/to/dir"))

    def test_register_people_no_people(self):
        with tempfile.TemporaryDirectory() as tmp:
            campaign_path = pl.Path(tmp)
            people_dir = campaign_path / "people"
            people_dir.mkdir()

            self.interactor = iactr.Interactor()
            self.interactor.set_campaign_path(campaign_path)

            self.interactor.register_people()

            people_list = self.interactor.get_people()

            self.assertListEqual([], people_list)

    def test_register_people_two_persons(self):
        with tempfile.TemporaryDirectory() as tmp:
            campaign_path = pl.Path(tmp)
            people_dir = campaign_path / "people"
            people_dir.mkdir()

            (people_dir / "Alice.md").write_text("# Alice")
            (people_dir / "Bob.md").write_text("# Bob")

            self.interactor = iactr.Interactor()
            self.interactor.set_campaign_path(campaign_path)

            self.interactor.register_people()

            people_list = self.interactor.get_people()

            self.assertListEqual(
                [ppl.Person("Alice"), ppl.Person("Bob")], people_list
            )

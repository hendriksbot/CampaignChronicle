"""this module tests the interactor module"""

import unittest as ut
import tempfile
import pathlib
import app.interactor as iactr
import app.domain.people as ppl
import app.database as db


class TestGetPeople(ut.TestCase):

    def test_set_path(self):
        self.interactor = iactr.Interactor()

    def test_register_people_two_persons(self):
        db_people_list = [
            db.MarkdownFile(
                "alice", pathlib.Path("path/to/alice.md"), "# Alice"
            ),
            db.MarkdownFile("bob", pathlib.Path("path/to/bob.md"), "# Bob"),
        ]
        self.interactor = iactr.Interactor()
        self.interactor.register_people(db_people_list)
        people_list = self.interactor.get_people()

        self.assertListEqual(
            [ppl.Person("Alice", "alice"), ppl.Person("Bob", "bob")],
            people_list,
        )

    def test_re_register_people(self):
        db_people_list_a = [
            db.MarkdownFile(
                "alice", pathlib.Path("path/to/alice.md"), "# Alice"
            ),
            db.MarkdownFile("bob", pathlib.Path("path/to/bob.md"), "# Bob"),
        ]
        db_people_list_b = [
            db.MarkdownFile(
                "carla", pathlib.Path("path/to/carla.md"), "# Carla"
            ),
            db.MarkdownFile("dave", pathlib.Path("path/to/dave.md"), "# Dave"),
        ]
        self.interactor = iactr.Interactor()
        self.interactor.register_people(db_people_list_a)
        self.interactor.register_people(db_people_list_b)
        people_list = self.interactor.get_people()

        self.assertListEqual(
            [ppl.Person("Carla", "carla"), ppl.Person("Dave", "dave")],
            people_list,
        )

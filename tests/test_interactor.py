"""this module tests the interactor module"""

import unittest as ut
import pathlib
import app.interactor as iactr
import app.domain.chronicle_objects as chrobj
import app.domain.relations as rel
import app.database as db


class TestGetPeople(ut.TestCase):
    """test suite for people"""

    def setUp(self):
        self.interactor = iactr.Interactor()
        self.interactor.register_chronicle_object_types(["person"])

    def test_register_people_two_persons(self):
        db_people_list = [
            db.MarkdownFile(
                "alice", "# Alice", pathlib.Path("path/to/alice.md")
            ),
            db.MarkdownFile(
                "bob",
                "# Bob",
                pathlib.Path("path/to/bob.md"),
            ),
        ]
        self.interactor.register_chronicle_objects("person", db_people_list)
        people_list = self.interactor.get_chronicle_object_list("person")

        self.assertListEqual(
            [
                chrobj.ChronicleObject("Alice", "person:alice", "person"),
                chrobj.ChronicleObject("Bob", "person:bob", "person"),
            ],
            people_list,
        )

        self.assertEqual(
            chrobj.ChronicleObject("Alice", "person:alice", "person"),
            self.interactor.get_chronicle_object("person", "person:alice"),
        )

    def test_re_register_people(self):
        db_people_list_a = [
            db.MarkdownFile(
                "alice", "# Alice", pathlib.Path("path/to/alice.md")
            ),
            db.MarkdownFile("bob", "# Bob", pathlib.Path("path/to/bob.md")),
        ]
        db_people_list_b = [
            db.MarkdownFile(
                "carla", "# Carla", pathlib.Path("path/to/carla.md")
            ),
            db.MarkdownFile("dave", "# Dave", pathlib.Path("path/to/dave.md")),
        ]
        self.interactor.register_chronicle_objects("person", db_people_list_a)
        self.interactor.register_chronicle_objects("person", db_people_list_b)
        people_list = self.interactor.get_chronicle_object_list("person")

        self.assertListEqual(
            [
                chrobj.ChronicleObject("Carla", "person:carla", "person"),
                chrobj.ChronicleObject("Dave", "person:dave", "person"),
            ],
            people_list,
        )

    def test_fail_get_person(self):
        with self.assertRaises(iactr.InvalidChronicleObjectError):
            self.interactor.get_chronicle_object("person", "person:alice")


class TestRelations(ut.TestCase):
    """test suite for relations"""

    def setUp(self):
        self.interactor = iactr.Interactor()

    def test_add_relation(self):
        exp_relations = [rel.Relation("friend", "alice-2-bob", "alice", "bob")]
        self.interactor.add_relation("alice", "bob", "friend")

        act_relations = self.interactor.get_relations()

        self.assertListEqual(exp_relations, act_relations)

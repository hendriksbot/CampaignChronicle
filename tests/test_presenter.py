"""this module tests the presenter"""

import unittest as ut
import app.presenter as presenter
import app.domain.people as ppl
import app.domain.relations as rel
import app.view_models.vm_people as vm_ppl


class PresenterSetup(ut.TestCase):

    def setUp(self):
        self.presenter = presenter.Presenter()


class TestShowPerson(PresenterSetup):
    """test for the view model of a person"""

    def test_show(self):
        person = ppl.Person("Bob", "bob")
        content = "# Bob\n Bob ist eine coole Socke."
        exp_vm = vm_ppl.VMPerson(
            "bob", "<h1>Bob</h1>\n<p>Bob ist eine coole Socke.</p>", content
        )

        act_vm = self.presenter.show_person(person, content)

        self.assertEqual(exp_vm.markdown_rendered, act_vm.markdown_rendered)
        self.assertEqual(exp_vm, act_vm)


class TestViewModelEdge(PresenterSetup):
    """test for view model of an edge"""

    def test_relation(self):
        relation = rel.Relation(
            type="parent_of", id="a-2-b", source_id="alice", target_id="bob"
        )
        exp_vm_rel = {
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
        vm_rel = self.presenter.show_edge(relation)

        self.assertDictEqual(exp_vm_rel, vm_rel)


class TestViewModelNode(PresenterSetup):
    """test for view model of a node"""

    def test_type_not_implemented(self):
        class FakeType:
            foo = 42

        with self.assertRaises(NotImplementedError):
            self.presenter.show_node(FakeType())

    def test_person(self):
        person = ppl.Person("Bob", "bob")
        exp_vm_node = {
            "data": {
                "id": person.id,
                "label": person.name,
                "type": "person",
                "href": "/person/bob",
            }
        }

        vm_node = self.presenter.show_node(person)

        self.assertDictEqual(exp_vm_node, vm_node)

"""this module tests the presenter"""

import unittest as ut
import app.presenter as presenter
import app.domain.people as ppl
import app.view_models.vm_people as vm_ppl


class TestShowPerson(ut.TestCase):

    def setUp(self):
        self.presenter = presenter.Presenter()

    def test_show(self):
        person = ppl.Person("Bob", "bob")
        content = "# Bob\n Bob ist eine coole Socke."
        exp_vm = vm_ppl.VMPerson(
            "bob", "<h1>Bob</h1>\n<p>Bob ist eine coole Socke.</p>", content
        )

        act_vm = self.presenter.show_person(person, content)

        self.assertEqual(exp_vm.markdown_rendered, act_vm.markdown_rendered)
        self.assertEqual(exp_vm, act_vm)

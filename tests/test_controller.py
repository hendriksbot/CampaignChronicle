"""this module tests the controller of the app"""

import unittest as ut
from unittest.mock import Mock, MagicMock, patch
import pathlib
import app.controller as ctr
import app.guis.file_gui as file_gui
import app.domain.chronicle_objects as chrobj
import app.domain.relations as rel
import app.database as db


class TestCampaignSetup(ut.TestCase):

    def setUp(self):
        self.mock_gui = Mock()
        self.mock_interactor = Mock()
        self.controller = ctr.Controller(self.mock_gui, self.mock_interactor)


class TestSetCampaignFolder(TestCampaignSetup):
    """tests for setting the campaign folder"""

    @patch("app.guis.file_gui.DirectorySelectorGui.ask_for_directory")
    def test_request_cancelled(self, mock_ask_for_dir: Mock):

        mock_ask_for_dir.side_effect = file_gui.CancelledRequest()
        self.controller.request_set_campaign_folder()

        mock_ask_for_dir.assert_called_once_with(title="Select folder...")
        self.mock_gui.emit_dict.assert_not_called()

    @patch("app.controller.FileHandler.load_relations")
    @patch("app.controller.create_chronicle_dir")
    @patch("app.guis.file_gui.DirectorySelectorGui.ask_for_directory")
    def test_valid_dir(
        self, mock_ask_for_dir: Mock, stub_create_dir, stub_load_relation
    ):
        mock_ask_for_dir.return_value = pathlib.Path("path/to/dir/")
        self.controller.request_set_campaign_folder()

        mock_ask_for_dir.assert_called_once_with(title="Select folder...")
        self.mock_gui.emit_dict.assert_called_once_with(
            "campaign_set_status", {"is_active": True}
        )


class TestIndexReload(TestCampaignSetup):
    """test to reload index page"""

    def test_reload_index_without_campaign_path(self):

        self.controller.request_reload_index()

        self.mock_gui.emit_dict.assert_called_once_with(
            "campaign_set_status", {"is_active": False}
        )

    @patch("app.controller.FileHandler.load_relations")
    def test_reload_index_with_campaign_path(self, stub_load_relation):
        self.controller.register_campaign(pathlib.Path("path/to/dir/"))
        self.controller.request_reload_index()

        self.mock_gui.emit_dict.assert_called_once_with(
            "campaign_set_status", {"is_active": True}
        )


class TestShowPeople(TestCampaignSetup):
    """tests to show people"""

    def test_no_people(self):
        self.mock_interactor.get_chronicle_object_list.return_value = []
        self.controller.request_chronicle_object_list({"type": "person"})
        self.mock_gui.emit_dict.assert_called_once_with(
            "updated_chronicle_object_list",
            {"resource_type": "person", "objects": []},
        )

    def test_one_person(self):
        self.mock_interactor.get_chronicle_object_list.return_value = [
            chrobj.ChronicleObject("Bobby", "bobby", "person")
        ]
        self.controller.request_chronicle_object_list({"type": "person"})
        self.mock_gui.emit_dict.assert_called_once_with(
            "updated_chronicle_object_list",
            {
                "resource_type": "person",
                "objects": [{"name": "Bobby", "id": "bobby"}],
            },
        )


class TestCreateNewPerson(TestCampaignSetup):
    """tests for creating new person"""

    @patch("app.controller.FileHandler.load_relations")
    @patch("app.controller.create_chronicle_dir")
    @patch("app.database.FileDatabase")
    def test_new_person(self, file_database: MagicMock, stub_dir, stub_load):
        data = {
            "name": "Salazar",
            "type": "person",
            "markdown": "",
        }
        people_db = MagicMock()
        file_database.return_value = people_db
        file_path = MagicMock()
        people_path = MagicMock()
        people_path.__truediv__.return_value = file_path
        campaign_path = MagicMock()
        campaign_path.__truediv__.return_value = people_path
        self.controller.register_campaign(campaign_path)
        self.mock_interactor.add_chronicle_object.return_value = (
            chrobj.ChronicleObject("Salazar", "person:salazar", "person")
        )
        self.mock_interactor.get_chronicle_object_list.return_value = [
            chrobj.ChronicleObject("Salazar", "person:salazar", "person")
        ]
        people_db.exist_file.return_value = False
        self.controller.request_create_chronicle_object(data)
        people_db.create_file.assert_called_once_with(
            db.MarkdownFile("salazar", "# Salazar\n")
        )

        self.mock_gui.emit_dict.assert_called_once_with(
            "updated_chronicle_object_list",
            {
                "resource_type": "person",
                "objects": [{"name": "Salazar", "id": "person:salazar"}],
            },
        )

    @patch("app.controller.FileHandler.load_relations")
    @patch("app.controller.create_chronicle_dir")
    @patch("app.database.FileDatabase")
    def test_new_person_already_exists(
        self, file_database: MagicMock, stub_dir, stub_load
    ):
        data = {
            "name": "Salazar",
            "type": "person",
            "markdown": "",
        }
        people_db = MagicMock()
        file_database.return_value = people_db
        file_path = MagicMock()
        people_path = MagicMock()
        people_path.__truediv__.return_value = file_path
        campaign_path = MagicMock()
        campaign_path.__truediv__.return_value = people_path
        self.controller.register_campaign(campaign_path)
        self.mock_interactor.add_chronicle_object.return_value = None

        self.controller.request_create_chronicle_object(data)


class TestInitRelations(TestCampaignSetup):
    """tests for relation initialization"""

    @patch("app.domain.relations.get_relation_type_definitions")
    def test_initial_relation_request(self, mock_get_defs: MagicMock):

        self.mock_interactor.get_chronicle_object_list.return_value = [
            chrobj.ChronicleObject("Bobby", "person:bobby", "person"),
            chrobj.ChronicleObject("Alice", "person:alice", "person"),
        ]

        self.mock_interactor.get_relations.return_value = [
            rel.Relation("friend", "a2b", "person:alice", "person:bob")
        ]

        mock_get_defs.return_value = []

        self.controller.request_initial_relations_data()

        exp_vm = {
            "config": {"relation_definitions": []},
            "nodes": [
                {
                    "data": {
                        "id": "person:bobby",
                        "label": "Bobby",
                        "type": "person",
                        "href": "/person/person:bobby",
                    }
                },
                {
                    "data": {
                        "id": "person:alice",
                        "label": "Alice",
                        "type": "person",
                        "href": "/person/person:alice",
                    }
                },
            ],
            "edges": [
                {
                    "data": {
                        "id": "a2b",
                        "label": "befreundet",
                        "type": "friend",
                        "source": "person:alice",
                        "target": "person:bob",
                    }
                }
            ],
        }

        self.mock_gui.emit_dict.assert_called_once_with(
            "initialized_relations", exp_vm
        )

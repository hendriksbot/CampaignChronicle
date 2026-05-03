"""this module tests the controller of the app"""

import unittest as ut
from unittest.mock import Mock, MagicMock, patch
import pathlib
import app.controller as ctr
import app.guis.file_gui as file_gui
import app.domain.people as ppl


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

    @patch("app.guis.file_gui.DirectorySelectorGui.ask_for_directory")
    def test_valid_dir(self, mock_ask_for_dir: Mock):
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

    def test_reload_index_with_campaign_path(self):
        self.controller.register_campaign(pathlib.Path("path/to/dir/"))
        self.controller.request_reload_index()

        self.mock_gui.emit_dict.assert_called_once_with(
            "campaign_set_status", {"is_active": True}
        )


class TestShowPeople(TestCampaignSetup):
    """tests to show people"""

    def test_no_people(self):
        self.controller.register_campaign(pathlib.Path("path/to/dir/"))
        self.controller.request_people_list()
        self.mock_gui.emit_dict.assert_called_once_with(
            "updated_people_list", {"people": []}
        )

    def test_one_person(self):
        people_path = MagicMock()
        people_path.exists.return_value = True
        people_path.is_dir.return_value = True
        campaign_path = MagicMock()
        campaign_path.__truediv__.return_value = people_path
        self.controller.register_campaign(campaign_path)
        self.mock_interactor.get_people.return_value = [ppl.Person("Bobby")]
        self.controller.request_people_list()
        self.mock_gui.emit_dict.assert_called_once_with(
            "updated_people_list", {"people": [{"name": "Bobby"}]}
        )

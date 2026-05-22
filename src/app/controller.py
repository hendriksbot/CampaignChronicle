"""this module contains the controller logic of the app"""

import pathlib
from slugify import slugify
import app.ports.event_handler as evh_if
import app.guis.gui
import app.guis.file_gui as file_gui
import app.interactor as iactr
import app.domain.configs as configs
import app.database as db


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(self, gui: app.guis.gui.Gui, interactor: iactr.Interactor):
        self._gui = gui
        self._interactor = interactor
        self._campaign_path: configs.CampaignPath | None = None

    def start_app(self, is_debug_mode: bool = False):
        self._gui.run(is_debug_mode)

    def register_campaign(self, campaign_path: pathlib.Path):
        self._campaign_path = configs.CampaignPath(campaign_path)
        self._file_dbs = {
            "people": db.FileDatabase(self._campaign_path.people())
        }
        self._interactor.register_people(
            self._file_dbs["people"].register_files()
        )

    def request_reload_index(self):
        is_active = bool(self._campaign_path)
        self._gui.emit_dict("campaign_set_status", {"is_active": is_active})

    def request_set_campaign_folder(self):
        try:
            path = file_gui.DirectorySelectorGui().ask_for_directory(
                title="Select folder..."
            )
        except file_gui.CancelledRequest:
            return

        self.register_campaign(path)
        self._gui.emit_dict("campaign_set_status", {"is_active": True})

    def request_people_list(self):
        people_list = [
            {"name": person.name} for person in self._interactor.get_people()
        ]
        self._gui.emit_dict("updated_people_list", {"people": people_list})

    def request_create_person(self, data: dict):
        person = self._interactor.add_person(data["name"])
        slug = slugify(person.name)
        file_name = slug + ".md"
        file_path = self._campaign_path.people() / file_name
        file_path.write_text(f"# {person.name}\n", encoding="utf-8")

        self.request_people_list()

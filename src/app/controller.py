"""this module contains the controller logic of the app"""

import pathlib
import app.ports.event_handler as evh_if
import app.guis.gui
import app.guis.file_gui as file_gui
import app.interactor as iactr
import app.domain.configs as configs
import app.database as db
import app.presenter as presenter


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(self, gui: app.guis.gui.Gui, interactor: iactr.Interactor):
        self._gui = gui
        self._interactor = interactor
        self._presenter = presenter.Presenter()
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
            {"name": person.name, "id": person.id}
            for person in self._interactor.get_people()
        ]
        self._gui.emit_dict("updated_people_list", {"people": people_list})

    def request_create_person(self, data: dict):
        person = self._interactor.add_person(data["name"])
        if not person:
            return
        file = db.MarkdownFile(person.id, content=f"# {person.name}\n")
        if self._file_dbs["people"].exist_file(file):
            return
        else:
            self._file_dbs["people"].create_file(file)

        self.request_people_list()

    def request_person(self, data):
        try:
            person = self._interactor.get_person(data["id"])
        except iactr.InvalidPersonError:
            return

        try:
            file = self._file_dbs["people"].get_file(person.id)
        except FileNotFoundError:
            return

        vm = self._presenter.show_person(person, file_content=file.content)

        self._gui.emit_dict("updated_person", vars(vm))

    def render_markdown(self, raw_markdown: str):
        return self._presenter.render_markdown(raw_markdown)

    def save_markdown(self, entity_type: str, entity_id: str, content: str):
        try:
            file = self._file_dbs[entity_type].get_file(entity_id)
        except FileNotFoundError:
            return

        file.write(content)

        self.request_person({"id": entity_id})

    def request_initial_relations_data(self):
        people_list = self._interactor.get_people()

        nodes = [
            {
                "data": {
                    "id": person.id,
                    "label": person.name,
                    "type": "person",
                    "href": f"/person/{person.id}",
                }
            }
            for person in people_list
        ]
        vm = {
            "config": {"relation_definitions": []},
            "nodes": nodes,
            "edges": [],
        }
        self._gui.emit_dict("initialized_relations", vm)

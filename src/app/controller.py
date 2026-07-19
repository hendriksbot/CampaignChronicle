"""this module contains the controller logic of the app"""

import pathlib
import json
from packaging.version import Version
from dataclasses import asdict
import app.ports.event_handler as evh_if
import app.guis.gui
import app.guis.file_gui as file_gui
import app.interactor as iactr
import app.domain.configs as configs
import app.domain.relations as rel
import app.database as db
import app.presenter as presenter


def create_chronicle_dir(path: pathlib.Path):
    path.mkdir(parents=True, exist_ok=True)


class FileHandler:
    """temp concept for better testability"""

    _campaign_path: configs.CampaignPath | None = None

    def bind_campaign_path(self, path: configs.CampaignPath):
        self._campaign_path = path

    def load_relations(self) -> list[rel.Relation]:
        path = self._campaign_path.chronicle() / "relations.json"
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        file_version = Version(data.get("__version", "0.0.0"))
        if file_version.major != rel.RELATION_VERSION.major:
            raise ValueError(
                f"Unsupported relation format version "
                f"{file_version}. "
                f"Expected major version "
                f"{rel.RELATION_VERSION.major}"
            )

        return [rel.Relation(**relation) for relation in data["relations"]]

    def save_relations(self, relations: list[rel.Relation]):
        path = self._campaign_path.chronicle() / "relations.json"
        data = {
            "__version": str(rel.RELATION_VERSION),
            "relations": [asdict(relation) for relation in relations],
        }

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(self, gui: app.guis.gui.Gui, interactor: iactr.Interactor):
        self._gui = gui
        self._interactor = interactor
        self._presenter = presenter.Presenter()
        self._campaign_path: configs.CampaignPath | None = None
        self._file_handler = FileHandler()

    def start_app(self, is_debug_mode: bool = False):
        self._gui.run(is_debug_mode)

    def register_campaign(self, campaign_path: pathlib.Path):
        self._campaign_path = configs.CampaignPath(campaign_path)
        self._file_handler.bind_campaign_path(self._campaign_path)
        create_chronicle_dir(self._campaign_path.chronicle())
        self._file_dbs = {
            "people": db.FileDatabase(self._campaign_path.people())
        }
        self._interactor.register_people(
            self._file_dbs["people"].register_files()
        )
        self._interactor.register_relations(self._file_handler.load_relations())

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

    def _create_edges_list(self) -> list:
        return [
            self._presenter.show_edge(relation)
            for relation in self._interactor.get_relations()
        ]

    def _create_graph_config(self) -> dict:
        definitions = rel.get_relation_type_definitions()
        return {
            "relation_definitions": self._presenter.create_relation_definitions(
                definitions
            )
        }

    def request_initial_relations_data(self):
        people_list = self._interactor.get_people()

        nodes = [self._presenter.show_node(person) for person in people_list]
        vm = {
            "config": self._create_graph_config(),
            "nodes": nodes,
            "edges": self._create_edges_list(),
        }
        self._gui.emit_dict("initialized_relations", vm)

    def request_create_relation(self, data):
        self._interactor.add_relation(
            data["source_id"],
            data["target_id"],
            data["type"],
        )
        nodes = [
            self._presenter.show_node(person)
            for person in self._interactor.get_people()
        ]
        vm = {
            "nodes": nodes,
            "edges": self._create_edges_list(),
        }
        self._file_handler.save_relations(self._interactor.get_relations())
        self._gui.emit_dict("updated_relations", vm)

    def request_delete_relation(self, relation_id: str):
        self._interactor.delete_relation(relation_id)
        nodes = [
            self._presenter.show_node(person)
            for person in self._interactor.get_people()
        ]
        vm = {
            "nodes": nodes,
            "edges": self._create_edges_list(),
        }
        self._file_handler.save_relations(self._interactor.get_relations())
        self._gui.emit_dict("updated_relations", vm)

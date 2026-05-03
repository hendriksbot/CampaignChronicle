"""this module contains the controller logic of the app"""

import pathlib
import app.ports.event_handler as evh_if
import app.guis.gui
import app.guis.file_gui as file_gui
import app.interactor as iactr


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(self, gui: app.guis.gui.Gui, interactor: iactr.Interactor):
        self._gui = gui
        self._interactor = interactor
        self._campaign_path: pathlib.Path | None = None

    def start_app(self, is_debug_mode: bool = False):
        self._gui.run(is_debug_mode)

    def register_campaign(self, campaign_path: pathlib.Path):
        self._campaign_path = campaign_path
        self._interactor.set_campaign_path(campaign_path)
        self._interactor.register_people()

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
        people_path = self._campaign_path / "people"
        people_list = []
        if people_path.exists() and people_path.is_dir():
            people = self._interactor.get_people()
            people_list = [{"name": person.name} for person in people]

        self._gui.emit_dict("updated_people_list", {"people": people_list})

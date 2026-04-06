"""this module contains the controller logic of the app"""

import pathlib
import app.ports.event_handler as evh_if
import app.guis.gui
import app.guis.file_gui as file_gui


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(
        self,
        gui: app.guis.gui.Gui,
    ):
        self._gui = gui
        self._campaign_path: pathlib.Path | None = None

    def start_app(self, is_debug_mode: bool = False):
        self._gui.run(is_debug_mode)

    def set_campaign_path(self, campaign_path: pathlib.Path):
        self._campaign_path = campaign_path

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

        self._campaign_path = path
        self._gui.emit_dict("campaign_set_status", {"is_active": True})

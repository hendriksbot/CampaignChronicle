"""this module contains the controller logic of the app"""

import app.ports.event_handler as evh_if
import app.guis.gui


class Controller(evh_if.EventHandlerInterface):
    """the controller class coordinates the interactor, presenters and gui"""

    def __init__(
        self,
        gui: app.guis.gui.Gui,
    ):
        self._gui = gui

    def start_app(self, is_debug_mode: bool = False):
        self._gui.run(is_debug_mode)

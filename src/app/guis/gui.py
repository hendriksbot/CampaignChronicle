"""this module provides an abstract gui"""

from abc import ABC, abstractmethod
import app.ports.event_handler as evh_if


class Gui(ABC):
    """abstract gui class"""

    def __init__(self):
        self._evh = None

    def bind_event_handler(self, evh: evh_if.EventHandlerInterface):
        self._evh = evh

    @abstractmethod
    def run(self, is_debug_mode: bool):
        """abstract run"""

    @abstractmethod
    def emit_dict(self, event: str, data: dict):
        """abstract emit dict"""

"""this module provides the event handler interface"""

from abc import ABC, abstractmethod


class EventHandlerInterface(ABC):
    """identifies all event interfaces"""

    @abstractmethod
    def request_reload_index(self):
        pass

    @abstractmethod
    def request_set_campaign_folder(self):
        pass

    @abstractmethod
    def request_people_list(self):
        pass

    @abstractmethod
    def request_create_person(self, data: dict):
        pass

    @abstractmethod
    def request_person(self, data: dict):
        pass

    @abstractmethod
    def render_markdown(self, raw_markdown: str) -> str:
        pass

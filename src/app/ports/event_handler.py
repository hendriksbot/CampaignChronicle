"""this module provides the event handler interface"""

from abc import ABC, abstractmethod


class EventHandlerInterface(ABC):
    """identifies all event interfaces"""

    @abstractmethod
    def request_set_campaign_folder(self):
        pass

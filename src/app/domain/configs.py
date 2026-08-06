"""contains config classes for the apps"""

from dataclasses import dataclass
import pathlib


@dataclass
class CampaignPath:
    """manages the directory path of the campaign"""

    campaign: pathlib.Path | None = None

    def object(self, obj_path: str):
        return self.campaign / obj_path

    def people(self) -> pathlib.Path:
        return self.campaign / "people"

    def chronicle(self) -> pathlib.Path:
        return self.campaign / ".chronicle"

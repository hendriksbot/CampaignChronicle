"""contains config classes for the apps"""

from dataclasses import dataclass
import pathlib


@dataclass
class CampaignPath:
    campaign: pathlib.Path | None = None

    def people(self) -> pathlib.Path:
        return self.campaign / "people"

    def chronicle(self) -> pathlib.Path:
        return self.campaign / ".chronicle"

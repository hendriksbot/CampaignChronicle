"""module for the app databases"""

import pathlib
from dataclasses import dataclass


@dataclass
class MarkdownFile:
    name: str
    path: pathlib.Path
    content: str


class FileDatabase:
    """database that is file and directory based"""

    def __init__(self, path_to_src: pathlib.Path):
        self._path_to_src = path_to_src

    def register_files(self) -> list[MarkdownFile]:
        files = self._path_to_src.glob("*.md")
        registered_files = []
        for file in files:
            registered_files.append(
                MarkdownFile(file.stem, file, file.read_text(encoding="utf-8"))
            )

        return registered_files

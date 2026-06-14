"""module for the app databases"""

import pathlib
from dataclasses import dataclass


@dataclass
class MarkdownFile:
    name: str
    content: str = ""
    path: pathlib.Path | None = None


class FileDatabase:
    """database that is file and directory based"""

    def __init__(self, path_to_src: pathlib.Path):
        self._path_to_src = path_to_src

    def register_files(self) -> list[MarkdownFile]:
        files = self._path_to_src.glob("*.md")
        registered_files = []
        for file in files:
            registered_files.append(
                MarkdownFile(
                    name=file.stem,
                    path=file,
                    content=file.read_text(encoding="utf-8"),
                )
            )

        return registered_files

    def exist_file(self, file: MarkdownFile) -> bool:
        file_path = self._path_to_src / f"{file.name}.md"
        return file_path.exists()

    def get_file(self, name: str) -> MarkdownFile:
        file = self._path_to_src / f"{name}.md"
        return MarkdownFile(
            name=file.stem, path=file, content=file.read_text(encoding="utf-8")
        )

    def create_file(self, file: MarkdownFile):
        file_path = self._path_to_src / f"{file.name}.md"
        file_path.write_text(data=file.content, encoding="utf-8")

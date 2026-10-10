"""module for the app databases"""

import pathlib
import frontmatter
from dataclasses import dataclass


@dataclass
class MarkdownMeta:
    id: str | None


@dataclass
class MarkdownFile:
    """represents a markdown file which is used to store the database content"""

    name: str
    meta: MarkdownMeta
    content: str = ""
    path: pathlib.Path | None = None

    def write(self, content: str = ""):
        if not content:
            content = self.content
        if self.path:
            document = frontmatter.Post(content=content, **vars(self.meta))
            self.path.write_text(
                data=frontmatter.dumps(document), encoding="utf-8"
            )


class FileDatabase:
    """database that is file and directory based"""

    def __init__(self, path_to_src: pathlib.Path):
        self._path_to_src = path_to_src

    def register_files(self) -> list[MarkdownFile]:
        files = self._path_to_src.glob("*.md")
        registered_files = []
        for file in files:
            registered_files.append(load_markdown(file))

        return registered_files

    def exist_file(self, file: MarkdownFile) -> bool:
        file_path = self._path_to_src / f"{file.name}.md"
        return file_path.exists()

    def get_file(self, name: str) -> MarkdownFile:
        file = self._path_to_src / f"{name}.md"
        return load_markdown(file)

    def create_file(self, file: MarkdownFile):
        file.path = self._path_to_src / f"{file.name}.md"
        file.write()


def load_markdown(file: pathlib.Path) -> MarkdownFile:
    document = frontmatter.loads(file.read_text(encoding="utf-8"))
    return MarkdownFile(
        name=file.stem,
        path=file,
        meta=MarkdownMeta(id=document.get("id", None)),
        content=document.content,
    )

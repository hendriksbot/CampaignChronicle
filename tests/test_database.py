"""tests for database"""

import unittest as ut
from unittest.mock import MagicMock
import pathlib
import tempfile
import frontmatter
import app.database as db


class TestFileDatabase(ut.TestCase):
    """tests for file database"""

    def test_register_no_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = pathlib.Path(tmp)
            file_db = db.FileDatabase(db_path)

            file_list = file_db.register_files()

            self.assertListEqual([], file_list)

    def test_register_one_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = pathlib.Path(tmp)
            file_db = db.FileDatabase(db_path)

            (db_path / "alice.md").write_text("# Alice")

            file_list = file_db.register_files()

            self.assertEqual(1, len(file_list))
            self.assertEqual("alice", file_list[0].name)
            self.assertEqual(db_path / "alice.md", file_list[0].path)
            self.assertEqual("# Alice", file_list[0].content)

    def test_create_new_file(self):

        file_path = MagicMock()
        file_path.exists.return_value = False
        db_path = MagicMock()
        db_path.__truediv__.return_value = file_path
        file_db = db.FileDatabase(db_path)
        file = db.MarkdownFile(
            name="salazar", meta=db.MarkdownMeta(id="person:salazar")
        )
        self.assertFalse(file_db.exist_file(file))

        exp_document = frontmatter.Post("", id="person:salazar")
        file_db.create_file(file)
        file_path.write_text.assert_called_once_with(
            data=frontmatter.dumps(exp_document), encoding="utf-8"
        )

    def test_create_new_file_exists(self):
        file_path = MagicMock()
        file_path.exists.return_value = True
        db_path = MagicMock()
        db_path.__truediv__.return_value = file_path
        file_db = db.FileDatabase(db_path)
        file = db.MarkdownFile(
            name="salazar", meta=db.MarkdownMeta(id="person:salazar")
        )
        self.assertTrue(file_db.exist_file(file))

    def test_get_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = pathlib.Path(tmp)
            file_db = db.FileDatabase(db_path)
            document = frontmatter.Post(content="# Alice", id="person:alice")
            (db_path / "alice.md").write_text(frontmatter.dumps(document))

            act_file = file_db.get_file("alice")

            self.assertEqual(
                db.MarkdownFile(
                    "alice",
                    db.MarkdownMeta(id="person:alice"),
                    "# Alice",
                    db_path / "alice.md",
                ),
                act_file,
            )

    def test_get_file_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = pathlib.Path(tmp)
            file_db = db.FileDatabase(db_path)

            with self.assertRaises(FileNotFoundError):
                file_db.get_file("alice")

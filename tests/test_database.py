"""tests for database"""

import unittest as ut
from unittest.mock import MagicMock
import pathlib
import tempfile
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
        file = db.MarkdownFile(name="salazar")
        self.assertFalse(file_db.exist_file(file))

        file_db.create_file(file)
        file_path.write_text.assert_called_once_with(
            data=file.content, encoding="utf-8"
        )

    def test_create_new_file_exists(self):
        file_path = MagicMock()
        file_path.exists.return_value = True
        db_path = MagicMock()
        db_path.__truediv__.return_value = file_path
        file_db = db.FileDatabase(db_path)
        file = db.MarkdownFile(name="salazar")
        self.assertTrue(file_db.exist_file(file))

"""tests for database"""

import unittest as ut
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

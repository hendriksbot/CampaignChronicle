"""This module implements file and directory browser guis"""

import tkinter as tk
from tkinter import filedialog
import pathlib

import app.utils.exceptions as exceptions


class CancelledRequest(exceptions.AppError):
    pass


class DirectorySelectorGui:
    """gui to select a directory"""

    def ask_for_directory(self, title: str) -> pathlib.Path:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.update()
        folder = filedialog.askdirectory(title=title)
        if not folder:
            raise CancelledRequest()
        dir_path = pathlib.Path(folder)
        root.destroy()
        return dir_path

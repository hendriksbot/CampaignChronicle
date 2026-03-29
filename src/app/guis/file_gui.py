"""This module implements file and directory browser guis"""

import tkinter as tk
from tkinter import filedialog
import pathlib


class DirectorySelectorGui:

    def ask_for_directory(self, title: str) -> pathlib.Path:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.update()
        dir_path = pathlib.Path(filedialog.askdirectory(title=title))
        root.destroy()
        return dir_path

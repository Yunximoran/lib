from tkinter import filedialog
import os


# from ._baseui import _BaseUI

def choose_file():
    file_path = filedialog.askopenfilename()
    filename = os.path.basename(file_path)
    return filename, file_path

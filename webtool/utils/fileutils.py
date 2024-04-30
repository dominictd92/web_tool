#
# This is a utility file for all file methods.
#   Creating, retrieving, editing, etc. should be done here.
#

import sys
from os import getcwd, remove
from os.path import join, basename, isfile
from pathlib import Path
from subprocess import call
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo, askokcancel
from shutil import copyfile

from openpyxl import Workbook

from webtool.constants.constants import default_search_filename, excel_ext, text_ext
from webtool.config.configs import INSTALLATION_LOCATION
from webtool.utils.systemsutil import get_os


# Get the base path of the system for files and logger
def get_base_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, INSTALLATION_LOCATION):
        # system is running from an application
        base_path = getattr(sys, INSTALLATION_LOCATION)
    else:
        # system is running from source
        base_path = str(Path(getcwd()).absolute())

    return base_path


def get_default_search_file():
    return get_base_path() + default_search_filename


# method to select to save a file with a specific name
def select_save_name(default_name: str, extension: str, extensions: tuple):
    save_file = asksaveasfilename(
        title="Enter file name", initialfile=default_name, initialdir=getcwd(),
        confirmoverwrite=True, defaultextension=extension, filetypes=extensions
    )
    return save_file


# method to export data to an excel file
def export_xlsx(dataset, default_filename: str):
    if isinstance(dataset, list):
        workbook = Workbook()
        sheet = workbook.active
        row = 1
        for data in dataset:
            sheet[f'A{row}'] = data
            row += 1

        filename = select_save_name(default_name=default_filename, extension=".xlsx", extensions=excel_ext)
        workbook.save(filename + ".xlsx")
        workbook.close()
        showinfo("Information", "The excel file has been saved.")
    else:
        showinfo("Error", "The excel file could not be saved because the data was invalid.")


# method to export data to a text file
def export_txt(dataset, default_filename: str):
    if isinstance(dataset, str):
        filename = select_save_name(default_name=default_filename, extension=".txt", extensions=text_ext)
        text_file = open(filename + ".txt", "x")
        text_file.write(dataset)
        text_file.close()
        showinfo("Information", "The txt file has been saved.")
    else:
        showinfo("Error", "The txt file could not be saved because the data was invalid.")


def open_dir(directory=""):
    if directory == "":
        directory = getcwd()

    current_platform = get_os()

    match current_platform:
        case "macOS":
            call(["open", directory])
        case "Windows":
            call(["explorer", directory])
        case None:
            showinfo("Error", f"The system you're using is not recognized: {current_platform}")


# Function to upload a file to a specific directory for configurations
def upload_file(extensions: tuple, directory: str = None, filename: str = None):
    original_file = askopenfilename(
        title="Select a file to upload", initialdir=getcwd(), filetypes=extensions)

    if original_file is not None and original_file != "":
        if directory is not None:
            upload_directory = directory
        else:
            upload_directory = get_base_path()

        if filename is not None:
            new_file = join(upload_directory, filename)
        else:
            new_file = join(upload_directory, basename(original_file))

        if isfile(new_file):
            overwrite = askokcancel("Overwrite file?",
                                    "Overwrite the existing file? (All of the information will be deleted)")
            if not overwrite:
                return
            else:
                remove(new_file)

        copyfile(original_file, new_file)
        showinfo("Successful", "File was uploaded")

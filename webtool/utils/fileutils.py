#
# This is a utility file for all file methods.
#   Creating, retrieving, editing, etc. should be done here.
#
import os
import platform

import subprocess

import openpyxl

import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

from webtool.constants.constants import *
from webtool.utils.systemsutil import get_os


# method to select to save a file with a specific name
def select_save_name(default_name: str, extension: str, extensions: tuple):
    save_file = filedialog.asksaveasfilename(
        title="Enter file name", initialfile=default_name, initialdir=os.getcwd(),
        confirmoverwrite=True, defaultextension=extension, filetypes=extensions
    )
    return save_file


# method to select a file from the user's device
def select_open_name(default_filename: str, extensions: tuple):
    selected_file = filedialog.askopenfilename(
        initialdir=os.getcwd(), title="Select a File", filetypes=extensions)
    if selected_file is None or selected_file == '':
        return default_filename
    else:
        return selected_file


# method to export data to an excel file
def export_xlsx(dataset, default_filename: str):
    if isinstance(dataset, list):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        row = 1
        for data in dataset:
            sheet[f'A{row}'] = data
            row += 1

        filename = select_save_name(default_name=default_filename, extension=".xlsx", extensions=excel_ext)
        workbook.save(filename + ".xlsx")
        workbook.close()
        messagebox.showinfo("Information", "The excel file has been saved.")
    else:
        messagebox.showinfo("Error", "The excel file could not be saved because the data was invalid.")


# method to export data to a text file
def export_txt(dataset, default_filename: str):
    if isinstance(dataset, str):
        filename = select_save_name(default_name=default_filename, extension=".txt", extensions=text_ext)
        text_file = open(filename + ".txt", "x")
        text_file.write(dataset)
        text_file.close()
        messagebox.showinfo("Information", "The txt file has been saved.")
    else:
        messagebox.showinfo("Error", "The txt file could not be saved because the data was invalid.")


def open_dir(directory=""):
    if directory == "":
        directory = os.getcwd()

    current_platform = get_os()

    match current_platform:
        case "macOS":
            subprocess.call(["open", directory])
        case "Windows":
            subprocess.call(["explorer", directory])
        case None:
            messagebox.showinfo("Error", "The system you're using is not recognized: " + current_platform)

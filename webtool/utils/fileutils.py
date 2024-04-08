#
# This is a utility file for all file methods.
#   Creating, retrieving, editing, etc. should be done here.
#

import openpyxl

import tkinter.messagebox as messagebox


def export_xlsx(filename, dataset):
    if isinstance(dataset, list):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        row = 1
        for data in dataset:
            sheet[f'A{row}'] = data
            row += 1
        if filename == '':
            workbook.save("Exported_Data.xlsx")
        else:
            workbook.save(filename + ".xlsx")
        workbook.close()
        messagebox.showinfo("Information", "The excel file has been saved.")
    else:
        messagebox.showinfo("Error", "The excel file could not be saved because the data was invalid.")


def export_txt(filename, dataset):
    if isinstance(dataset, str):
        if filename == '':
            text_file = open("Exported_Data.txt", "x")
        else:
            text_file = open(filename + ".txt", "x")
        text_file.write(dataset)
        text_file.close()
        messagebox.showinfo("Information", "The txt file has been saved.")
    else:
        messagebox.showinfo("Error", "The txt file could not be saved because the data was invalid.")

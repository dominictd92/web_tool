#
# This is a webscrapper that can cycle through any
#   list of urls and look for a specific string within those urls.
#

import os
import threading

import requests

import openpyxl

import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from tkinter import ttk

from webtool.widget.Hint import Hint
from webtool.widget.ScrollableFrame import ScrollableFrame
from webtool.constants.constants import *
from webtool.utils.fileutils import export_txt, export_xlsx
from webtool.utils.loggingutils import get_logger
from webtool.utils.validationutils import validate_int
from webtool.utils.webutils import return_webpage
from webtool.utils.widgetutils import activate


# the class for the webscrapper with all needed methods within it
class Webscrapper(tk.Frame):
    # class variables
    default_filename = "search.xlsx"
    found_text_formatter = " - Found Text: '{search_string}' on {url} {find_count} time(s)\n"
    history_text_formatter = "Searches: {searches}\n{results}" + ("-" * 15) + "\n"

    notes = (
        "- This webscrapper can traverse through any list of urls and search for any text.\n"
        "- The file has to be in an excel format and listed in the first column.\n"
        "- The default file to be searched is 'search.xlsx' in the program's directory if no file is selected.\n"
        "- To search for multiple things, use '+' with no spaces between the '+' and the search text."
        "- Hover over items with '\u2071' alongside it.\n"
        "- For assistance, email Dominic Dangerfield at dominic.t.dangerfield@gmail.com.\n")

    def __init__(self, parent, root):
        self.logger = get_logger()
        super().__init__(parent)

        self.scrollable_frame = ScrollableFrame(self)

        # Variables used throughout the webscrapper
        self.found_results = []
        self.filename = tk.StringVar()
        self.filename.set(self.default_filename)
        self.input_variable = tk.StringVar()
        self.completion_text = tk.StringVar()
        self.completion_text.set("Results: ")
        note_text = tk.StringVar()
        note_text.set(self.notes)
        self.stop_variable = tk.BooleanVar()
        self.stop_variable.set(False)
        # variables for options
        self.specific_tags = tk.StringVar()
        self.specific_tags.set("Look for specific tags (In development...)")
        self.case_sensitive = tk.IntVar()
        self.auto_retry_urls = tk.IntVar()
        self.force_retry_urls = tk.IntVar()
        self.default_timeout = tk.IntVar()

        # Webscrapper frames
        #   Note frame
        note_frame = tk.Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=2)
        note_frame.grid(row=0, sticky=tk.EW)

        #   Search frame
        search_frame = tk.Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=2)
        search_frame.grid(row=1, sticky=tk.EW)

        #   Options frame
        options_frame = tk.Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=2)
        options_frame.grid(row=2, sticky=tk.EW)

        #   Buttons frame
        button_frame = tk.Frame(self.scrollable_frame)
        button_frame.grid(row=3, sticky=tk.EW)

        #   Results frame
        self.results_labelframe = tk.LabelFrame(self.scrollable_frame, text=self.completion_text.get(), height=200)
        self.results_labelframe.grid(row=4, sticky=tk.EW)
        self.results_labelframe.grid_rowconfigure(0, weight=1)
        self.results_labelframe.grid_columnconfigure(0, weight=1)
        self.results_labelframe.grid_propagate(False)

        #   Skipped urls frame
        skipped_labelframe = tk.LabelFrame(self.scrollable_frame, text="Skipped URLs:", height=200)
        skipped_labelframe.grid(row=5, sticky=tk.EW)
        skipped_labelframe.grid_rowconfigure(0, weight=1)
        skipped_labelframe.grid_columnconfigure(0, weight=1)
        skipped_labelframe.grid_propagate(False)

        #   History frame
        history_labelframe = tk.LabelFrame(self.scrollable_frame, text="History:", height=200)
        history_labelframe.grid(row=6, sticky=tk.EW)
        history_labelframe.grid_rowconfigure(0, weight=1)
        history_labelframe.grid_columnconfigure(0, weight=1)
        history_labelframe.grid_propagate(False)

        # Widgets within the frames
        #   Note frame
        self.notes_label_text = tk.StringVar()
        self.notes_label_text.set(collapsible_texts[0].format(object="Notes"))
        note_label_label = tk.Label(
            note_frame, textvariable=self.notes_label_text, anchor=tk.W, justify=tk.LEFT, cursor='hand2')
        note_label_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        note_collapsible_frame = tk.Frame(note_frame)
        note_collapsible_frame.grid(row=1, sticky=tk.EW)

        note_label = tk.Label(note_collapsible_frame, textvariable=note_text, wraplength=680, justify=tk.LEFT)
        note_label.grid(row=0, column=0, columnspan=5, padx=10, pady=(0, 10))

        note_label_label.bind(
            '<Button-1>',
            lambda e: activate(note_collapsible_frame, self.notes_label_text, "Notes"))

        # start with the notes collapsed
        activate(note_collapsible_frame, self.notes_label_text, "Notes")

        #   Search frame
        search_label = tk.Label(search_frame, text="Search Settings")
        search_label.grid(row=0, column=0, sticky=tk.W, padx=(5, 0), pady=5)

        select_file_label = tk.Label(search_frame, text="URL File:", justify=tk.LEFT, anchor=tk.W)
        select_file_label.grid(row=1, column=0, padx=(15, 5), pady=5, sticky=tk.W)

        file_label = tk.Label(search_frame, textvariable=self.filename, justify=tk.LEFT, anchor=tk.W)
        file_label.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky=tk.W)

        file_button = tk.Button(search_frame, text="Browse Files", width=10, command=self.select_file)
        file_button.grid(row=2, column=0, padx=(15, 5), pady=5, sticky=tk.W)

        clear_file_button = tk.Button(search_frame, text="Clear File", width=10,
                                      command=lambda: self.filename.set(self.default_filename))
        clear_file_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        search_label = tk.Label(search_frame, text="Search terms: ")
        search_label.grid(row=3, column=0, sticky=tk.W, padx=(15, 5), pady=5)

        search_entry = ttk.Entry(search_frame, textvariable=self.input_variable, width=50, justify=tk.LEFT)
        search_entry.grid(row=3, column=1, columnspan=4, sticky=tk.W, padx=5, pady=5)

        #   Options frame
        options_label_text = tk.StringVar()
        options_label_text.set(collapsible_texts[0].format(object="Options"))
        options_label_label = tk.Label(
            options_frame, textvariable=options_label_text, anchor=tk.W, justify=tk.LEFT, cursor='hand2')
        options_label_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        options_collapsible_frame = tk.Frame(options_frame)
        options_collapsible_frame.grid(row=1, sticky=tk.EW)

        specific_tags_label = tk.Label(options_collapsible_frame, text="HTML tags \u2071")
        specific_tags_label.grid(row=0, column=0, sticky=tk.W, padx=(15, 5), pady=5)

        Hint(specific_tags_label, "In development...")

        option_case_sensitive = tk.Checkbutton(options_collapsible_frame, text="Case Sensitive",
                                               variable=self.case_sensitive, onvalue=1, offvalue=0)
        option_case_sensitive.grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)

        specific_tags_entry = ttk.Entry(options_collapsible_frame, textvariable=self.specific_tags,
                                        width=50, justify=tk.LEFT, state=tk.DISABLED)
        specific_tags_entry.grid(row=0, column=1, columnspan=4, sticky=tk.W, padx=5, pady=5)

        retry_urls_label = tk.Label(options_collapsible_frame, text="Retry Urls \u2071")
        retry_urls_label.grid(row=1, column=0, sticky=tk.W, padx=(15, 5), pady=5)

        Hint(retry_urls_label, "When to retry URLs after timeout")

        option_auto_retry_urls = tk.Checkbutton(options_collapsible_frame, text="After finishing",
                                                variable=self.auto_retry_urls, onvalue=1, offvalue=0)
        option_auto_retry_urls.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        option_force_retry_urls = tk.Checkbutton(options_collapsible_frame, text="Now (ignoring Excel file)",
                                                 variable=self.force_retry_urls, onvalue=1, offvalue=0)
        option_force_retry_urls.grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)

        option_default_timeout = tk.Checkbutton(
            options_collapsible_frame, text="Default Timeout", variable=self.default_timeout,
            onvalue=1, offvalue=0, command=lambda: self.toggle_default_retries())
        option_default_timeout.grid(row=2, column=0, sticky=tk.W, padx=(15, 5), pady=5)

        option_retry_seconds_label = tk.Label(options_collapsible_frame, text="Seconds before timeout \u2071")
        option_retry_seconds_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        Hint(option_retry_seconds_label, "Default: 3, Min: 2, Max: 6")

        reg_option_retry_seconds_entry = (options_collapsible_frame.register(validate_int),
                                          '%P', '%V', '2', '6')

        self.option_retry_seconds_entry = ttk.Entry(
            options_collapsible_frame, width=3, justify=tk.LEFT,
            validate=tk.ALL, validatecommand=reg_option_retry_seconds_entry)
        self.option_retry_seconds_entry.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.option_retry_seconds_entry.insert(0, "3")

        option_retry_quantity_label = tk.Label(options_collapsible_frame, text="Number of retries \u2071")
        option_retry_quantity_label.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)

        Hint(option_retry_quantity_label, "Default: 3, Min: 0, Max: 5")

        reg_option_retry_quantity_entry = (options_collapsible_frame.register(validate_int),
                                           '%P', '%V', '0', '5')

        self.option_retry_quantity_entry = ttk.Entry(
            options_collapsible_frame, width=3, justify=tk.LEFT,
            validate=tk.ALL, validatecommand=reg_option_retry_quantity_entry)
        self.option_retry_quantity_entry.grid(row=2, column=4, columnspan=4, sticky=tk.W, padx=5, pady=5)
        self.option_retry_quantity_entry.insert(0, "3")

        options_label_label.bind(
            "<Button-1>",
            lambda e: activate(options_collapsible_frame, options_label_text, "Options"))

        # start with the options collapsed
        activate(options_collapsible_frame, options_label_text, "Options")

        #   Buttons frame
        self.search_button = tk.Button(
            button_frame, text="Search", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: False if not self.validate_values() else threading.Thread(target=self.scrape).start())
        self.search_button.grid(row=0, column=0, padx=10, pady=5)

        self.stop_button = tk.Button(
            button_frame, text="Stop", state=tk.DISABLED, width=10, fg="black", disabledforeground="black",
            command=lambda: self.stop_variable.set(True))
        self.stop_button.grid(row=0, column=1, padx=10, pady=5)

        self.export_results_button = tk.Button(
            button_frame, text="Export Results", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: threading.Thread(target=export_xlsx(filename='', dataset=self.found_results)).start())
        self.export_results_button.grid(row=0, column=2, padx=10, pady=5)

        export_history_button = tk.Button(
            button_frame, text="Export History", width=10, fg="black", disabledforeground="black",
            command=lambda: threading.Thread(
                    target=export_txt(filename='', dataset=self.history_text.get("1.0", tk.END))).start())
        export_history_button.grid(row=0, column=3, padx=10, pady=5)

        quit_button = tk.Button(
            button_frame, text="Quit", width=10, fg="black", disabledforeground="black", command=root.quit)
        quit_button.grid(row=0, column=4, padx=10, pady=5)

        #   Results frame
        self.results_text = tk.Text(self.results_labelframe)
        self.results_text.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, padx=10, pady=10)

        results_scrollbar = ttk.Scrollbar(
            self.results_labelframe, command=self.results_text.yview)
        results_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.results_text['yscrollcommand'] = results_scrollbar.set

        #   Skipped frame
        self.skipped_text = tk.Text(skipped_labelframe)
        self.skipped_text.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, padx=10, pady=10)

        skipped_scrollbar = ttk.Scrollbar(skipped_labelframe, command=self.skipped_text.yview)
        skipped_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.skipped_text['yscrollcommand'] = skipped_scrollbar.set

        #   History frame
        self.history_text = tk.Text(history_labelframe)
        self.history_text.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, padx=10, pady=10)

        history_scrollbar = ttk.Scrollbar(history_labelframe, command=self.history_text.yview)
        history_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)
        self.history_text['yscrollcommand'] = history_scrollbar.set

    # Function for selecting a file from the system
    def select_file(self):
        selected_file = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select a File",
            filetypes=(("Excel Files", "*.xlsx .xls"), ("all files", "*.* ")))
        if selected_file is None or selected_file == '':
            self.filename.set(self.default_filename)
        else:
            self.filename.set(selected_file)

    # Change the state of the search button, export results button, and stop button
    def flip_buttons(self):
        if str(self.search_button['state']) == str(tk.DISABLED):
            self.search_button['state'] = str(tk.NORMAL)
            self.export_results_button['state'] = str(tk.NORMAL)
            self.stop_button['state'] = str(tk.DISABLED)
            self.stop_variable.set(False)
        else:
            self.search_button['state'] = str(tk.DISABLED)
            self.export_results_button['state'] = str(tk.DISABLED)
            self.stop_button['state'] = str(tk.NORMAL)

    # Toggle state of retry options based on default selected
    def toggle_default_retries(self):
        if self.default_timeout.get() == 0:
            self.option_retry_seconds_entry.config(state=tk.NORMAL)
            self.option_retry_quantity_entry.config(state=tk.NORMAL)
        else:
            self.option_retry_seconds_entry.delete(0, tk.END)
            self.option_retry_seconds_entry.insert(0, "3")
            self.option_retry_seconds_entry.config(state=tk.DISABLED)

            self.option_retry_quantity_entry.delete(0, tk.END)
            self.option_retry_quantity_entry.insert(0, "3")
            self.option_retry_quantity_entry.config(state=tk.DISABLED)

    # Validate all user inputs, returning true/false
    def validate_values(self):
        errors = []
        if not os.path.isfile(self.filename.get()):
            errors.append("- The file '{file}' could not be found.".format(file=self.filename.get()))

        if self.input_variable.get() == "":
            errors.append("- No search arguments entered.")

        if self.force_retry_urls.get() == 1 and len(self.skipped_text.get('1.0', tk.END)) == 0:
            errors.append("- No skipped URLs to search.")

        if not validate_int(self.option_retry_quantity_entry.get()):
            errors.append("- The number of retries option is invalid")

        if not validate_int(self.option_retry_seconds_entry.get()):
            errors.append("- The seconds before timeout option is invalid")

        if len(errors) != 0:
            messagebox.showinfo("Error", '\n'.join(errors))
            return False
        return True

    # function to search a website for
    def search_url(self, url, session, retries, wait_time):
        if url is not None and (url.find("https:") == 0 or url.find("http:") == 0):
            try:
                current_page = return_webpage(session, url, retry_quantity=retries, timeout_limit=wait_time)
                for search_string in self.input_variable.get().split("+"):
                    if self.case_sensitive == 1:
                        find_count = current_page.text.count(search_string.upper())
                    else:
                        find_count = current_page.text.upper().count(search_string.upper())

                    if find_count != 0:
                        found_text = self.found_text_formatter.format(
                            search_string=search_string,
                            url=url,
                            find_count=find_count)
                        self.found_results.append(found_text)
                        self.results_text.insert(tk.END, found_text)
            except requests.exceptions.Timeout:
                self.logger.debug("Url request timeout: {url}".format(url=url))
                self.skipped_text.insert(tk.INSERT, url + "\n")

    # scrape the web based on the user's selection
    def scrape(self):
        self.flip_buttons()
        # Reset variables for the new search
        http = requests.Session()  # Create a session object to use so that it is faster to reach
        self.found_results = []
        percentage_complete = 0
        percent_complete_text = format(percentage_complete, ".0%")
        self.results_text.delete('1.0', tk.END)

        try:
            # only run the skipped urls if selected
            if self.force_retry_urls != 1:
                # get the file that has been selected
                url_file = openpyxl.load_workbook(self.filename.get(), read_only=True)
                worksheet = url_file.active

                for row in worksheet.iter_rows(1, worksheet.max_row):
                    if self.stop_variable.get():
                        self.logger.info("User stopped the webscrapper at " + percent_complete_text)
                        self.completion_text.set("Results: User stopped at " + percent_complete_text)
                        self.results_labelframe.configure(text=self.completion_text.get())
                        break
                    if round(row[0].row / worksheet.max_row, 2) > percentage_complete:
                        percentage_complete = round(row[0].row / worksheet.max_row, 2)
                        percentage_complete_text = format(percentage_complete, ".0%")
                        self.completion_text.set("Results: " + percentage_complete_text)
                        self.results_labelframe.configure(text=self.completion_text.get())
                    url = row[0].value

                    self.search_url(url, http, int(self.option_retry_quantity_entry.get()),
                                    int(self.option_retry_seconds_entry.get()))
                url_file.close()

            if self.force_retry_urls == 1 or self.auto_retry_urls == 1:
                # run the skipped urls if the user chose to do so in any way
                skipped_urls = self.skipped_text.get('1.0', tk.END).split("\n")
                self.skipped_text.delete('1.0', tk.END)

                for index, skipped_url in enumerate(skipped_urls):
                    if self.stop_variable.get():
                        self.completion_text.set("Results: User stopped at " + percent_complete_text)
                        self.results_labelframe.configure(text=self.completion_text.get())
                        break
                    if round(index / len(skipped_urls), 2) > percentage_complete:
                        percentage_complete = round(index / len(skipped_urls), 2)
                        percentage_complete_text = format(percentage_complete, ".0%")
                        self.completion_text.set("Results: " + percentage_complete_text)
                        self.results_labelframe.configure(text=self.completion_text.get())

                    self.search_url(skipped_url, http, int(self.option_retry_quantity_entry.get()),
                                    int(self.option_retry_seconds_entry.get()))
            if len(self.found_results) == 0:
                message = "- The search produced no results (check skipped URLs)."
                self.results_text.delete('1.0', tk.END)
                self.results_text.insert(tk.INSERT, message)
                history_text = self.history_text_formatter.format(
                    searches=",".join(self.input_variable.get().split("+")),
                    results=message)
            else:
                history_text = self.history_text_formatter.format(
                    searches=", ".join(self.input_variable.get().split("+")),
                    results="".join(self.found_results))
            self.history_text.insert('1.0', history_text)

            http.close()
        except Exception as thrownException:
            self.logger.error("Unexpected error when scraping: {error}".format(error=repr(thrownException)))
        finally:
            self.flip_buttons()

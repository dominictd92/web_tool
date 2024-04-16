#
# This maps a website by navigating the website through all
#   links found on each page starting with the home page
#

import re
import requests
import threading

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

from bs4 import BeautifulSoup

from webtool.widget.CollapsibleFrame import CollapsibleFrame
from webtool.widget.ScrollableFrame import ScrollableFrame
from webtool.widget.ScrollableText import ScrollableText
from webtool.constants.constants import *
from webtool.utils.fileutils import export_xlsx
from webtool.utils.loggingutils import get_logger
from webtool.utils.webutils import return_webpage, update_url


# the class for the webmapper with all needed methods within it
class Webmapper(tk.Frame):
    # class variables
    default_ignored_file_ext = ["pdf", "doc", "docx", "xls", "xlsx"]

    subdirectory_url_regex = "(^[/])"
    relative_url_regex = "(^[.])"
    absolute_url_regex = "(^{home})"
    full_url_regex = "{absolute}|{subdirectory}|{relative}"

    notes = (
        " - This webmapper goes through an entire website, following the links on the pages.\n")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.logger = get_logger()

        self.scrollable_frame = ScrollableFrame(self)

        # Variables used throughout the webmapper
        self.urls_searched = []
        self.urls_to_search = []
        self.url_protocol_option = tk.StringVar()
        self.url_protocol_option.set(url_protocol_options[0])
        self.starting_url = tk.StringVar()
        self.file_name = tk.StringVar()
        self.ignore_files = tk.StringVar()
        self.ignore_files.set(",".join(self.default_ignored_file_ext))
        note_text = tk.StringVar()
        note_text.set(self.notes)
        self.stop_variable = tk.BooleanVar()
        self.stop_variable.set(False)

        # Webmapper frames
        #   Note frame
        note_frame = tk.Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=1)
        note_frame.grid(row=0, column=0, sticky=tk.EW)

        #   Input frame
        input_frame = tk.Frame(self.scrollable_frame)
        input_frame.grid(row=1, column=0, sticky=tk.EW)

        #   Button frame
        button_frame = tk.Frame(self.scrollable_frame)
        button_frame.grid(row=2, column=0, sticky=tk.EW)

        #   Results frame
        self.results_label_text = tk.StringVar()
        self.results_label_text.set("Results")
        self.results_labelframe = tk.LabelFrame(
            self.scrollable_frame, text=self.results_label_text.get(), height=200, width=725)
        self.results_labelframe.grid(row=3, column=0, sticky=tk.EW)
        self.results_labelframe.grid_rowconfigure(0, weight=1)
        self.results_labelframe.grid_columnconfigure(0, weight=1)
        self.results_labelframe.grid_propagate(False)

        #   Skipped urls frame
        skipped_labelframe = tk.LabelFrame(
            self.scrollable_frame, text="Skipped URLs", height=200, width=725)
        skipped_labelframe.grid(row=4, column=0, sticky=tk.EW, pady=5)
        skipped_labelframe.grid_rowconfigure(0, weight=1)
        skipped_labelframe.grid_columnconfigure(0, weight=1)
        skipped_labelframe.grid_propagate(False)

        # Widgets within the frames
        #   Note frame
        note_label_label = tk.Label(note_frame, text="", anchor=tk.W, justify=tk.LEFT, cursor='hand2')
        note_label_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        note_collapsible_frame = CollapsibleFrame(note_frame, "Note", note_label_label)
        note_collapsible_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)

        note_label = tk.Label(note_collapsible_frame, textvariable=note_text, wraplength=680, justify=tk.LEFT)
        note_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        #   Input frame
        starting_url_label = tk.Label(input_frame, text="Starting URL: ")
        starting_url_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        starting_url_protocol = tk.OptionMenu(input_frame, self.url_protocol_option, *url_protocol_options)
        starting_url_protocol.grid(row=0, column=1, sticky=tk.E, padx=5, pady=10)

        starting_url_entry = ttk.Entry(input_frame, textvariable=self.starting_url, width=45, justify=tk.LEFT)
        starting_url_entry.grid(row=0, column=2, columnspan=3, sticky=tk.W, padx=10, pady=10)

        ignore_files_label = tk.Label(input_frame, text="Ignore file extensions: ")
        ignore_files_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        ignore_files_entry = ttk.Entry(input_frame, textvariable=self.ignore_files, width=45, justify=tk.LEFT)
        ignore_files_entry.grid(row=1, column=2, columnspan=4, sticky=tk.W, padx=10, pady=10)

        file_name_label = tk.Label(input_frame, text="File Name: ")
        file_name_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

        file_name_entry = ttk.Entry(input_frame, textvariable=self.file_name, width=45, justify=tk.LEFT)
        file_name_entry.grid(row=2, column=2, columnspan=4, sticky=tk.W, padx=10, pady=10)

        #   Button frame
        self.search_button = tk.Button(
            button_frame, text="Search", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: False if not self.validate_values() else threading.Thread(target=self.map).start())
        self.search_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(
            button_frame, text="Stop", state=tk.DISABLED, width=10, fg="black", disabledforeground="black",
            command=lambda: self.stop_variable.set(True))
        self.stop_button.grid(row=0, column=2, padx=10, pady=10)

        export_button = tk.Button(
            button_frame, text="Export", width=10, fg="black", disabledforeground="black",
            command=lambda: export_xlsx(dataset=self.urls_searched, default_filename=mapper_default_filename))
        export_button.grid(row=0, column=4, padx=10, pady=10)

        #   Results frame
        self.results_text = ScrollableText(self.results_labelframe, highlightthickness=0, wrap='none')
        self.results_text.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, pady=(5, 5), padx=(5, 15))

        #   Skipped frame
        self.skipped_text = ScrollableText(skipped_labelframe, highlightthickness=0, wrap='none')
        self.skipped_text.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, pady=(5, 5), padx=(5, 15))

    # Change the state of the search button, export results button, and stop button
    def flip_buttons(self):
        if str(self.search_button['state']) == str(tk.DISABLED):
            self.search_button['state'] = str(tk.NORMAL)
        else:
            self.search_button['state'] = str(tk.DISABLED)

        if str(self.stop_button['state']) == str(tk.DISABLED):
            self.stop_button['state'] = str(tk.NORMAL)
        else:
            self.stop_button['state'] = str(tk.DISABLED)
            self.stop_variable.set(False)

    # Validate all user inputs, returning true/false
    def validate_values(self):
        errors = []
        if self.starting_url.get() == '':
            errors.append("The Starting URL requires a valid URL.")

        if len(errors) != 0:
            messagebox.showinfo("Error", '\n'.join(errors))
            return False

        return True

    # map the website base on the user's selections
    def map(self):
        self.flip_buttons()
        # Reset variables for the new mapping
        current_url = ""
        session = requests.Session()
        self.results_text.delete('1.0', tk.END)

        home_url = update_url(self.url_protocol_option.get() + self.starting_url.get(), add_end_slash=True)
        self.logger.debug("Home url: " + home_url)

        self.urls_to_search.append(home_url)

        self.absolute_url_regex = self.absolute_url_regex.format(home=home_url)
        self.full_url_regex = self.full_url_regex.format(
            absolute=self.absolute_url_regex,
            subdirectory=self.subdirectory_url_regex,
            relative=self.relative_url_regex)

        while len(self.urls_to_search) > 0:
            if self.stop_variable.get():
                self.logger.info("User stopped application.")
                break

            try:
                current_url = self.urls_to_search[0]
                current_page = return_webpage(session, current_url, retry_quantity=3, timeout_limit=3)
                # At times, the URL that is in the href attribute comes back as a different one than expected
                #   and is not what is normally seen, even though it is

                soup = BeautifulSoup(current_page.text, features='html.parser')

                page_links = soup.find_all('a')

                for a in filter(lambda link: link.attrs is not None and 'href' in link.attrs, page_links):
                    current_link = a['href']

                    self.logger.debug("Webmapper reviewing {link} on {page}".format(
                        link=current_link,
                        page=current_page.url
                    ))

                    if (re.search(self.full_url_regex, current_link) and
                        re.search(ignored_files_regex.format(ext='|'.join(self.ignore_files.get().split(','))),
                                  current_link)):

                        self.logger.debug("Webmapper validated {link} on {page}".format(
                            link=current_link, page=current_page.url))

                        # format the url to a standardized version
                        current_link = update_url(url=current_link, base_url=home_url, add_end_slash=True)

                        self.logger.info("{link} in lists {first} on {second}".format(
                            link=current_link,
                            first=str(current_link not in self.urls_searched),
                            second=str(current_link not in self.urls_to_search)))

                        if current_link not in self.urls_searched and current_link not in self.urls_to_search:
                            self.urls_to_search.append(current_link)
                            self.results_label_text.set(
                                "Links to review: {num}".format(num=str(len(self.urls_to_search))))
                            self.results_labelframe.configure(text=self.results_label_text.get())
                            self.logger.info("Added {link}".format(link=current_link))

                self.urls_to_search.remove(current_url)

                self.urls_searched.append(current_url)
                self.results_text.insert(tk.END, "\n - " + current_url)
            except requests.exceptions.Timeout:
                # Add this url to a list of URLs that timed out to retry later
                self.logger.debug("Url request timeout: {url}".format(url=current_url))
                self.skipped_text.insert(tk.INSERT, current_url + "\n")
                self.urls_to_search.remove(current_url)

            except Exception as thrownException:
                self.logger.error(
                    "Url {url} unexpected error: {error}".format(url=current_url, error=repr(thrownException)))
                self.urls_to_search.remove(current_url)

        self.flip_buttons()

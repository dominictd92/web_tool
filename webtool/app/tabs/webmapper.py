#
# This maps a website by navigating the website through all
#   links found on each page starting with the home page
#

import re
import requests
import threading

from tkinter import (W, E, EW, NSEW, LEFT, END, INSERT, NORMAL, DISABLED, BooleanVar, StringVar, Button, OptionMenu,
                     Entry, Label, LabelFrame, Frame)
from tkinter.messagebox import showinfo

from bs4 import BeautifulSoup

from webtool.constants.constants import ignored_files_regex, mapper_default_filename, url_protocol_options
from webtool.widget.CollapsibleFrame import CollapsibleFrame
from webtool.widget.ScrollableFrame import ScrollableFrame
from webtool.widget.ScrollableText import ScrollableText
from webtool.utils.fileutils import export_xlsx
from webtool.utils.loggingutils import get_logger
from webtool.utils.webutils import return_webpage, update_url


# the class for the webmapper with all needed methods within it
class Webmapper(Frame):
    # class variables
    default_ignored_file_ext = ["pdf", "doc", "docx", "xls", "xlsx"]

    subdirectory_url_regex = "(^[/])"
    relative_url_regex = "(^[.])"
    absolute_url_regex = "(^{home})"
    full_url_regex = "{absolute}|{subdirectory}|{relative}"

    notes = (
        " - This webmapper goes through an entire website, following the links on the pages.\n"
        " - Ensure that you add to the ignored extensions to make it go as fast as it can.\n")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.logger = get_logger()

        self.scrollable_frame = ScrollableFrame(self)

        # Variables used throughout the webmapper
        self.urls_searched = []
        self.urls_to_search = []
        self.url_protocol_option = StringVar()
        self.url_protocol_option.set(url_protocol_options[0])
        self.starting_url = StringVar()
        self.file_name = StringVar()
        self.ignore_files = StringVar()
        self.ignore_files.set(",".join(self.default_ignored_file_ext))
        note_text = StringVar()
        note_text.set(self.notes)
        self.stop_variable = BooleanVar()
        self.stop_variable.set(False)

        # Webmapper frames
        #   Note frame
        note_frame = Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=1)
        note_frame.grid(row=0, column=0, sticky=EW)

        #   Input frame
        input_frame = Frame(self.scrollable_frame)
        input_frame.grid(row=1, column=0, sticky=EW)

        #   Button frame
        button_frame = Frame(self.scrollable_frame)
        button_frame.grid(row=2, column=0, sticky=EW)

        #   Results frame
        self.results_label_text = StringVar()
        self.results_label_text.set("Results")
        self.results_labelframe = LabelFrame(
            self.scrollable_frame, text=self.results_label_text.get(), height=200, width=725)
        self.results_labelframe.grid(row=3, column=0, sticky=EW)
        self.results_labelframe.grid_rowconfigure(0, weight=1)
        self.results_labelframe.grid_columnconfigure(0, weight=1)
        self.results_labelframe.grid_propagate(False)

        #   Skipped urls frame
        skipped_labelframe = LabelFrame(
            self.scrollable_frame, text="Skipped URLs", height=200, width=725)
        skipped_labelframe.grid(row=4, column=0, sticky=EW, pady=5)
        skipped_labelframe.grid_rowconfigure(0, weight=1)
        skipped_labelframe.grid_columnconfigure(0, weight=1)
        skipped_labelframe.grid_propagate(False)

        # Widgets within the frames
        #   Note frame
        note_label_label = Label(note_frame, text="", anchor=W, justify=LEFT, cursor='hand2')
        note_label_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        note_collapsible_frame = CollapsibleFrame(note_frame, "Note", note_label_label)
        note_collapsible_frame.grid(row=1, column=0, padx=5, pady=5, sticky=EW)

        note_label = Label(note_collapsible_frame, textvariable=note_text, wraplength=680, justify=LEFT)
        note_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        #   Input frame
        starting_url_label = Label(input_frame, text="Starting URL: ")
        starting_url_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        starting_url_protocol = OptionMenu(input_frame, self.url_protocol_option, *url_protocol_options)
        starting_url_protocol.grid(row=0, column=1, sticky=E, padx=5, pady=10)

        starting_url_entry = Entry(input_frame, textvariable=self.starting_url, width=45, justify=LEFT)
        starting_url_entry.grid(row=0, column=2, columnspan=3, sticky=W, padx=10, pady=10)

        ignore_files_label = Label(input_frame, text="Ignore file extensions: ")
        ignore_files_label.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        ignore_files_entry = Entry(input_frame, textvariable=self.ignore_files, width=45, justify=LEFT)
        ignore_files_entry.grid(row=1, column=2, columnspan=4, sticky=W, padx=10, pady=10)

        file_name_label = Label(input_frame, text="File Name: ")
        file_name_label.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        file_name_entry = Entry(input_frame, textvariable=self.file_name, width=45, justify=LEFT)
        file_name_entry.grid(row=2, column=2, columnspan=4, sticky=W, padx=10, pady=10)

        #   Button frame
        self.search_button = Button(
            button_frame, text="Search", state=NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: False if not self.validate_values() else threading.Thread(target=self.map).start())
        self.search_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = Button(
            button_frame, text="Stop", state=DISABLED, width=10, fg="black", disabledforeground="black",
            command=lambda: self.stop_variable.set(True))
        self.stop_button.grid(row=0, column=2, padx=10, pady=10)

        export_button = Button(
            button_frame, text="Export", width=10, fg="black", disabledforeground="black",
            command=lambda: export_xlsx(dataset=self.urls_searched, default_filename=mapper_default_filename))
        export_button.grid(row=0, column=4, padx=10, pady=10)

        trace_button = Button(
            button_frame, text="Trace", state=NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: False if not self.validate_values() else False)
        trace_button.grid(row=0, column=0, padx=10, pady=10)

        #   Results frame
        self.results_text = ScrollableText(self.results_labelframe, highlightthickness=0, wrap='none')
        self.results_text.grid(row=0, column=0, columnspan=4, sticky=NSEW, pady=(5, 5), padx=(5, 15))

        #   Skipped frame
        self.skipped_text = ScrollableText(skipped_labelframe, highlightthickness=0, wrap='none')
        self.skipped_text.grid(row=0, column=0, columnspan=4, sticky=NSEW, pady=(5, 5), padx=(5, 15))

        note_collapsible_frame.activate()

    # Change the state of the search button, export results button, and stop button
    def flip_buttons(self):
        if str(self.search_button['state']) == str(DISABLED):
            self.search_button['state'] = str(NORMAL)
        else:
            self.search_button['state'] = str(DISABLED)

        if str(self.stop_button['state']) == str(DISABLED):
            self.stop_button['state'] = str(NORMAL)
        else:
            self.stop_button['state'] = str(DISABLED)
            self.stop_variable.set(False)

    # Validate all user inputs, returning true/false
    def validate_values(self):
        errors = []
        if self.starting_url.get() == '':
            errors.append("The Starting URL requires a valid URL.")

        if len(errors) != 0:
            showinfo("Error", '\n'.join(errors))
            return False

        return True

    # map the website base on the user's selections
    def map(self):
        self.flip_buttons()
        # Reset variables for the new mapping
        current_url = ""
        session = requests.Session()
        self.results_text.delete('1.0', END)

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

                    self.logger.debug(f"Webmapper reviewing {current_link} on {current_page.url}")

                    if (re.search(self.full_url_regex, current_link) and
                        re.search(ignored_files_regex.format(ext='|'.join(self.ignore_files.get().split(','))),
                                  current_link)):

                        self.logger.debug(f"Webmapper reviewing {current_link} on {current_page.url}")

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
                self.results_text.insert(END, "\n - " + current_url)
            except requests.exceptions.Timeout:
                # Add this url to a list of URLs that timed out to retry later
                self.logger.debug(f"Url request timeout: {current_url}")
                self.skipped_text.insert(INSERT, current_url + "\n")
                self.urls_to_search.remove(current_url)

            except Exception as thrownException:
                self.logger.error(f"Url {current_url} unexpected error: {repr(thrownException)}")
                self.urls_to_search.remove(current_url)

        self.flip_buttons()

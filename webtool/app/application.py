#
# This is the main tk application that is called from the main
#   class to build and display the UI for the application
#

import tkinter as tk
from tkinter import ttk

import webtool.app.tabs.webscrapper as webscrapper
import webtool.app.tabs.webmapper as webmapper
import webtool.app.tabs.admin as admin
from webtool.utils.loggingutils import get_logger


# this class combines the tabs for all tools
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = get_logger()

        self.title("Web Tool")
        self.wm_title("Web Tool")
        self.geometry("800x850")

        # create the tabs
        tab_controller = ttk.Notebook(self)
        webscrapper_tab = webscrapper.Webscrapper(tab_controller)
        webmapper_tab = webmapper.Webmapper(tab_controller)
        admin_tab = admin.Admin(tab_controller)

        # a list of tabs alongside their sizes and names to auto resize the window
        #   tab: tkinter frame, name: displayed name of the tab, size: 'width x height' of the window
        self.tabs_list = [
            {'tab': webscrapper_tab, 'name': "Webscrapper", 'size': "800x850"},
            {'tab': webmapper_tab, 'name': "Webmapper", 'size': "800x700"},
            {'tab': admin_tab, 'name': "Admin", 'size': "800x350"}
        ]

        # add the tabs to the window
        for tab in self.tabs_list:
            tab_controller.add(tab['tab'], text=tab['name'])
            self.logger.debug("Added tab {tab} to the application".format(tab=tab['name']))
        tab_controller.pack(expand=1, fill=tk.BOTH)

        # update the size of the tkinter window based on the notebook
        tab_controller.bind('<<NotebookTabChanged>>',
                            lambda e: self.update_window_size(tab_controller.index(tab_controller.select())))

    def update_window_size(self, index):
        self.geometry(self.tabs_list[index]['size'])

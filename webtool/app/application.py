#
# This is the main tk application that is called from the main
#   class to build and display the UI for the application
#

from tkinter import BOTH, Tk
from tkinter.ttk import Notebook

from webtool.app.tabs.webscrapper import Webscrapper
from webtool.app.tabs.webmapper import Webmapper
from webtool.app.tabs.admin import Admin
from webtool.utils.loggingutils import get_logger


# this class combines the tabs for all tools
class Application(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().title("Web Tool")
        super().wm_title("Web Tool")
        super().geometry("800x850")

        self.logger = get_logger()

        # create the tabs
        tab_controller = Notebook(self)
        webscrapper_tab = Webscrapper(tab_controller)
        webmapper_tab = Webmapper(tab_controller)
        admin_tab = Admin(tab_controller)

        # a list of tabs alongside their sizes and names to auto resize the window
        #   tab: tkinter frame, name: displayed name of the tab, size: 'width x height' of the window
        self.tabs_list = [
            {'tab': webscrapper_tab, 'name': "Webscrapper", 'size': "800x850"},
            {'tab': webmapper_tab, 'name': "Webmapper", 'size': "800x700"},
            {'tab': admin_tab, 'name': "Admin", 'size': "800x200"}
        ]

        # add the tabs to the window
        for tab in self.tabs_list:
            tab_controller.add(tab['tab'], text=tab['name'])
            self.logger.debug("Added tab {tab} to the application".format(tab=tab['name']))
        tab_controller.pack(expand=1, fill=BOTH)

        # update the size of the tkinter window based on the notebook
        tab_controller.bind('<<NotebookTabChanged>>',
                            lambda e: self.update_window_size(tab_controller.index(tab_controller.select())))

    def update_window_size(self, index):
        self.geometry(self.tabs_list[index]['size'])

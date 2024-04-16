#
# This is the admin tab that would only be useful for testing or configurations
#

import tkinter as tk

import webtool.utils.loggingutils as logging_utils

from webtool.widget.ScrollableFrame import ScrollableFrame
from webtool.utils.loggingutils import get_logger


# the class for the admin tab for verifying information
class Admin(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.logger = get_logger()

        self.scrollable_frame = ScrollableFrame(self)

        # variables
        logging_location = tk.StringVar()
        logging_location.set(logging_utils.get_logging_location())

        # Admin frames
        #   Log frame
        log_frame = tk.Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=2)
        log_frame.grid(row=0, column=0, sticky=tk.EW)

        # Widgets within the frames
        #   Log frame
        logging_location_label = tk.Label(log_frame, text="Log Location", anchor=tk.W, justify=tk.LEFT)
        logging_location_label.grid(row=0, column=0, padx=5, pady=10, sticky=tk.EW)

        logging_location_text = tk.Label(log_frame, textvariable=logging_location, anchor=tk.W, justify=tk.LEFT)
        logging_location_text.grid(row=0, column=1, columnspan=4, padx=5, pady=10, sticky=tk.EW)

        refresh_log_button = tk.Button(
            log_frame, text="Refresh Location", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: logging_location.set(logging_utils.get_logging_location()))
        refresh_log_button.grid(row=1, column=0, padx=10, pady=10)

        open_log_button = tk.Button(
            log_frame, text="Open Location", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: logging_utils.open_log_folder())
        open_log_button.grid(row=1, column=1, padx=10, pady=10)

        clear_log_button = tk.Button(
            log_frame, text="Clear Log", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: logging_utils.clear_log())
        clear_log_button.grid(row=1, column=2, padx=10, pady=10)

        delete_log_button = tk.Button(
            log_frame, text="Delete Log", state=tk.NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: logging_utils.delete_log())
        delete_log_button.grid(row=1, column=3, padx=10, pady=10)

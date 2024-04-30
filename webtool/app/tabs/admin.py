#
# This is the admin tab that would only be useful for testing or configurations
#

from tkinter import EW, W, LEFT, NORMAL, StringVar, Label, Button, Frame

from webtool.utils.loggingutils import clear_log, delete_log, get_logging_location, open_log_folder
from webtool.widget.ScrollableFrame import ScrollableFrame
from webtool.utils.loggingutils import get_logger


# the class for the admin tab for verifying information
class Admin(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.logger = get_logger()

        self.scrollable_frame = ScrollableFrame(self)

        # variables
        logging_location = StringVar()
        logging_location.set(get_logging_location())

        # Admin frames
        #   Log frame
        log_frame = Frame(self.scrollable_frame, highlightbackground='white', highlightthickness=2)
        log_frame.grid(row=0, column=0, sticky=EW)

        # Widgets within the frames
        #   Log frame
        logging_location_label = Label(log_frame, text="Log Location", anchor=W, justify=LEFT)
        logging_location_label.grid(row=0, column=0, padx=5, pady=10, sticky=EW)

        logging_location_text = Label(log_frame, textvariable=logging_location, anchor=W, justify=LEFT)
        logging_location_text.grid(row=0, column=1, columnspan=4, padx=5, pady=10, sticky=EW)

        open_log_button = Button(
            log_frame, text="Open Location", state=NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: open_log_folder())
        open_log_button.grid(row=1, column=0, padx=10, pady=10)

        clear_log_button = Button(
            log_frame, text="Clear Log", state=NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: clear_log())
        clear_log_button.grid(row=1, column=1, padx=10, pady=10)

        delete_log_button = Button(
            log_frame, text="Delete Log", state=NORMAL, width=10, fg="black", disabledforeground="black",
            command=lambda: delete_log())
        delete_log_button.grid(row=1, column=2, padx=10, pady=10)

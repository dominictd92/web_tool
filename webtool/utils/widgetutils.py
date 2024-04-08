#
# Utilities for the tkinter widgets. There are some functions which are useful
#   for a number of my app within this project so this is strictly for those
#

from ..constants.constants import *


# Switch the state of the collapsible frame
def activate(collapsible_frame, widget, widget_text):
    if widget.get() == collapsible_texts[0].format(object=widget_text):
        collapsible_frame.grid_forget()
        widget.set(collapsible_texts[1].format(object=widget_text))

    elif widget.get() == collapsible_texts[1].format(object=widget_text):
        collapsible_frame.grid(row=1, column=0, columnspan=2)
        widget.set(collapsible_texts[0].format(object=widget_text))

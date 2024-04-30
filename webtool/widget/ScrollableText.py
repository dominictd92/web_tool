#
# This is creating a tk.Text that is scrollable horizontal and vertical. Quick view of
#   tk.scrolledText.ScrolledText didn't present a horizontal scroll as well, so I made this
# Note: Have to change to be a frame so the grid for the scrollbars work properly
#

from tkinter import VERTICAL, HORIZONTAL, NSEW, Text
from tkinter.ttk import Scrollbar


class ScrollableText(Text):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        results_y_scrollbar = Scrollbar(parent, command=self.yview, orient=VERTICAL)
        results_y_scrollbar.grid(row=0, column=1, sticky=NSEW)

        results_x_scrollbar = Scrollbar(parent, command=self.xview, orient=HORIZONTAL)
        results_x_scrollbar.grid(row=1, column=0, sticky=NSEW)

        self['yscrollcommand'] = results_y_scrollbar.set
        self['xscrollcommand'] = results_x_scrollbar.set

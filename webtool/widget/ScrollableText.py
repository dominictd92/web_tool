#
# This is creating a tk.Text that is scrollable horizontal and vertical. Quick view of
#   tk.scrolledText.ScrolledText didn't present a horizontal scroll as well, so I made this
# Note: Have to change to be a frame so the grid for the scrollbars work properly
#

import tkinter as tk
from tkinter import ttk


class ScrollableText(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        results_y_scrollbar = ttk.Scrollbar(parent, command=self.yview, orient=tk.VERTICAL)
        results_y_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        results_x_scrollbar = ttk.Scrollbar(parent, command=self.xview, orient=tk.HORIZONTAL)
        results_x_scrollbar.grid(row=1, column=0, sticky=tk.NSEW)

        self['yscrollcommand'] = results_y_scrollbar.set
        self['xscrollcommand'] = results_x_scrollbar.set

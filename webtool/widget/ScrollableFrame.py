#
# This is creating a tk.Frame that is scrollable, applying the canvas to it
#   to enable this functionality.
# Similar functionality and foundation of this logic can be found here:
#   https://blog.teclado.com/tkinter-scrollable-frames/
#

import tkinter as tk
from tkinter import ttk

from webtool.utils.systemsutil import get_os

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # create a canvas to allow the application to be scrollable if resized
        self.canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar_vertical = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar_horizontal = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.canvas.xview)

        super().__init__(self.canvas, *args, **kwargs)

        self.canvas.create_window((0, 0), window=self, anchor=tk.NW)

        self.canvas.configure(yscrollcommand=scrollbar_vertical.set)
        self.canvas.configure(xscrollcommand=scrollbar_horizontal.set)

        scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.columnconfigure((0, 1), weight=1)
        self.canvas.rowconfigure((0, 1), weight=1)

        self.bind(
            '<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
        )
        self.canvas.bind_all("<MouseWheel>", lambda e: self.scroll_on_mousewheel(e), add="+")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(True)

    # allow scrolling on the notebook screens
    def scroll_on_mousewheel(self, event):
        current_platform = get_os()

        match current_platform:
            case "macOS":
                self.canvas.yview_scroll(int(-1 * event.delta), "units")
            case "Windows":
                self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")

#
# This is creating a tk.Frame that is scrollable, applying the canvas to it
#   to enable this functionality.
# Similar functionality can be found here: https://blog.teclado.com/tkinter-scrollable-frames/
#

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        # create a canvas to allow the application to be scrollable if resized
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar_vertical = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_horizontal = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=canvas.xview)

        super().__init__(canvas)

        self.bind(
            '<Configure>',
            lambda e: canvas.configure(
                scrollregion=canvas.bbox(tk.ALL)
            )
        )

        canvas.create_window((0, 0), window=self, anchor=tk.NW)

        canvas.configure(yscrollcommand=scrollbar_vertical.set)
        canvas.configure(xscrollcommand=scrollbar_horizontal.set)

        scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

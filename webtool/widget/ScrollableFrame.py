#
# This is creating a tk.Frame that is scrollable, applying the canvas to it
#   to enable this functionality.
# Similar functionality and foundation of this logic can be found here:
#   https://blog.teclado.com/tkinter-scrollable-frames/
#

from tkinter import X, Y, RIGHT, LEFT, BOTH, BOTTOM, VERTICAL, HORIZONTAL, ALL, NW, Frame, Canvas
from tkinter.ttk import Scrollbar

from webtool.utils.systemsutil import get_os


class ScrollableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        # create a canvas to allow the application to be scrollable if resized
        self.canvas = Canvas(parent, highlightthickness=0)
        scrollbar_vertical = Scrollbar(parent, orient=VERTICAL, command=self.canvas.yview)
        scrollbar_horizontal = Scrollbar(parent, orient=HORIZONTAL, command=self.canvas.xview)

        super().__init__(self.canvas, *args, **kwargs)

        self.canvas.create_window((0, 0), window=self, anchor=NW)

        self.canvas.configure(yscrollcommand=scrollbar_vertical.set)
        self.canvas.configure(xscrollcommand=scrollbar_horizontal.set)

        scrollbar_horizontal.pack(side=BOTTOM, fill=X)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas.columnconfigure((0, 1), weight=1)
        self.canvas.rowconfigure((0, 1), weight=1)

        self.bind(
            '<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        )
        self.canvas.bind_all("<MouseWheel>", lambda e: self.__scroll_on_mousewheel(e), add="+")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_propagate(True)

    # allow scrolling on the notebook screens
    def __scroll_on_mousewheel(self, event):
        current_platform = get_os()

        match current_platform:
            case "macOS":
                self.canvas.yview_scroll(int(-1 * event.delta), "units")
            case "Windows":
                self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")

#
# This class is to create a hide-able hint similar to tkinter.tix.Balloon, which is deprecated. When there
#   is an alternative, this can be deleted and replaced. Framing of it came from below:
# https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
#

import tkinter as tk


# use with no need to declare/instantiate an object for it:
#   Hint(Frame/Widget associated, "Text to be displayed")
class Hint(tk.Frame):
    id = None
    message = ""
    parent = None
    hint_window = None

    def __init__(self, parent, message):
        super().__init__(parent)

        self.message = message
        self.parent = parent

        parent.bind('<Enter>', lambda e: self.show_hint(e))
        parent.bind('<Leave>', lambda e: self.hidetip())

    def show_hint(self, event):
        x, y, cx, cy = self.parent.bbox(tk.INSERT)
        x = x + self.parent.winfo_pointerx()
        y = y + self.parent.winfo_pointery()
        self.hint_window = tk.Toplevel()
        self.hint_window.wm_overrideredirect(True)
        self.hint_window.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.hint_window, text=self.message, justify=tk.LEFT, foreground="black",
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "12", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        self.hint_window.destroy()

#
# This creates a collapsible frame, with a button/link to show/hide an associated frame
#

from tkinter import Frame

from webtool.constants.constants import collapsible_texts


class CollapsibleFrame(Frame):
    def __init__(self, parent, label_name, activator, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label_name = label_name
        self.activator_widget = activator

        # initially activate the label
        self.activator_widget.config(text=collapsible_texts[0].format(object=self.label_name))

        self.activator_widget.bind("<Button-1>", lambda e: self.activate())

    # Show/Hide the frame
    def activate(self):
        if self.activator_widget.cget(key="text") == collapsible_texts[0].format(object=self.label_name):
            self.grid_forget()
            self.activator_widget.config(text=collapsible_texts[1].format(object=self.label_name))
        elif self.activator_widget.cget(key="text") == collapsible_texts[1].format(object=self.label_name):
            self.grid(row=1, column=0, columnspan=2)
            self.activator_widget.config(text=collapsible_texts[0].format(object=self.label_name))

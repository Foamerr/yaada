import tkinter as tk
from collections import OrderedDict
from tkinter import messagebox
from tkinter import ttk
from frames.arp_poisoning_frame import ArpFrame
from frames.initial_frame import InitialFrame


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        """
        Initialises the graphical user interface (GUI) of the application
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.winfo_toplevel().title("hackerman")

        # Setting the dimensions of the application window
        width = int(self.winfo_screenwidth() * 0.4)
        height = int(self.winfo_screenheight() * 0.4)
        x_start = int(self.winfo_screenwidth() * 0.2)
        y_start = int(self.winfo_screenheight() * 0.2)

        parent.geometry('%dx%d+%d+%d' % (width, height, x_start, y_start))
        parent.resizable(0, 0)

        # Adding the menubar
        self.create_menubar(parent)

        # Divide the application into rows and columns
        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

        self.tabs = {}
        self.tab_mapping = OrderedDict([
            (InitialFrame, 'Initial'),
            (ArpFrame, 'ARP Spoofing')
        ])

        # Add the frames to the application
        for tab in self.tab_mapping.keys():
            frame_name = self.tab_mapping[tab]
            frame = tab(parent=self.notebook, controller=self)
            self.notebook.add(frame, text=frame_name)
        self.tabs[tab.__name__] = frame

    def create_menubar(self, parent):
        """
        Creates a menu bar with respect to @parent
        """
        menubar = tk.Menu(self)
        helpmenu = tk.Menu(menubar, tearoff=0)

        helpmenu.add_command(label="About", command=self.dis_about)
        helpmenu.add_command(label="Documentation", command=self.dis_doc)
        # helpmenu.add_separator()

        menubar.add_cascade(label="Help", menu=helpmenu)
        menubar.add_command(label="Exit", command=root.quit)

        parent.config(menu=menubar)

    @staticmethod
    def dis_about():
        """
        Displays a message box containing the `about' section information
        """
        messagebox.showinfo("About", "Created by Stijn Derks and Nick van de Waterlaat")

    @staticmethod
    def dis_doc():
        """
        Displays a message box containing the `Documentation' section information
        """
        messagebox.showinfo("Documentation", "Lorem ipsum...")


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

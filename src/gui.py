import tkinter as tk
from collections import OrderedDict
from tkinter import ttk
from frames.attack_arp_frame import AttackARPFrame
from frames.initial_frame import InitialFrame
from frames.attack_dns_frame import AttackDNSFrame
from frames.logging_frame import LoggingFrame
from frames.help_frame import HelpFrame


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        """
        Initialises the graphical user interface (GUI) of the application
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.winfo_toplevel().title("hackerman")
        self.configure(bg='black')

        self.font = "Times New Roman"
        self.font_size = 11
        self.notebook = None
        self.tabs = None
        self.tab_map = None
        self.log = None

        self.set_style()
        self.set_size(parent)
        # self.create_menu_bar(parent)
        self.create_tabs()

    def set_style(self):
        style = ttk.Style()
        style.element_create('Plain.Notebook.tab', 'from', 'default')

        # TODO: Make lines below work
        style.configure("color.TButton", bg='#DADADA', fg='black')
        style.configure("color.TLabel", bg='#DADADA', fg='black')

        style.theme_use('classic')

        customed_style = ttk.Style()
        customed_style.configure('Custom.TNotebook.Tab', padding=[10, 8], font=(self.font, self.font_size))

        #

        # style.layout("TNotebook.Tab",
        #              [('Plain.Notebook.tab', {'children':
        #               [('Notebook.padding', {'side': 'top', 'children':
        #                 [('Notebook.focus', {'side': 'top', 'children':
        #                   [('Notebook.label', {'side': 'top', 'sticky': ''})], 'sticky': 'NSWE'})], 'sticky': 'NSWE'})],
        #                     'sticky': 'NSWE'})])
        # style.configure("TNotebook", background='black', borderwidth=0)
        # style.configure("TNotebook.Tab", background='black', foreground='white', lightcolor='gray', borderwidth=2)
        # style.configure("TFrame", background='black', foreground='white', borderwidth=0)

    def set_size(self, parent):
        """
        Sets the width, height, and start positions of the applications
        """
        x_start = int(self.winfo_screenwidth() * 0.2)
        y_start = int(self.winfo_screenheight() * 0.2)
        width = int(self.winfo_screenwidth() * 0.25)
        height = int(self.winfo_screenheight() * 0.6)

        parent.geometry('%dx%d+%d+%d' % (width, height, x_start, y_start))
        parent.resizable(0, 0)

    def create_tabs(self):
        """
        Creates tabs from frames and names provided in @tab_map
        """
        row = 0
        while row < 100:
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            row += 1

        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.log = LoggingFrame(parent=self, controller=self)

        self.notebook.grid(row=0, column=0, columnspan=100, rowspan=31, sticky='NSWE')
        self.log.grid(row=31, column=0, columnspan=100, rowspan=100, sticky='NSWE')

        self.tabs = {}
        self.tab_map = OrderedDict([
            (InitialFrame, 'Home'),
            (AttackARPFrame, 'ARP Poisoning'),
            (AttackDNSFrame, 'DNS Spoofing'),
            (HelpFrame, 'Help')
        ])

        # Add the frames to the application
        for tab in self.tab_map.keys():
            frame_name = self.tab_map[tab]
            frame = tab(parent=self.notebook, controller=self)
            self.notebook.add(frame, text=frame_name)
        self.tabs[tab.__name__] = frame

    # def create_menu_bar(self, parent):
    #     """
    #     Creates a menu bar with respect to @parent
    #     """
    #     menu_bar = tk.Menu(self)
    #     help_menu = tk.Menu(menu_bar, tearoff=0)
    #
    #     help_menu.add_command(label="About", command=self.dis_about)
    #     help_menu.add_command(label="Documentation", command=self.dis_doc)
    #     # help_menu.add_separator()
    #
    #     menu_bar.add_cascade(label="Help", menu=help_menu)
    #     menu_bar.add_command(label="Exit", command=root.quit)
    #
    #     parent.config(menu=menu_bar)

    # @staticmethod
    # def dis_about():
    #     """
    #     Displays a message box containing the `about' section information
    #     """
    #     messagebox.showinfo("About", "Hackerman is a tool for ARP and DNS spoofing \n"
    #                                  "with different modalities that automatically \n"
    #                                  "poisons ARP caches and uses DNS queries to \n"
    #                                  "poison recursive DNS cache. \n"
    #                                  "Created by Stijn Derks and Nick van de Waterlaat")
    #
    # @staticmethod
    # def dis_doc():
    #     """
    #     Displays a message box containing the `Documentation' section information
    #     """
    #     messagebox.showinfo("Documentation", "Lorem ipsum...")


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

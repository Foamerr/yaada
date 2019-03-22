import tkinter as tk
import webbrowser
from tkinter import messagebox


class HelpFrame(tk.Frame):

    def __init__(self, parent, controller):
        """ Initialises GUI of the frame used for the help tab """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')
        self.font = "Georgia"
        self.font_size = 11
        self.stop_thread = None

        self.label_welcome = tk.Label(self,
                                      text='One can get basic information about the application here.'
                                           ' Furthermore, one can find the report with the documentation regarding the'
                                           "application in here when clicking the `Documentation' button.",
                                      font=(self.controller.font, self.controller.font_size),
                                      justify=tk.LEFT,
                                      wraplength=450)
        self.label_welcome.config(bg='#DADADA', fg='black'), self.label_welcome.pack(side='top', pady=10)

        self.button_about = tk.Button(self,
                                      text='About',
                                      command=self.dis_about,
                                      width=35,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_about.config(bg='#DADADA', fg='black'), self.button_about.pack(side='top', pady=10)

        self.button_doc = tk.Button(self,
                                    text='Documentation',
                                    command=self.dis_doc,
                                    width=35,
                                    font=(self.controller.font, self.controller.font_size))
        self.button_doc.config(bg='#DADADA', fg='black'), self.button_doc.pack(side='top', pady=5)

    @staticmethod
    def dis_about():
        """ Displays a message box containing the `about' section information """
        messagebox.showinfo("About", "YAADA is a tool for ARP and DNS cache poisoning "
                                     "with different modalities that automatically "
                                     "poisons ARP caches and uses DNS queries to "
                                     "poison recursive DNS cache. \n"
                                     "Created by Stijn Derks and Nick van de Waterlaat")

    @staticmethod
    def dis_doc():
        """ Opens documentation PDF file in default browser """
        file = r'..\resources\documentation.pdf'
        webbrowser.open_new(file)

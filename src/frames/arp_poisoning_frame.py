import tkinter as tk
import discovery as dis


class ArpFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for ARP spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.label_welcome = tk.Label(self, text='Welcome to tab used for ARP poisoning.')
        self.label_welcome.config(bg='#DADADA', fg='black')
        self.label_welcome.pack(side='top', pady=20)

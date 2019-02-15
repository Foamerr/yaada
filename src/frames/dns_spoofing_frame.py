import tkinter as tk


class InitialFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # welcome text start page
        label_welcome = tk.Label(self, text='Welcome to tab used for DNS spoofing.')
        label_welcome.pack(side='top', pady=20)

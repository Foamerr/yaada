import tkinter as tk


class DnsSpoofingFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        # welcome text start page
        self.label_welcome = tk.Label(self, text='Welcome to tab used for DNS spoofing.')
        self.label_welcome.config(bg='black', foreground='white')
        self.label_welcome.pack(side='top', pady=20)

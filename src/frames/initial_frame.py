import tkinter as tk


class InitialFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the initially showed tab
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        self.label_welcome = tk.Label(self, text='Welcome to H4CK3RM4N')
        self.label_welcome.config(bg='black', foreground='white')
        self.label_welcome.pack(side='top', pady=20)

import tkinter as tk


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.label_welcome = tk.Label(self, text='Welcome to tab used for DNS spoofing.', font=(self.controller.font,
                                                                                                self.controller.font_size))
        self.label_welcome.config(bg='#DADADA', fg='black')
        self.label_welcome.pack(side='top', pady=20)

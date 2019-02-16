import tkinter as tk
import discovery as dis


class TargetFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for selecting the target
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.label_welcome = tk.Label(self, text='The target has to be selected here.')
        self.label_welcome.config(bg='#DADADA', fg='black')
        self.label_welcome.pack(side='top', pady=20)

        options = dis.arp_ping(netmask="192.168.2.0/24")
        tkvar = tk.StringVar(self)
        tkvar.set('Select your target here')
        self.option_menu = tk.OptionMenu(self, tkvar, *options)
        self.option_menu.config(bg='#DADADA', fg='black', borderwidth=1)
        self.option_menu.pack(side='top', pady=5)

        # TODO: replace command and actually set global target
        self.button_doc = tk.Button(self, text='Set target', command=self.quit)
        self.button_doc.config(bg='#DADADA', fg='black')
        self.button_doc.pack(side='top', pady=10)

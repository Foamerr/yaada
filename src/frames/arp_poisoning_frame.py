import tkinter as tk
import discovery as dis


class ArpFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for ARP spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # welcome text start page
        label_welcome = tk.Label(self, text='Welcome to tab used for ARP poisoning.')
        label_welcome.pack(side='top', pady=20)

        options = dis.arp_ping(netmask="192.168.2.0/24")
        tkvar = tk.StringVar(self)
        tkvar.set(options[0])
        option_menu = tk.OptionMenu(self, tkvar, *options)
        option_menu.pack()

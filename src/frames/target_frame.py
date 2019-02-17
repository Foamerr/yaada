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

        self.button_scan = tk.Button(self, text="Scan local network", command=self.update_local)
        self.button_scan.config(bg='#DADADA', fg='black')
        self.button_scan.pack(side='top', pady=15)

        self.ip_box = tk.Listbox(self, width=50, selectmode=tk.MULTIPLE)
        self.ip_box.pack(side='top', pady=5)

        # TODO: add command for setting global victim(s)
        self.button_victim = tk.Button(self, text="Set victim(s)")
        self.button_victim.config(bg='#DADADA', fg='black')
        self.button_victim.pack(pady=5)

        self.button_reset = tk.Button(self, text="Reset victim(s)", command=self.update_local)
        self.button_reset.config(bg='#DADADA', fg='black')
        self.button_reset.pack(pady=5)

    def update_local(self):
        self.ip_box.delete(0, tk.END)

        # TODO: Create TextBox where users have to fill in the netmask
        options = dis.arp_ping(netmask="192.168.2.0/24")
        for option in options:
            self.ip_box.insert(tk.END, option)

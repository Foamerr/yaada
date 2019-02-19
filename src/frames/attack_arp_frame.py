import tkinter as tk
import discovery as dis
import netifaces
import re


class AttackARPFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for selecting the target
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.label_ip = tk.Label(self, text="IP of network to scan")
        self.label_ip.config(bg='#DADADA', fg='black')
        self.label_ip.pack(side='top', pady=5)

        self.textbox_ip = tk.Entry(self, width=50)
        self.textbox_ip.insert(0, self.get_local_ip())
        self.textbox_ip.pack(side='top', pady=5)

        # TODO: Display more information about ip address/mac address?
        # See: https://www.studytonight.com/network-programming-in-python/integrating-port-scanner-with-nmap
        self.button_scan = tk.Button(self, text="Scan local network", command=self.update_local, width=50)
        self.button_scan.config(bg='#DADADA', fg='black')
        self.button_scan.pack(side='top', pady=15)

        self.ip_box = tk.Listbox(self, width=75, selectmode=tk.SINGLE)
        self.ip_box.pack(side='top', pady=5)

        # TODO: add command for setting global target(s)
        self.button_target = tk.Button(self, text="Set target", command=self.set_target, width=50)
        self.button_target.config(bg='#DADADA', fg='black')
        self.button_target.pack(pady=5)

        self.button_victim = tk.Button(self, text="Set victim", command=self.set_victim, width=50)
        self.button_victim.config(bg='#DADADA', fg='black')
        self.button_victim.pack(padx=5)

        self.label_victim = tk.Label(self, text="Victim: None")
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.pack(side='top', pady=5)

        self.label_target = tk.Label(self, text="Target: None")
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.pack(side='top', pady=5)

        self.button_start = tk.Button(self, text="Start poisoning", command=self.start_arp)
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.pack(side='top', pady=5)

        self.button_stop = tk.Button(self, text="Stop poisoning", command=self.stop_arp)
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.pack(side='top', pady=5)

    def update_local(self):
        self.ip_box.delete(0, tk.END)

        self.controller.log.update_stat('Searching for local network addresses')
        self.controller.log.update_out('searching for local network addresses')

        options = dis.arp_ping(netmask=self.textbox_ip.get())
        if not len(options) == 0:
            for option in options:
                # TODO: Add "(self)" behind own MAC-ip address combo so that the user knows their own address
                self.ip_box.insert(tk.END, option)
        else:
            self.ip_box.insert(tk.END, "could not find any IP addresses")
            self.controller.log.update_out('could not find any IP addresses')

        self.controller.log.update_stat('Finished searching for local network addresses')
        self.controller.log.update_out('finished searching for local network addresses')

    @staticmethod
    def get_local_ip():
        # TODO: Add text escaping (special symbols) & verify if valid ip?
        gws = netifaces.gateways()
        return str(gws['default'][netifaces.AF_INET][0]) + '/24'

    def set_target(self):
        # TODO: Extend to MULTIPLE rather than SINGLE
        target = self.ip_box.get(self.ip_box.curselection())

        if len(target) == 0:
            # TODO: display error message
            print('No target selected')
        else:
            self.ip_box.select_clear(0, tk.END)
            target = str(target).split('at', 1)[1]
            self.controller.log.update_out(target + ' has been set as the target IP address')
            self.label_target.config(text=('Target: ' + target))

    def set_victim(self):
        victim = self.ip_box.get(self.ip_box.curselection())

        if len(victim) == 0:
            # TODO: display error message
            print('No target selected')
        else:
            self.ip_box.select_clear(0, tk.END)
            victim = str(victim).split('at', 1)[1]
            self.controller.log.update_out(victim + ' has been set as the victim IP address')
            self.label_victim.config(text=('Victim: ' + victim))

    def start_arp(self):
        return

    def stop_arp(self):
        return

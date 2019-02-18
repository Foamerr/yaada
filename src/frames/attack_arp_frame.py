import tkinter as tk
import discovery as dis


class AttackARPFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for selecting the target
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.label_ip = tk.Label(self, text="IP of network to scan")
        self.label_ip.pack(side='top', pady=5)

        self.textbox_ip = tk.Entry(self, width=50)
        self.textbox_ip.insert(0, self.get_local_ip())
        self.textbox_ip.pack(side='top', pady=5)

        self.button_scan = tk.Button(self, text="Scan local network", command=self.update_local, width=50)
        self.button_scan.config(bg='#DADADA', fg='black')
        self.button_scan.pack(side='top', pady=15)

        self.ip_box = tk.Listbox(self, width=75, selectmode=tk.MULTIPLE)
        self.ip_box.pack(side='top', pady=5)

        # TODO: add command for setting global target(s)
        self.button_target = tk.Button(self, text="Set victim(s)", command=self.set_target, width=50)
        self.button_target.config(bg='#DADADA', fg='black')
        self.button_target.pack(pady=5)

        # TODO: change command or update status text display based on cases (2 in total)
        self.button_reset = tk.Button(self, text="Clear victim(s)", command=self.update_local, width=50)
        self.button_reset.config(bg='#DADADA', fg='black')
        self.button_reset.pack(pady=5)

    def update_local(self):
        self.ip_box.delete(0, tk.END)

        self.controller.log.update_stat('Searching for local network addresses')
        self.controller.log.update_out('searching for local network addresses')

        options = dis.arp_ping(netmask=self.textbox_ip.get())
        if not len(options) == 0:
            for option in options:
                self.ip_box.insert(tk.END, option)
        else:
            self.ip_box.insert(tk.END, "could not find any IP addresses")
            self.controller.log.update_out('could not find any IP addresses')

        self.controller.log.update_stat('Finished searching for local network addresses')
        self.controller.log.update_out('finished searching for local network addresses')

    def get_local_ip(self):
        return "192.168.2.0/24"

    def set_target(self):
        targets = ['Stijn']

        if len(targets) > 1:
            self.controller.log.update_out('')
            for target in targets[:-1]:
                self.controller.log.update_out((target + ', '), append=True)
            self.controller.log.update_out('and ' + targets[-1] + ' have been set as targets', append=True)
        else:
            self.controller.log.update_out(targets[0] + ' has been set as the target')

import tkinter as tk
import discovery as dis
import netifaces
from tkinter import messagebox


class AttackARPFrame(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for selecting the target
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')
        self.victims = []
        self.target = None

        top_frame, label_frame, button_set_frame, bottom_frame = tk.Frame(self), tk.Frame(self, height=15), tk.Frame(self, height=15), tk.Frame(self)
        button_set_frame.configure(bg='#DADADA'), top_frame.configure(bg='#DADADA')
        label_frame.configure(bg='#DADADA'), bottom_frame.configure(bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        button_set_frame.pack(side="top", fill="both", expand=True)
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        label_frame.pack(side="bottom", fill="both", expand=True)

        self.label_ip = tk.Label(top_frame, text="Gateway to use (already provided is default)",
                                 font=(self.controller.font, self.controller.font_size))
        self.label_ip.config(bg='#DADADA', fg='black')
        self.label_ip.pack(side='top', pady=5)

        self.textbox_ip = tk.Entry(top_frame, width=20, font=(self.controller.font, self.controller.font_size),
                                   justify='center')
        self.textbox_ip.insert(0, (self.get_default_gateway() + '/24'))
        self.textbox_ip.pack(side='top', pady=5)

        # TODO: Display more information about ip address/mac address?
        # See: https://www.studytonight.com/network-programming-in-python/integrating-port-scanner-with-nmap
        self.button_scan = tk.Button(top_frame, text="Scan", command=self.update_local, width=30,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_scan.config(bg='#DADADA', fg='black')
        self.button_scan.pack(side='top', pady=5)

        self.ip_box = tk.Listbox(top_frame, width=45, selectmode=tk.MULTIPLE,
                                 font=(self.controller.font, self.controller.font_size), justify='center',
                                 activestyle='none')
        self.ip_box.pack(side='top', pady=10)

        self.button_victim = tk.Button(button_set_frame, text="Set victim(s)", command=self.set_victim, width=15,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_victim.config(bg='#DADADA', fg='black')
        self.button_victim.place(relx=0.70, rely=0.5, anchor=tk.CENTER)

        self.button_target = tk.Button(button_set_frame, text="Set target", command=self.set_target, width=15,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_target.config(bg='#DADADA', fg='black')
        self.button_target.place(relx=0.30, rely=0.5, anchor=tk.CENTER)

        self.label_victim = tk.Label(label_frame, text="Victim(s): None", font=(self.controller.font,
                                                                             self.controller.font_size))
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.place(relx=0.70, rely=0.5, anchor=tk.CENTER)

        self.label_target = tk.Label(label_frame, text="Target: None", font=(self.controller.font,
                                                                             self.controller.font_size))
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.place(relx=0.30, rely=0.5, anchor=tk.CENTER)

        self.button_start = tk.Button(bottom_frame, text="Start spoofing", command=self.start_arp, width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.pack(side='top', pady=10)
        self.button_start.config(state=tk.DISABLED)

        self.button_stop = tk.Button(bottom_frame, text="Stop spoofing", command=self.stop_arp, width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.pack(side='top')
        self.button_stop.config(state=tk.DISABLED)

    def update_local(self):
        address = self.textbox_ip.get()

        self.ip_box.delete(0, tk.END)
        self.controller.log.update_stat('Searching for local network addresses')
        self.controller.log.update_out('searching for local network addresses')

        options = dis.arp_ping(netmask=address)
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
    def get_default_gateway():
        # TODO: Text escaping/converting to host model, and adding (default) behind the text?
        gws = netifaces.gateways()
        return str(gws['default'][netifaces.AF_INET][0])

    def set_target(self):
        try:
            target = self.ip_box.get(self.ip_box.curselection())
            self.ip_box.select_clear(0, tk.END)
            target = str(target).split('at ', 1)[1]
            self.controller.log.update_out(target + ' has been set as the target IP address')
            self.label_target.config(text=('Target: ' + target))
            self.enable_start()
            self.target = target
        except tk.TclError:
            self.dis_err('exactly one target')

    def set_victim(self):
        selection = self.ip_box.curselection()

        if len(selection) != 0:
            result = []
            if len(selection) > 1:
                for i in selection:
                    entry = self.ip_box.get(i)
                    entry = str(entry).split('at ', 1)[1]
                    result.append(entry)
                strings = ', '.join(result)
                self.controller.log.update_out(strings + ' have been set as the victims')
                self.label_victim.config(text='Victims set, see log for details')
                self.enable_start()
                self.victims = strings
            else:
                entry = str(self.ip_box.get(selection)).split('at ', 1)[1]
                self.controller.log.update_out(entry + ' has been set as the victims')
                self.label_victim.config(text='Victim: ' + entry)
                self.enable_start()
                self.victims = [entry]

            self.ip_box.select_clear(0, tk.END)
        else:
            self.dis_err('at least one victim')

    def enable_start(self):
        victim_text = self.label_victim.cget('text')
        target_text = self.label_target.cget('text')

        if (victim_text != 'Victim(s): None') and (target_text != 'Target: None'):
            self.button_start.config(state=tk.NORMAL)
            self.controller.log.update_out('both victim and target set have been set')
            self.controller.log.update_out('ready for action')

    def start_arp(self):
        # TODO: implement in arp_attack.py (?)

        if self.target in self.victims:
            messagebox.showerror("Error", "You cannot not set the target as a victim.")
        else:
            self.button_stop.config(state=tk.NORMAL)
            self.button_start.config(state=tk.DISABLED)

            # Convert these to method parameters rather than global vars
            print(self.target)
            print(self.victims)

            self.controller.log.update_out('starting ARP spoofing')
            self.controller.log.update_stat('ARP spoofing is active')
            return

    def stop_arp(self):
        # TODO: implement in arp_attack.py (?)
        self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)

        self.target = None
        self.victims = []

        self.controller.log.update_out('stopping ARP spoofing')
        self.controller.log.update_stat('ARP spoofing is inactive')
        return

    @staticmethod
    def dis_err(case):
        """
        Displays a message box containing error
        """
        messagebox.showerror("Error", "Please make sure to first select " + case + " IP before pressing this button.")

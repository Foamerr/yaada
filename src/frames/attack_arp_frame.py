import tkinter as tk
from tkinter import messagebox
import dns.resolver

import discovery as dis
from attacks.arp_attack import ArpPois

try:
    from frames.attack_dns_frame import *
except ImportError:
    import attack_dns_frame


class AttackARPFrame(tk.Frame):

    def __init__(self, parent, controller):
        """ Initialises GUI of the frame used for selecting the target """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')
        self.victims = None
        self.victims_mac = None
        self.target = None
        self.target_mac = None
        self.font = "Georgia"
        self.font_size = 11
        self.arp = None
        self.is_poisoning = False
        self.log = self.controller.log
        self.attacker_ip = None
        self.ns = None

        # FRAMES SETUP #
        top_frame = tk.Frame(self)
        self.labelframe_in = tk.LabelFrame(top_frame,
                                           text="Input",
                                           font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_in.config(bg='#DADADA', fg='black')
        self.labelframe_in.pack(pady=15)

        button_set_frame, below_buttons_frame, bottom_frame = tk.Frame(self.labelframe_in, height=55), \
                                                              tk.Frame(self.labelframe_in), tk.Frame(self)
        button_start_frame = tk.Frame(bottom_frame)

        button_set_frame.configure(bg='#DADADA'), top_frame.configure(bg='#DADADA')
        below_buttons_frame.configure(bg='#DADADA')
        button_start_frame.configure(bg='#DADADA'), bottom_frame.configure(bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        below_buttons_frame.pack(side="bottom", fill="both", expand=True)
        button_set_frame.pack(side="bottom", fill="both", expand=True)
        bottom_frame.pack(side="top", fill="both", expand=True)
        button_start_frame.pack(side="bottom", fill="both", expand=True)

        # INPUT #
        self.label_ip = tk.Label(self.labelframe_in,
                                 text="Scan the network and select the targets and victims",
                                 font=(self.controller.font, self.controller.font_size))
        self.label_ip.config(bg='#DADADA', fg='black')
        self.label_ip.pack(side='top', pady=5)

        self.button_scan = tk.Button(self.labelframe_in,
                                     text="Scan",
                                     command=self.update_local,
                                     width=30,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_scan.config(bg='#DADADA', fg='black')
        self.button_scan.pack(side='top', pady=5)

        self.ip_box = tk.Listbox(self.labelframe_in,
                                 width=53,
                                 height=7,
                                 selectmode=tk.MULTIPLE,
                                 font=(self.controller.font,
                                       self.controller.font_size),
                                 activestyle='none')
        self.ip_box.pack(side='top', padx=10, pady=5)

        self.button_victim = tk.Button(button_set_frame,
                                       text="Set victims",
                                       command=self.set_victim,
                                       width=15,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_victim.config(bg='#DADADA', fg='black')
        self.button_victim.place(relx=0.70, rely=0.5, anchor=tk.CENTER)

        self.button_target = tk.Button(button_set_frame,
                                       text="Set target",
                                       command=self.set_target,
                                       width=15,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_target.config(bg='#DADADA', fg='black')
        self.button_target.place(relx=0.30, rely=0.5, anchor=tk.CENTER)

        # SETTINGS #
        self.labelframe_out = tk.LabelFrame(bottom_frame,
                                            text="Settings",
                                            font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_out.config(bg='#DADADA', fg='black')
        self.labelframe_out.pack(pady=0)

        self.label_victim = tk.Label(self.labelframe_out,
                                     text="Victims: None",
                                     font=(self.controller.font,
                                           self.controller.font_size),
                                     width=53,
                                     wraplength=450,
                                     anchor=tk.W,
                                     justify=tk.LEFT)
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.pack(side='top', padx=10, pady=5)

        self.label_target = tk.Label(self.labelframe_out,
                                     text="Target: None",
                                     font=(self.controller.font,
                                           self.controller.font_size),
                                     width=53,
                                     wraplength=450,
                                     anchor=tk.W,
                                     justify=tk.LEFT)
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.pack(side='top', padx=10, pady=5)

        # BUTTONS #
        self.button_start = tk.Button(button_start_frame,
                                      text="Start poisoning",
                                      command=self.start_arp,
                                      width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.place(relx=0.30, rely=0.5, anchor=tk.CENTER)
        self.button_start.config(state=tk.DISABLED)

        self.button_stop = tk.Button(button_start_frame,
                                     text="Stop poisoning",
                                     command=self.stop_arp,
                                     width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.place(relx=0.70, rely=0.5, anchor=tk.CENTER)
        self.button_stop.config(state=tk.DISABLED)

        self.label_time = tk.Label(below_buttons_frame,
                                   text="Please enter a time interval to send packets\n(default is every 10 seconds)",
                                   font=(self.controller.font, self.controller.font_size))
        self.label_time.config(bg='#DADADA', fg='black')
        self.label_time.pack(side='top', pady=5)

        self.max_value = tk.StringVar()
        self.max_value.trace('w', self.limit_size)

        self.textbox_time = tk.Entry(below_buttons_frame,
                                     width=3,
                                     justify=tk.CENTER,
                                     textvariable=self.max_value,
                                     font=(self.controller.font, self.controller.font_size))
        self.textbox_time.pack(side='top', padx=10, pady=5)

        self.textbox_time.insert(tk.END, 10)

    def limit_size(self, *args):
        value = self.max_value.get()
        if len(value) > 3:
            self.max_value.set(value[:3])

    def update_local(self):
        """ Scan the network and store all found IP/MAC combinations in a listbox """
        # interface = self.textbox_ip.get(self.textbox_ip.curselection())

        self.ip_box.delete(0, tk.END)
        self.log.update_stat('Searching for local network addresses')
        self.log.update_out('Searching for local network addresses')

        try:
            default = dns.resolver.get_default_resolver()
            self.ns = default.nameservers[0]
        except:
            pass

        combinations = dis.scan_local_network()
        if combinations is None:
            messagebox.showerror("Error", "Something went wrong with scanning the network.")

        self.attacker_ip = dis.get_local_host_ip()
        local_mac = dis.mac_for_ip(self.attacker_ip)
        self.ip_box.insert(tk.END, self.attacker_ip + ' at ' + local_mac + ' (self)')

        if combinations:
            for ip in combinations:
                print(ip)
                if ip == self.ns:
                    self.ip_box.insert(tk.END, ip + ' at ' + combinations[ip] + ' (DNS NS)')
                else:
                    self.ip_box.insert(tk.END, ip + ' at ' + combinations[ip])
        else:
            self.ip_box.insert(tk.END, 'Could not find any other IP addresses')

        self.log.update_stat('Finished searching for local network addresses')
        self.log.update_out('Finished searching for local network addresses')

    def set_target(self):
        """ Sets the target (MAC/IP combination) """
        try:
            target = self.ip_box.get(self.ip_box.curselection())
            self.ip_box.select_clear(0, tk.END)

            self.target = str(target).split('at ', 1)[0]

            self.target_mac = str(target).split('at ', 1)[1]
            self.target_mac = str(self.target_mac).split(' ', 1)[0]

            self.log.update_out(self.target + ' has been set as the target IP address.')
            self.label_target.config(text=('Target: ' + self.target))

            self.enable_start()
        except tk.TclError:
            self.dis_err('exactly one target')

    def set_victim(self):
        """ Sets the victim(s) (MAC/IP combination(s)) """
        selection = self.ip_box.curselection()

        if len(selection) >= 2:
            result = []
            result_mac = []
            for i in selection:
                entry = self.ip_box.get(i)
                ip = str(entry).split(' at ', 1)[0]
                mac = str(entry).split(' at ', 1)[1]
                mac = mac.split(' ', 1)[0]
                result_mac.append(mac)
                result.append(ip)
            strings = ', '.join(result)
            self.log.update_out('The victims have been set. Check the output logs.')
            self.label_victim.config(text='Victims: ' + strings)
            self.enable_start()
            self.victims = result
            self.victims_mac = result_mac

            self.ip_box.select_clear(0, tk.END)
        else:
            self.dis_err('at least two victims')

    def enable_start(self):
        """ Checks if the start button should be enabled """
        victim_text = self.label_victim.cget('text')
        target_text = self.label_target.cget('text')

        if (victim_text != 'Victims: None') and (target_text != 'Target: None') and not self.is_poisoning:
            self.button_start.config(state=tk.NORMAL)
            self.log.update_out('Both victim and target set have been set.')
            self.log.update_out('Ready for action!')

    def start_arp(self):
        """ Starts an ARP spoofing attack on all combinations between victim pairs with respect to the target """
        if self.target is None or self.victims is None:
            messagebox.showerror(
                "Error", "You have to set a target and/or victims first.")
            return

        if self.target in self.victims:
            messagebox.showerror(
                "Error", "You cannot not set the target as a victim.")
            return

        self.button_stop.config(state=tk.NORMAL)
        self.button_start.config(state=tk.DISABLED)
        self.is_poisoning = True

        self.target = str(self.target).split(' ', 1)[0]

        victims = []
        for victim in self.victims:
            victim = str(victim).split(' ', 1)[0]
            victims.append(victim)
        self.victims = victims

        self.arp = ArpPois()
        self.arp.set_time(self.max_value.get())
        self.arp.set_victims(self.victims, self.victims_mac)
        self.arp.set_target(self.target, self.target_mac)
        self.arp.start_poisoning()

        self.log.update_out('------------------Currently ARP Poisoning----------------------------------------')
        self.log.update_out('Victim: ' + ', '.join(self.victims))
        self.log.update_out('Target: ' + self.target)
        self.log.update_out('--------------------------------------------------------------------------')

        self.log.update_stat('ARP Poisoning is active. See above logs for details.')

        # only possible to execute dns cache poisoning if two victims are used and the target mac address is
        # the mac address of the attacker
        if len(self.victims) == 2 and self.target == self.attacker_ip:
            for vic in self.victims:
                if vic == self.ns:
                    messagebox.showinfo("Possible DNS cache poisoning attack",
                                        "It is now possible to execute a DNS cache poisoning attack."
                                        " Please navigate to the `DNS cache poisoning' tab to execute this attack."
                                        "\n\nSee the log below for more information on the victims and the target.")
                    self.log.update_out('It is now possible to execute')
                    self.log.update_out('a DNS cache poisoning attack.')
                    self.controller.notebook.tab('.!mainapplication.!notebook.!attackdnsframe', state="normal")
                    dis.set_dns_settings(self.victims, self.ns)

        return

    def stop_arp(self):
        """ Stops all ARP spoofing attack """
        # self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.ip_box.delete(0, tk.END)

        self.arp.stop_poisoning()

        self.is_poisoning = False
        self.label_victim.config(text="Victims: None")
        self.label_target.config(text="Target: None")

        self.target = None
        self.victims = None

        self.log.update_out('Stopping ARP poisoning')
        self.log.update_stat('ARP poisoning is inactive')

        self.controller.notebook.tab('.!mainapplication.!notebook.!attackdnsframe', state="disabled")

        return

    @staticmethod
    def dis_err(case):
        """
        Displays a message box containing error
        """
        messagebox.showerror("Error", "Please make sure to first select " +
                             case + " IP before pressing this button.")

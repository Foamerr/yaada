import tkinter as tk
from tkinter import messagebox

import discovery as dis
# from attacks.arp_attack import ArpPoison
# from attacks.arp import *
from attacks.arp_multiple_vic import *


class AttackARPFrame(tk.Frame):

    def __init__(self, parent, controller):
        """ Initialises GUI of the frame used for selecting the target """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')
        self.victims = []
        self.victims_mac = []
        self.target = None
        self.target_mac = None
        self.font = "Georgia"
        self.font_size = 11
        self.arp = None
        self.log = self.controller.log

        # FRAMES SETUP #
        top_frame = tk.Frame(self)
        self.labelframe_in = tk.LabelFrame(top_frame,
                                           text="Input",
                                           font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_in.config(bg='#DADADA', fg='black')
        self.labelframe_in.pack(pady=15)

        button_set_frame, bottom_frame = tk.Frame(
            self.labelframe_in, height=55), tk.Frame(self)
        button_start_frame = tk.Frame(bottom_frame)

        button_set_frame.configure(
            bg='#DADADA'), top_frame.configure(bg='#DADADA')
        button_start_frame.configure(
            bg='#DADADA'), bottom_frame.configure(bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        button_set_frame.pack(side="bottom", fill="both", expand=True)
        bottom_frame.pack(side="top", fill="both", expand=True)
        button_start_frame.pack(side="bottom", fill="both", expand=True)

        # INPUT #
        self.label_ip = tk.Label(self.labelframe_in,
                                 text="Scan the network and select the targets and victims",
                                 font=(self.controller.font, self.controller.font_size))
        self.label_ip.config(bg='#DADADA', fg='black')
        self.label_ip.pack(side='top', pady=5)

        # self.textbox_ip = tk.Listbox(self.labelframe_in,
        #                              width=53,
        #                              height=3,
        #                              font=(self.controller.font, self.controller.font_size))
        # interfaces = netifaces.interfaces()
        # for interface in interfaces:
        #     self.textbox_ip.insert(0, interface)
        # self.textbox_ip.pack(side='top', pady=5)

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

    def update_local(self):
        """ Scan the network and store all found IP/MAC combinations in a listbox """
        # interface = self.textbox_ip.get(self.textbox_ip.curselection())

        self.ip_box.delete(0, tk.END)
        self.log.update_stat('Searching for local network addresses')
        self.log.update_out('searching for local network addresses')

        combinations = dis.scan_local_network()
        local_ip = dis.get_local_host_ip()
        local_mac = dis.mac_for_ip(dis.get_local_host_ip())
        self.ip_box.insert(tk.END, local_ip + ' at ' + local_mac + ' (self)')

        if combinations:
            for ip in combinations:
                print(ip)
                # if dis.get_default_gateway() == ip:
                #     self.ip_box.insert(tk.END, ip + ' at ' + combinations[ip] + ' (gateway)')
                # else:
                self.ip_box.insert(tk.END, ip + ' at ' + combinations[ip])
        else:
            self.ip_box.insert(tk.END, 'could not find any IP addresses')
            self.log.update_out('could not find any IP addresses')

        self.log.update_stat('Finished searching for local network addresses')
        self.log.update_out('finished searching for local network addresses')

    def set_target(self):
        """ Sets the target (MAC/IP combination) """
        try:
            target = self.ip_box.get(self.ip_box.curselection())
            self.ip_box.select_clear(0, tk.END)

            self.target = str(target).split('at ', 1)[0]

            self.target_mac = str(target).split('at ', 1)[1]
            self.target_mac = str(self.target_mac).split(' ', 1)[0]

            self.log.update_out(self.target + ' has been set as the target IP address')
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
                ip = str(entry).split('at ', 1)[0]
                mac = str(entry).split('at ', 1)[1]
                mac = mac.split(' ', 1)[0]
                result_mac.append(mac)
                result.append(ip)
            strings = ', '.join(result)
            self.log.update_out(strings + ' have been set as the victims')
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

        if (victim_text != 'Victims: None') and (target_text != 'Target: None'):
            self.button_start.config(state=tk.NORMAL)
            self.log.update_out('both victim and target set have been set')
            self.log.update_out('ready for action')

    def start_arp(self):
        """ Starts an ARP spoofing attack on all combinations between victim pairs with respect to the target """
        if self.target in self.victims:
            messagebox.showerror(
                "Error", "You cannot not set the target as a victim.")
        else:
            self.button_stop.config(state=tk.NORMAL)
            self.button_start.config(state=tk.DISABLED)

            # Convert these to method parameters rather than global vars
            self.target = str(self.target).split(' ', 1)[0]

            victims = []
            for victim in self.victims:
                victim = str(victim).split(' ', 1)[0]
                victims.append(victim)
            self.victims = victims

            # print("target: " + self.target)
            # print("target mac: " + self.target_mac)
            # print("all victims: " + str(self.victims))

            # self.arp = ArpPoison(target=self.target, victims=self.victims)
            # self.arp.start_poisoning()
            # self.arp = ArpSpoof()
            # for vic in self.victims:
            #     self.arp.attach_vic(vic)
            # self.arp.attach_tar(self.target, self.target_mac)

            self.arp = ArpPois()
            self.arp.set_victims(self.victims, self.victims_mac)
            self.arp.set_target(self.target, self.target_mac)
            self.arp.start()

            self.log.update_out('starting ARP poisoning')
            self.log.update_stat('ARP poisoning is active')
            return

    def stop_arp(self):
        """ Stops all ARP spoofing attack """
        self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.ip_box.delete(0, tk.END)

        self.arp.stop()

        self.label_victim.config(text="Victims: None")
        self.label_target.config(text="Target: None")

        self.target = None
        self.victims = []
        self.arp.stop_poisoning()

        self.log.update_out('stopping ARP poisoning')
        self.log.update_stat('ARP poisoning is inactive')
        return

    @staticmethod
    def dis_err(case):
        """
        Displays a message box containing error
        """
        messagebox.showerror("Error", "Please make sure to first select " +
                             case + " IP before pressing this button.")

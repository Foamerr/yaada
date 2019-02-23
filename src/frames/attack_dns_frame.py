import tkinter as tk
from tkinter import messagebox

from validation import *


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        # FRAMES SETUP #
        text_box_width = 53
        top_frame, button_set_frame, bottom_frame = tk.Frame(self), tk.Frame(self, height=15), tk.Frame(self)
        button_set_frame.configure(bg='#DADADA'), top_frame.configure(bg='#DADADA'), bottom_frame.configure(
            bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        button_set_frame.pack(side="top", fill="both", expand=True)
        bottom_frame.pack(side="bottom", fill="both", expand=True)

        # INPUT #
        self.labelframe_in = tk.LabelFrame(top_frame,
                                           text="Input",
                                           font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_in.config(bg='#DADADA', fg='black')
        self.labelframe_in.pack(pady=15)

        self.label_site = tk.Label(self.labelframe_in,
                                   text="Target domain(s) (Separate multiple with a ', ')",
                                   font=(self.controller.font, self.controller.font_size))
        self.label_site.config(bg='#DADADA', fg='black')
        self.label_site.pack(side='top', pady=5)

        self.domain = tk.Entry(self.labelframe_in,
                               font=(self.controller.font, self.controller.font_size),
                               width=text_box_width)
        self.domain.pack(side='top', padx=10, pady=5)

        self.label_victim = tk.Label(self.labelframe_in,
                                     text="Victim IP addresses (Separate multiple with a ', ')",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.pack(side='top', pady=5)

        self.victims = tk.Entry(self.labelframe_in,
                                font=(self.controller.font, self.controller.font_size),
                                width=text_box_width)
        self.victims.pack(side='top', padx=10, pady=5)

        self.label_target = tk.Label(self.labelframe_in,
                                     text="Target IP",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.pack(side='top', pady=5)

        self.target = tk.Entry(self.labelframe_in,
                               font=(self.controller.font, self.controller.font_size),
                               width=text_box_width)
        self.target.pack(side='top', padx=10, pady=5)

        # BUTTONS #
        self.button_start = tk.Button(button_set_frame,
                                      text="Start spoofing",
                                      command=self.start_dns,
                                      width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.place(relx=0.30, rely=0.5, anchor=tk.CENTER)

        self.button_stop = tk.Button(button_set_frame,
                                     text="Stop spoofing",
                                     command=self.stop_dns,
                                     width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.place(relx=0.70, rely=0.5, anchor=tk.CENTER)

        self.button_stop.config(state=tk.DISABLED)

        # OUTPUT #
        # TODO: add wraplength for wrapping long text
        self.labelframe_out = tk.LabelFrame(bottom_frame,
                                            text="Settings",
                                            font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_out.config(bg='#DADADA', fg='black')
        self.labelframe_out.pack(pady=15)

        self.label_site_out = tk.Label(self.labelframe_out,
                                       text="Target domain(s): None",
                                       font=(self.controller.font, self.controller.font_size),
                                       width=text_box_width,
                                       anchor=tk.W,
                                       justify=tk.LEFT)
        self.label_site_out.config(bg='#DADADA', fg='black')
        self.label_site_out.pack(side='top', padx=10, pady=15)

        self.victims_out = tk.Label(self.labelframe_out,
                                    text="Victim(s): None",
                                    font=(self.controller.font, self.controller.font_size),
                                    width=text_box_width,
                                    anchor=tk.W,
                                    justify=tk.LEFT)
        self.victims_out.config(bg='#DADADA', fg='black')
        self.victims_out.pack(side='top', padx=10, pady=15)

        self.target_out = tk.Label(self.labelframe_out,
                                   text="Target: None",
                                   font=(self.controller.font, self.controller.font_size),
                                   width=text_box_width,
                                   anchor=tk.W,
                                   justify=tk.LEFT)
        self.target_out.config(bg='#DADADA', fg='black')
        self.target_out.pack(side='top', padx=10, pady=15)

    @staticmethod
    def get_targets(unfiltered_list):
        unfiltered_list = unfiltered_list.split(', ')
        return unfiltered_list

    def start_dns(self):
        domains = self.domain.get()
        target = self.target.get()
        victims = self.victims.get()

        domains = self.get_targets(domains)
        victims = self.get_targets(victims)

        print(domains)
        print(victims)

        if not are_valid_address([target]):
            messagebox.showerror("Error", "The target IP address is not a valid IPv4 or IPv6 IP address.")
            return

        if not are_valid_address(victims):
            messagebox.showerror("Error", "The victim IP address is not a valid IPv4 or IPv6 IP address.")
            return

        self.controller.log.update_out('Domain, target, and victim successfully set')

        # TODO: implement in dns_attack.py (?)
        self.controller.log.update_out('Starting DNS spoofing')

        self.controller.log.update_stat("DNS spoofing provided victim's domain with target IP")
        self.controller.log.update_out('DNS spoofing active')

        self.button_start.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.ENABLED)
        self.label_site_out.configure(text="Target domain(s): " + self.domain.get())
        self.victims_out.configure(text="Victim(s): " + self.victims.get())
        self.target_out.configure(text="Target: " + self.target.get())

    def stop_dns(self):
        # TODO: implement in dns_attack.py (?)
        self.label_site_out.configure(text="Target domain(s): None")
        self.victims_out.configure(text="Victim(s): None")
        self.target_out.configure(text="Target: None")

        self.controller.log.update_out('Stopping DNS spoofing')

        self.controller.log.update_out('DNS spoofing stopped')
        self.controller.log.update_stat("Stopped DNS spoofing")
        self.button_start.config(state=tk.ENABLED)
        self.button_stop.config(state=tk.DISABLED)
        return

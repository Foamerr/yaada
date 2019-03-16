import tkinter as tk
import urllib
from tkinter import messagebox

import discovery as dis
from attacks.dns_attack import DnsPois


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """ Initialises GUI of the frame used for selecting the target """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')
        self.font = "Georgia"
        self.font_size = 11
        self.arp = None
        self.dns = None
        self.domain = None
        self.fake_domain = None
        self.auth_dns = None
        self.rec_dns = None
        self.log = self.controller.log

        # FRAMES SETUP #
        top_frame = tk.Frame(self)
        self.labelframe_in = tk.LabelFrame(top_frame,
                                           text="Input",
                                           font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_in.config(bg='#DADADA', fg='black')
        self.labelframe_in.pack(pady=15)

        bottom_frame = tk.Frame(self)
        button_start_frame = tk.Frame(bottom_frame)

        top_frame.configure(bg='#DADADA')
        button_start_frame.configure(bg='#DADADA'), bottom_frame.configure(bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        bottom_frame.pack(side="top", fill="both", expand=True)
        button_start_frame.pack(side="bottom", fill="both", expand=True)

        # INPUT #
        self.label_intro = tk.Label(self.labelframe_in,
                                    text="The DNS cache poisoning attack will be performed on victims "
                                         "from the ARP Poisoning attack. Please write down the IP address of the "
                                         "DNS name server below.",
                                    wraplength=450,
                                    justify=tk.LEFT,
                                    font=(self.controller.font, self.controller.font_size))
        self.label_intro.config(bg='#DADADA', fg='black')
        self.label_intro.pack(side='top', pady=5)

        self.textbox_ns = tk.Entry(self.labelframe_in,
                                   width=53,
                                   font=(self.controller.font, self.controller.font_size))
        self.textbox_ns.pack(side='top', padx=10, pady=5)

        self.label_domain = tk.Label(self.labelframe_in,
                                     text="Target domain (e.g., www.realsite.com)",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_domain.config(bg='#DADADA', fg='black')
        self.label_domain.pack(side='top', pady=5)

        self.textbox_domain = tk.Entry(self.labelframe_in,
                                       width=53,
                                       font=(self.controller.font, self.controller.font_size))
        self.textbox_domain.pack(side='top', padx=10, pady=10)

        self.button_domain = tk.Button(self.labelframe_in,
                                       text="Set domain",
                                       command=self.set_domain,
                                       width=30,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_domain.config(bg='#DADADA', fg='black')
        self.button_domain.pack(side='top', pady=10)

        self.label_domain_fake = tk.Label(self.labelframe_in,
                                          text="Fake IP (the IP the victim will visit when trying to visit the domain above)",
                                          font=(self.controller.font, self.controller.font_size))
        self.label_domain_fake.config(bg='#DADADA', fg='black')
        self.label_domain_fake.pack(side='top', pady=10)

        self.textbox_domain_fake = tk.Entry(self.labelframe_in,
                                            width=53,
                                            font=(self.controller.font, self.controller.font_size))
        self.textbox_domain_fake.pack(side='top', padx=10, pady=10)

        self.button_domain_fake = tk.Button(self.labelframe_in,
                                            text="Set fake IP",
                                            command=self.set_fake_domain,
                                            width=30,
                                            font=(self.controller.font, self.controller.font_size))
        self.button_domain_fake.config(bg='#DADADA', fg='black')
        self.button_domain_fake.pack(side='top', pady=10)

        # SETTINGS #
        self.labelframe_out = tk.LabelFrame(bottom_frame,
                                            text="Settings",
                                            font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_out.config(bg='#DADADA', fg='black')
        self.labelframe_out.pack(pady=0)

        self.label_domain = tk.Label(self.labelframe_out,
                                     text="Target domain: None",
                                     font=(self.controller.font, self.controller.font_size),
                                     width=53,
                                     wraplength=450,
                                     anchor=tk.W,
                                     justify=tk.LEFT)
        self.label_domain.config(bg='#DADADA', fg='black')
        self.label_domain.pack(side='top', padx=10, pady=10)

        self.label_fake_domain = tk.Label(self.labelframe_out,
                                          text="Fake IP: None",
                                          font=(self.controller.font, self.controller.font_size),
                                          width=53,
                                          wraplength=450,
                                          anchor=tk.W,
                                          justify=tk.LEFT)
        self.label_fake_domain.config(bg='#DADADA', fg='black')
        self.label_fake_domain.pack(side='top', padx=10, pady=10)

        # BUTTONS #
        self.button_start = tk.Button(button_start_frame,
                                      text="Start spoofing",
                                      command=self.start_dns,
                                      width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.place(relx=0.30, rely=0.5, anchor=tk.CENTER)
        self.button_start.config(state=tk.DISABLED)

        self.button_stop = tk.Button(button_start_frame,
                                     text="Stop spoofing",
                                     command=self.stop_dns,
                                     width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.place(relx=0.70, rely=0.5, anchor=tk.CENTER)
        self.button_stop.config(state=tk.DISABLED)

    def set_domain(self):
        """ Sets the domain """
        self.domain = self.textbox_domain.get()

        # if self.check_url(self.domain):
        self.log.update_out(self.domain + ' has been set as the target domain')
        self.label_domain.config(text=('Target domain: ' + self.domain))
        self.enable_start()
        # else:
        #    messagebox.showerror("Error", "Please make sure the domain has been correctly formatted.")

    def set_fake_domain(self):
        """ Sets the domain """
        self.fake_domain = self.textbox_domain_fake.get()
        self.log.update_out(self.fake_domain + ' has been set as the fake ip')
        self.label_fake_domain.config(text=('Fake IP: ' + self.fake_domain))
        self.enable_start()

    def enable_start(self):
        """ Checks if the start button should be enabled """
        fake_domain_text = self.label_fake_domain.cget('text')
        domain_text = self.label_domain.cget('text')

        if (fake_domain_text != 'Fake IP: None') and (domain_text != 'Target domain: None') and self.textbox_ns.get():
            self.button_start.config(state=tk.NORMAL)
            self.log.update_out('Both victim(s) and domain(s) set have been set')
            self.log.update_out('Ready for action!')

    def start_dns(self):
        """ Starts a DNS spoofing attack on all combinations between victim pairs with respect to the target """
        victims, target = dis.get_dns_settings()
        if self.textbox_ns.get() not in victims:
            messagebox.showerror("Error", "It seems like the DNS name server you set is not in the "
                                          "list of victims you used ARP poisoning on.")
            return

        for vic in victims:
            if self.textbox_ns.get() == vic:
                self.rec_dns = vic
            else:
                self.auth_dns = vic

        self.button_stop.config(state=tk.NORMAL)
        self.button_start.config(state=tk.DISABLED)

        self.controller.log.update_out('Starting DNS spoofing')

        self.dns = DnsPois()
        self.dns.set(self.auth_dns, self.rec_dns, self.fake_domain, self.domain)
        self.dns.start()

        self.controller.log.update_stat('DNS spoofing is active')

        self.log.update_out('------------------Currently DNS Poisoning----------------------------------------')
        self.log.update_out('Target domain: ' + self.domain)
        self.log.update_out('Fake IP: ' + self.fake_domain)
        self.log.update_out('DNS Auth. server: ' + self.auth_dns)
        self.log.update_out('DNS NS: ' + self.rec_dns)
        self.log.update_out('--------------------------------------------------------------------------')

    def stop_dns(self):
        """ Stops all DNS spoofing attack """
        self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.textbox_domain_fake.delete(0, tk.END)
        self.textbox_domain.delete(0, tk.END)

        self.label_fake_domain.config(text="Fake IP: None")
        self.label_domain.config(text="Target domain: None")

        self.controller.log.update_out('DNS spoofing stopped')
        self.controller.log.update_stat("Stopped DNS spoofing")

    @staticmethod
    def dis_err(case):
        """ Displays a message box containing error """
        messagebox.showerror("Error", "Please make sure to select " + case + " IP before pressing this button.")

    @staticmethod
    def check_url(url):
        try:
            error_code = urllib.request.urlopen(url).getcode()
            if error_code == 200:
                return True
            else:
                return False
        except:
            return False

import tkinter as tk
import urllib
from tkinter import messagebox

import discovery as dis
from attacks.dns_attack import DnsPois


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for selecting the target
        """
        tk.Frame.__init__(self, parent)
        self.poison_vic = False
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
        self.save_traffic = False

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
                                         "from the ARP Poisoning attack.",
                                    wraplength=450,
                                    justify=tk.LEFT,
                                    font=(self.controller.font, self.controller.font_size))
        self.label_intro.config(bg='#DADADA', fg='black')
        self.label_intro.pack(side='top', pady=2)

        self.label_domain = tk.Label(self.labelframe_in,
                                     text="Target domain (e.g., www.realsite.com)",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_domain.config(bg='#DADADA', fg='black')
        self.label_domain.pack(side='top', pady=2)

        self.textbox_domain = tk.Entry(self.labelframe_in,
                                       width=53,
                                       font=(self.controller.font, self.controller.font_size))
        self.textbox_domain.pack(side='top', padx=10, pady=2)

        self.button_domain = tk.Button(self.labelframe_in,
                                       text="Set domain",
                                       command=self.set_domain,
                                       width=30,
                                       font=(self.controller.font, self.controller.font_size))
        self.button_domain.config(bg='#DADADA', fg='black')
        self.button_domain.pack(side='top', pady=2)

        self.label_domain_fake = tk.Label(self.labelframe_in,
                                          text="Fake IP (the IP the victim will visit when trying to visit the domain above)",
                                          wraplength=450,
                                          font=(self.controller.font, self.controller.font_size))
        self.label_domain_fake.config(bg='#DADADA', fg='black')
        self.label_domain_fake.pack(side='top', pady=2)

        self.textbox_domain_fake = tk.Entry(self.labelframe_in,
                                            width=53,
                                            font=(self.controller.font, self.controller.font_size))
        self.textbox_domain_fake.pack(side='top', padx=10, pady=2)

        self.button_domain_fake = tk.Button(self.labelframe_in,
                                            text="Set fake IP",
                                            command=self.set_fake_domain,
                                            width=30,
                                            font=(self.controller.font, self.controller.font_size))
        self.button_domain_fake.config(bg='#DADADA', fg='black')
        self.button_domain_fake.pack(side='top', pady=2)

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
        self.label_domain.pack(side='top', padx=10, pady=2)

        self.label_fake_domain = tk.Label(self.labelframe_out,
                                          text="Fake IP: None",
                                          font=(self.controller.font, self.controller.font_size),
                                          width=53,
                                          wraplength=450,
                                          anchor=tk.W,
                                          justify=tk.LEFT)
        self.label_fake_domain.config(bg='#DADADA', fg='black')
        self.label_fake_domain.pack(side='top', padx=10, pady=2)

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

        self.ck = tk.StringVar()
        self.ck.set("0")
        self.save = tk.Checkbutton(self.labelframe_in,
                                   text="Save traffic",
                                   font=(self.controller.font, self.controller.font_size),
                                   variable=self.ck)
        self.save.config(bg='#DADADA', fg='black')
        self.save.pack(side='top', pady=5)

        self.pois_vic = tk.StringVar()
        self.pois_vic.set("0")
        self.vic = tk.Checkbutton(self.labelframe_in,
                                   text="Poison victim host instead of authoritative DNS server",
                                   font=(self.controller.font, self.controller.font_size),
                                   variable=self.pois_vic)
        self.vic.config(bg='#DADADA', fg='black')
        self.vic.pack(side='top', pady=5)

    def set_domain(self):
        """ Sets the domain """
        self.domain = self.textbox_domain.get()
        # error handling
        try:
            self.domain = self.domain.split('www.', 1)[1]
        except:
            messagebox.showerror("Error",
                                 "Please check the format of your provided domain and correct it.".format(self.domain))
            return

        # try:
        #     self.auth_dns = dis.get_authoritative_nameserver(self.domain)
        # except:
        #     messagebox.showerror("Error", "We could not obtain the authoritative DNS server for {0}.\n\n"
        #                                   "See if you can reach this domain with your internet connection. If not,"
        #                                   "then this could be the reason.".format(self.domain))
        #     return

        self.log.update_out(self.domain + ' has been set as the target domain')
        self.label_domain.config(text=('Target domain: ' + self.domain))
        self.enable_start()

    def set_fake_domain(self):
        """
        Sets the domain
        """
        self.fake_domain = self.textbox_domain_fake.get()
        self.log.update_out(self.fake_domain + ' has been set as the fake ip')
        self.label_fake_domain.config(text=('Fake IP: ' + self.fake_domain))
        self.enable_start()

    def enable_start(self):
        """
        Checks if the start button should be enabled
        """
        fake_domain_text = self.label_fake_domain.cget('text')
        domain_text = self.label_domain.cget('text')

        if (fake_domain_text != 'Fake IP: None') and (domain_text != 'Target domain: None'):
            self.button_start.config(state=tk.NORMAL)
            self.log.update_out('Both victim(s) and domain(s) set have been set')
            self.log.update_out('Ready for action!')

    def start_dns(self):
        """
        Starts a DNS spoofing attack on all combinations between victim pairs with respect to the target
        """
        victims, self.rec_dns = dis.get_dns_settings()
        print("victims: " + str(victims))
        for vic in victims:
            if vic != str(self.rec_dns):
                self.auth_dns = vic

        # deal with saving the traffic in a pcap file
        if self.ck.get() is not "0":
            self.save_traffic = True

        if self.pois_vic.get() is not "0":
            self.poison_vic = True

        if self.auth_dns is None or self.rec_dns is None or self.domain is None:
            messagebox.showerror(
                "Error", "Make sure you fill in all the required information above.")
            return

        print(self.rec_dns)
        print(self.domain)
        print(self.auth_dns)

        if self.auth_dns not in victims:
            messagebox.showerror("Error",
                                 "The authoritative DNS server for that domain ({0}) is currently not a victim.\n\n"
                                 "There is currently no ARP cache poisoning between the authoritative DNS server and the "
                                 "DNS nameserver. This means we cannot perform a DNS cache poisoning attack.\n\n"
                                 "Please execute the ARP poisoning attack again with the DNS nameserver and authoritative server as victims.".format(
                                     self.auth_dns))
            return

        self.button_stop.config(state=tk.NORMAL)
        self.button_start.config(state=tk.DISABLED)

        self.controller.log.update_out('Starting DNS spoofing')

        print("Poisoning vic instead? : " + str(self.poison_vic))

        self.dns = DnsPois()
        self.dns.set(self.auth_dns, self.rec_dns, self.fake_domain, self.domain, self.save_traffic, self.poison_vic)
        self.dns.start()

        self.controller.log.update_stat('DNS spoofing is active')

        self.log.update_out('------------------Currently DNS Poisoning----------------------------------------')
        self.log.update_out('Target domain: ' + self.domain)
        self.log.update_out('Fake IP: ' + self.fake_domain)
        self.log.update_out('DNS Auth. server: ' + self.auth_dns)
        self.log.update_out('DNS NS: ' + self.rec_dns)
        self.log.update_out('--------------------------------------------------------------------------')

    def stop_dns(self):
        """
        Stops all DNS spoofing attack
        """
        # self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.textbox_domain_fake.delete(0, tk.END)
        self.textbox_domain.delete(0, tk.END)

        self.dns.stop_poisoning()

        self.label_fake_domain.config(text="Fake IP: None")
        self.label_domain.config(text="Target domain: None")

        self.domain = None
        self.fake_domain = None
        self.auth_dns = None
        self.rec_dns = None
        self.poison_vic = False

        self.controller.log.update_out('DNS spoofing stopped')
        self.controller.log.update_stat('Stopped DNS spoofing')

        if self.save_traffic:
            messagebox.showinfo("Saved trafic", "You can observe the saved traffic under the `pcap_files' folder. This "
                                            "file can be opened with Wireshark. Here, one can observe the traffic "
                                            "that was involved during the ARP poisoning and"
                                            "DNS cache poisoning attack.")
            self.save_traffic = False

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

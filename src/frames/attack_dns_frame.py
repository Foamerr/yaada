import tkinter as tk
from validation import *
from tkinter import messagebox


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        top_frame = tk.Frame(self)
        top_frame.configure(bg='#DADADA')

        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg='#DADADA')

        top_frame.pack(side="top", fill="x")
        bottom_frame.pack(side="top", fill="both", expand=True)

        self.label_site = tk.Label(top_frame, text="Target domain (Website URL/IP address)", font=(self.controller.font, self.controller.font_size))
        self.label_site.config(bg='#DADADA', fg='black')
        self.label_site.pack(side='top', pady=5)

        self.domain = IPEntry(top_frame, controller=self)
        self.domain.pack(side='top', pady=5)
        self.domain_site = tk.Entry(top_frame, font=(self.controller.font, self.controller.font_size))

        self.check = tk.Button(bottom_frame, text='Use Website URL instead', command=self.toggle, font=(self.controller.font, self.controller.font_size))
        self.check.config(bg='#DADADA', fg='black', highlightbackground='#DADADA', highlightcolor='#DADADA', highlightthickness=0)
        self.check.pack(side='top', pady=5)

        self.label_victim = tk.Label(bottom_frame, text="Victim IP", font=(self.controller.font, self.controller.font_size))
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.pack(side='top', pady=5)

        self.victim_ip = IPEntry(bottom_frame, controller=self)
        self.victim_ip.pack(side='top', pady=5)

        self.label_target = tk.Label(bottom_frame, text="Target IP",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.pack(side='top', pady=5)

        self.target_ip = IPEntry(bottom_frame, controller=self)
        self.target_ip.pack(side='top', pady=5)

        self.button_start = tk.Button(bottom_frame, text="Start spoofing", command=self.start_dns, width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.pack(side='top', pady=10)

        self.button_stop = tk.Button(bottom_frame, text="Stop spoofing", command=self.stop_dns, width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.pack(side='top')
        self.button_stop.config(state=tk.DISABLED)

    def toggle(self):
        if self.check.config('text')[4] == 'Use Website URL instead':
            self.check.config(text='Use IP address instead')
            self.domain.pack_forget()
            self.domain_site.pack(side='top', pady=5)
        else:
            self.check.config(text='Use Website URL instead')
            self.domain_site.pack_forget()
            self.domain.pack(side='top', pady=5)

    def start_dns(self):
        domain = self.domain.get()
        target = self.target_ip.get()
        victim = self.victim_ip.get()

        if not are_valid_address([target]):
            messagebox.showerror("Error",  "The target IP address is not a valid IPv4 or IPv6 IP address.")

        if not are_valid_address([victim]):
            messagebox.showerror("Error", "The victim IP address is not a valid IPv4 or IPv6 IP address.")

        self.controller.log.update_out('Domain, target, and victim successfully set')

        # TODO: implement in dns_attack.py (?)
        self.controller.log.update_out('Starting DNS spoofing')

        self.controller.log.update_stat("DNS spoofing provided victim's domain with target IP")
        self.controller.log.update_out('DNS spoofing active')

    def stop_dns(self):
        # TODO: implement in dns_attack.py (?)
        self.controller.log.update_out('Stopping DNS spoofing')

        self.controller.log.update_out('DNS spoofing stopped')
        self.controller.log.update_stat("Stopped DNS spoofing")
        return


class IPEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, borderwidth=1, relief="sunken", background="white")
        self.entries = []

        # Doesn't work in a for loop w/ a list / dictionary (?)
        entry_text0 = tk.StringVar()
        entry_text1 = tk.StringVar()
        entry_text2 = tk.StringVar()
        entry_text3 = tk.StringVar()

        vals = [entry_text0, entry_text1, entry_text2, entry_text3]

        entry_text0.trace("w", lambda *args: self.character_limit(entry_text0))
        entry_text1.trace("w", lambda *args: self.character_limit(entry_text1))
        entry_text2.trace("w", lambda *args: self.character_limit(entry_text2))
        entry_text3.trace("w", lambda *args: self.character_limit(entry_text3))

        for i in range(4):
            entry = tk.Entry(self, width=3, borderwidth=0,
                             justify="center",
                             highlightthickness=0, background="white",
                             font=(controller.controller.font, controller.controller.font_size),
                             validate="key", textvariable=vals[i])
            entry.configure(validatecommand=(entry.register(self.validate_number), '%P', '%d'))
            entry.pack(side="left")
            self.entries.append(entry)

            if i < 3:
                dot = tk.Label(self, text=".", background="white")
                dot.pack(side="left")

    @staticmethod
    def character_limit(entry_text):
        if len(entry_text.get()) > 3:
            entry_text.set(entry_text.get()[:3])

    @staticmethod
    def validate_number(in_str, act_typ):
        """
        Checks if input is a number or not

        https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        """
        if act_typ == '1':  # inserting value
            if not in_str.isdigit():
                return False
        return True

    def get(self):
        return ".".join([entry.get() for entry in self.entries])

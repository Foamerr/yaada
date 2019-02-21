import tkinter as tk


class AttackDNSFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the DNS spoofing
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        self.top_frame = tk.Frame(self)
        self.top_frame.configure(bg='#DADADA')

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.configure(bg='#DADADA')

        self.top_frame.pack(side="top", fill="x")
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        self.label_site = tk.Label(self.top_frame, text="Target domain (Website URL/IP address)", font=(self.controller.font, self.controller.font_size))
        self.label_site.config(bg='#DADADA', fg='black')
        self.label_site.pack(side='top', pady=5)

        self.textbox_domain = tk.Entry(self.top_frame, width=20, font=(self.controller.font, self.controller.font_size),
                                       justify='center')
        self.textbox_domain.pack(side='top', pady=5)

        self.label_victim = tk.Label(self.top_frame, text="Victim IP", font=(self.controller.font, self.controller.font_size))
        self.label_victim.config(bg='#DADADA', fg='black')
        self.label_victim.pack(side='top', pady=5)

        self.textbox_victim = tk.Entry(self.top_frame, width=20, font=(self.controller.font, self.controller.font_size), justify='center')
        self.textbox_victim.pack(side='top', pady=5)

        self.label_target = tk.Label(self.top_frame, text="Target IP",
                                     font=(self.controller.font, self.controller.font_size))
        self.label_target.config(bg='#DADADA', fg='black')
        self.label_target.pack(side='top', pady=5)

        self.textbox_target = tk.Entry(self.top_frame, width=20, font=(self.controller.font, self.controller.font_size),
                                       justify='center')
        self.textbox_target.pack(side='top', pady=5)

        self.button_start = tk.Button(self.bottom_frame, text="Start spoofing", command=self.start_dns, width=15,
                                      font=(self.controller.font, self.controller.font_size))
        self.button_start.config(bg='#DADADA', fg='black')
        self.button_start.pack(side='top', pady=10)
        self.button_start.config(state=tk.DISABLED)

        self.button_stop = tk.Button(self.bottom_frame, text="Stop spoofing", command=self.stop_dns, width=15,
                                     font=(self.controller.font, self.controller.font_size))
        self.button_stop.config(bg='#DADADA', fg='black')
        self.button_stop.pack(side='top')
        self.button_stop.config(state=tk.DISABLED)

    def start_dns(self):
        domain = self.textbox_site.get()
        target = self.textbox_target.get()
        victim = self.textbox_victim.get()

        # TODO: check if domain is a website or a valid IP, check if target & victim are valid IP addresses.
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

    # @staticmethod
    # def validate_number(in_str, act_typ):
    #     """
    #     Checks if input is a number or not
    #
    #     https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
    #     """
    #     if act_typ == '1':  # inserting value
    #         if not in_str == '.' or not in_str.isdigit():
    #             return False
    #     return True


# class IPEntry(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent, borderwidth=1, relief="sunken", background="white")
#         self.entries = []
#
#         for i in range(4):
#             entry = tk.Entry(self, width=3, borderwidth=0,
#                              justify="center",
#                              highlightthickness=0, background="white",
#                              font=(parent.controller.font, parent.controller.font_size),
#                              validate="key")
#             entry.configure(validatecommand=(entry.register(self.validate_number), '%P', '%d'))
#             entry.pack(side="left")
#             self.entries.append(entry)
#
#             if i < 3:
#                 dot = tk.Label(self, text=".", background="white")
#                 dot.pack(side="left")
#
#     @staticmethod
#     def validate_number(in_str, act_typ):
#         """
#         Checks if input is a number or not
#
#         https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
#         """
#         if act_typ == '1':  # inserting value
#             if not in_str.isdigit():
#                 return False
#         return True
#
#     def get(self):
#         return ".".join([entry.get() for entry in self.entries])

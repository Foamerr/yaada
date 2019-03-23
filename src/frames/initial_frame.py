import tkinter as tk


class InitialFrame(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialises GUI of the frame used for the initially showed tab
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#DADADA')

        # SET FRAMES #
        top_frame, bottom_frame = tk.Frame(self), tk.Frame(self)
        bottom_frame.configure(bg='#DADADA'), top_frame.configure(bg='#DADADA')
        top_frame.pack(side="top", fill="x"), bottom_frame.pack(side="top", fill="both", expand=True)

        # GUI COMPONENTS #
        about_desc = "YAADA is a tool that provides an easy way to easily execute ARP " \
                     "poisoning and DNS cache poisoning attacks on a selected list of victims " \
                     "with a target. Here, a DNS cache poisoning attack also considers a target domain and fake IP." \
                     "See the documentation on the `Help' tab for a more detailed description of the tool." \
                     "\n\nThe `Home' tab provides a general description of the tool and explains " \
                     "the various tabs. \n\nThe `ARP Poisoning' tab provides a way to " \
                     "execute an ARP poisoning attack on a list of victims and a specified " \
                     "target. \n\nThe `DNS Spoofing' tab provides a way to execute a DNS spoofing " \
                     "attack a target domain with a fake IP to redirect to. This tab will only be enabled after executing an ARP poisoning attack." \
                     "One should perform an ARP poisoning attack on a DNS name server and authoritative server in order to execute DNS cache poisoning afterwards. \n\nThe `Help' tab " \
                     "provides additional ways to get help and other documentation of the " \
                     "tool."

        self.label_welcome = tk.Label(top_frame,
                                      text='YAADA',
                                      font=(self.controller.font, 44))
        self.label_welcome.config(bg='#DADADA', fg='black')
        self.label_welcome.pack(side='top', pady=0)
        self.labelframe_gen_widget = tk.LabelFrame(bottom_frame,
                                                   text="General description",
                                                   font=(self.controller.font, self.controller.font_size, "bold"))
        self.labelframe_gen_widget.config(bg='#DADADA', fg='black')
        self.label_gen_widget = tk.Label(self.labelframe_gen_widget,
                                         text=about_desc,
                                         wraplength=450,
                                         justify=tk.LEFT,
                                         width=53,
                                         font=(self.controller.font, self.controller.font_size))
        self.label_gen_widget.config(bg='#DADADA', fg='black')
        self.labelframe_gen_widget.pack(padx=5, pady=0)
        self.label_gen_widget.pack(padx=10, pady=0)

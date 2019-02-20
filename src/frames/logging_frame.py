import tkinter as tk
from datetime import datetime


class LoggingFrame(tk.Frame):
    stat = '[#] '

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')
        self.pack_propagate(False)
        self.empty_stat = 'The current status will be displayed here'
        self.stat_text = None
        self.stat_msg = None
        self.out_text = 'output («) and input (») will be displayed here'
        self.out_msg = None
        self.out_list = None
        self.font_size = 11

        self.create_stat_bar()
        self.create_out_box()

    def create_out_box(self):
        """
        Creates a box for outputs and inputs
        """
        self.out_msg = tk.Canvas(self)
        self.out_msg.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, expand=tk.TRUE)
        self.out_msg.config(width=600, bg='black')

        scroll = tk.Scrollbar(self.out_msg)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.out_list = tk.Listbox(self.out_msg, bg='black', fg='white', yscrollcommand=scroll.set,
                                   font=(self.controller.font, self.controller.font_size))
        scroll.config(command=self.out_list.yview)
        self.out_list.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.W, expand=tk.TRUE)
        self.out_list.insert(tk.END, self.get_prefix_out().__add__(self.out_text))

    def create_stat_bar(self):
        """
        Creates a status bar
        """
        self.stat_text = self.empty_stat
        self.stat_msg = tk.Message(self, text=self.stat.__add__(self.stat_text), width=600, anchor=tk.W,
                                   font=(self.controller.font, self.controller.font_size))
        self.stat_msg.pack(anchor=tk.W, fill=tk.X, side=tk.BOTTOM)
        self.stat_msg.config(bg='#DADADA', fg='black')

    def update_stat(self, msg, append=False):
        """
        Updates the status by either appending @msg or setting the text as @msg.

        @precondition: @msg.type == str
        """
        if not append:
            self.stat_text = msg
        else:
            self.stat_text += msg
        self.stat_msg.configure(text=self.stat.__add__(self.stat_text))
        self.update()

    # TODO: combine out and in and simply consider 2 cases that have to be passed as parameters
    def update_out(self, msg):
        """
        Updates the output by either appending @msg or setting the text as @msg.
        """
        self.out_list.insert(tk.END, self.get_prefix_out().__add__(msg))
        self.out_list.select_clear(self.out_list.size() - 2)
        self.out_list.select_set(tk.END)
        self.out_list.yview(tk.END)

    def update_in(self, msg):
        """
        Updates the output as input by either appending @message or setting the text as @message.
        """
        self.out_list.insert(tk.END, self.get_prefix_in().__add__(msg))
        self.out_list.select_clear(self.out_list.size() - 2)
        self.out_list.select_set(tk.END)
        self.out_list.yview(tk.END)

    @staticmethod
    def get_prefix_out():
        return ' [« ' + str(datetime.now().time().strftime("%H:%M:%S")) + "] "

    @staticmethod
    def get_prefix_in():
        return ' [» ' + str(datetime.now().time().strftime("%H:%M:%S")) + "] "

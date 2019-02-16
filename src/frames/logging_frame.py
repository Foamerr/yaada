import tkinter as tk
from datetime import datetime


class LoggingFrame(tk.Frame):
    stat = '[#] '

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg='black')
        self.pack_propagate(False)
        self.empty_stat = 'the current status will be displayed here'
        self.stat_text = None
        self.stat_msg = None
        self.out_text = 'output («) and input (») will be displayed here'
        self.out_msg = None
        self.out_list = None

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
        self.out_list = tk.Listbox(self.out_msg, bg='black', fg='white', yscrollcommand=scroll.set)
        scroll.config(command=self.out_list.yview)
        self.out_list.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.W, expand=tk.TRUE)
        self.out_list.insert(tk.END, self.get_prefix_out().__add__(self.out_text))

    def create_stat_bar(self):
        """
        Creates a status bar
        """
        self.stat_text = self.empty_stat
        self.stat_msg = tk.Message(self, text=self.stat.__add__(self.stat_text), width=600, anchor=tk.W)
        self.stat_msg.pack(anchor=tk.W, fill=tk.X, side=tk.BOTTOM)
        self.stat_msg.config(bg='black', fg='white')

    def empty_line(self):
        """
        Outputs an empty line
        """
        self.output_listbox.insert(tk.END, "")

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

    def update_out(self, msg, append=False):
        """
        Updates the output by either appending @msg or setting the text as @msg.

        @precondition: @msg.type == str
        """
        if not append:
            self.output_listbox.delete(0, tk.END)
        self.output_listbox.insert(tk.END, self.get_output_prefix().__add__(tk.re.sub(r'[^a-zA-Z0-9\._-]', ' ', msg)))
        self.update()

    def update_in(self, msg, append=True):
        """
        Updates the output as input by either appending @message or setting the text as @message.

        @precondition: @msg.type == str
        """
        if not append:
            self.output_listbox.delete(0, tk.END)
        self.output_listbox.insert(tk.END, self.get_input_prefix().__add__(tk.re.sub(r'[^a-zA-Z0-9\._-]', ' ', msg)))
        self.update()

    @staticmethod
    def get_prefix_out():
        return ' [« ' + str(datetime.now().time().strftime("%H:%M:%S")) + "] "

    @staticmethod
    def get_prefix_in():
        return ' [» ' + str(datetime.now().time().strftime("%H:%M:%S")) + "] "

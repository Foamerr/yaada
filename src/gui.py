import tkinter as tk
import discovery as dis

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("hackerman")

        self.label = tk.Label(master, text="hackerman interface")
        self.label.pack()

        options = dis.arp_ping()
        tkvar = tk.StringVar(master)
        tkvar.set(options[0])
        option_menu  = tk.OptionMenu(master, tkvar, *options)
        option_menu.pack()

root = tk.Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
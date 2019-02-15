from tkinter import Tk, Label, Button, Menubutton
import tkinter as tk

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("hackerman")

        self.label = Label(master, text="hackerman interface")
        self.label.pack()

        options = self.discover()
        tkvar = tk.StringVar(master)
        tkvar.set(options[0])
        option_menu  = tk.OptionMenu(master, tkvar, *options)
        option_menu.pack()
    
    def discover(self):
        return ['1', '2']

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
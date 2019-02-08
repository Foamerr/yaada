from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("hackerman")

        self.label = Label(master, text="hackerman interface")
        self.label.pack()

        self.greet_button = Button(master, text="hack", command=self.hack)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def hack(self):
        print("ARP Poison ofzo")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
import tkinter as tk

class watergui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.label = tk.Label(root, text="Drink Water!", font=("Arial", 28, "bold"), fg="green")
        self.label.pack()
        





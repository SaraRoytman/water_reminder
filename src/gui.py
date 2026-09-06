import tkinter as tk

class watergui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")

        self.root.attributes('-topmost', True)
        self.label = tk.Label(root, text="Drink Water!", font=("Arial", 28, "bold"), fg="green")
        self.label.pack()

        self.drink_btn = tk.Button(root, text="שתיתי מים!", font=("Arial", 16), command=self.on_drink)
        self.drink_btn.pack(pady=10)

        self.root.withdraw()
        self.root.after(5000, self.show_window)

    def show_window(self):
        self.root.deiconify()

    def on_drink(self):
        self.root.withdraw()
        self.root.after(25000, self.show_window)
        





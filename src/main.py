import tkinter as tk
from gui import watergui

def main():
    root = tk.Tk()
    app = watergui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
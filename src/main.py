import tkinter as tk
from gui import WaterReminderGUI

def main():
    root = tk.Tk()
    app = WaterReminderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
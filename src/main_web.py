import os
from nicegui import ui
from gui import WaterReminderGUI

@ui.page("/")
def main_page():
    WaterReminderGUI()

ui.run(host="0.0.0.0", port=int(os.environ.get("PORT" ,5000)), native=False, reload=False)
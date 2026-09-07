from gui import WaterReminderGUI
from nicegui import ui
import os

WaterReminderGUI()

port = int(os.environ.get("PORT", 8080))
ui.run(host="0.0.0.0", port=port, title="Water Reminder", native=False, reload=False)
import os
from dotenv import load_dotenv
from nicegui import ui
import gui

load_dotenv()

port = int(os.environ.get("PORT", 8080))

ui.run(host="0.0.0.0", port=port, title="Water Reminder", native=False, reload=True)
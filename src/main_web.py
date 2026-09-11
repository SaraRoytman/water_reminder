
import os
from dotenv import load_dotenv
from nicegui import ui
import gui

load_dotenv()

secret = os.getenv('Password')
if not secret:
    raise ValueError("Missing Password! Please check your .env file.")

port = int(os.environ.get("PORT", 8080))

ui.run(host="0.0.0.0", port=port, title="Water Reminder", native=False, reload=False, storage_secret=secret)

from nicegui import ui
import os
from dotenv import load_dotenv
import gui

load_dotenv()
secret = os.getenv('Password')
if not secret:
    raise ValueError("Missing Password! Please check your .env file.")


ui.run(title="Water Reminder", native=True, reload=False, storage_secret=secret)


import os
from datetime import date
from nicegui import ui, app
from mongomock import MongoClient
from dotenv import load_dotenv
from logic import WaterTracker

load_dotenv() 
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["water_app"]
collection = db["daily_logs"]

class user_select_screen:
    def __init__(self, on_select):
        ui.label("who are you? ").classes('text-white text-3xl font-semibold')
        with ui.row().classes('gap-6 mt-4'):
            ui.button("Developer", on_click=lambda: on_select('Developer'), color='teal').classes('font-bold text-xl px-6 py-2')
            ui.button("Guest", on_click=lambda: on_select('Guest'), color='grey').classes('font-bold text-xl px-6 py-2')

class Main_tracker_screen:
    def __init__(self, on_back, on_finish):
        self.on_back = on_back
        self.on_finish = on_finish
        self.current_user = None 
        self.tracker = None
        self.current_date = None

        self.label = ui.label("Drink Water!").classes('text-red-500 text-2xl font-semibold')
        self.total_label = ui.label("").classes('text-white text-md font-mono')

        with ui.row().classes('items-center justify-center gap-4'):
            self.drink_btn = ui.button("500 ml", on_click=lambda: self.on_drink(self.tracker.add_tub0), color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')
            self.drink_btn_250 = ui.button("250 ml", on_click=lambda: self.on_drink(self.tracker.add_tub1), color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')
            self.drink_sip = ui.button("shlook" , on_click=self.show_sip_input, color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')

        with ui.button("Caffeine", color='brown').classes('font-mono font-bold text-lg text-black').props('dense') as self.caffeine_btn:
            with ui.menu():
                ui.menu_item("Coffe", on_click=lambda: self.on_drink(self.tracker.add_caffe))
                ui.menu_item("xl", on_click=lambda: self.on_drink(self.tracker.add_xl))

        with ui.row().classes('items-center gap-2') as self.sip_input_container:
            self.sip_input_container.set_visibility(False)
            self.sip_input = ui.number(value=1, format='%.0f').classes('w-24 bg-white rounded').props('dense')
            ui.button("✓", on_click=self.on_custom_sip, color='green-4').classes('min-w-[40px]')
            ui.button("✗", on_click=self.hide_sip_input, color='red-4').classes('min-w-[40px]')
        
        ui.button("Back", on_click=self.on_back, color='white').classes('absolute right-2 top-1/2 -translate-y-1/2')

    def load_user(self, user_type):
        self.current_user = user_type
        self.current_date = date.today().isoformat()

        record = collection.find_one({"user": self.current_user, "date": self.current_date})
        
        saved_amount = record["amount"] if record else 0

        self.tracker = WaterTracker(init_amount=saved_amount)
        self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")

    def on_drink(self, add_func):
        today_str = date.today().isoformat()
        
        if self.current_date != today_str:
            self.tracker.consumed = 0
            self.current_date = today_str

        add_func()

        collection.update_one(
            {"user": self.current_user, "date": today_str},
            {"$set": {"amount": self.tracker.consumed}},
            upsert=True
        )
        
        self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")
       
        ui.timer(10, self.on_finish, once=True)

    def show_sip_input(self):
        self.drink_sip.set_visibility(False)
        self.sip_input_container.set_visibility(True)

    def hide_sip_input(self):
        self.sip_input_container.set_visibility(False)
        self.drink_sip.set_visibility(True)

    def on_custom_sip(self):
        sips = self.sip_input.value or 0
        if sips > 0:
            self.hide_sip_input()
            amount_ml = sips * 20
            self.on_drink(lambda: self.tracker.add_amount(amount_ml))




    




        
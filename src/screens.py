import os
from datetime import date
from nicegui import ui, run
from pymongo import MongoClient 
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from logic import WaterTracker

load_dotenv() 
MONGO_URI = os.getenv("MONGO_URI")

collection = None
if MONGO_URI:
    try:
        # קיצור זמן ההמתנה ל-3 שניות כדי לא לעכב תהליכים ברקע
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000, connectTimeoutMS=3000)
        db = client["water_app"]
        collection = db["daily_logs"]
    except Exception as e:
        print(f"MongoDB init error: {e}")
else:
    print("WARNING: MONGO_URI was not found in .env file!")


def fetch_user_amount_sync(user: str, current_date: str) -> int:
    """פונקציה שרצה ברקע כדי לא לתקוע את הממשק"""
    if collection is None:
        return 0
    try:
        record = collection.find_one({"user": user, "date": current_date})
        return record.get("amount", 0) if record else 0
    except PyMongoError as e:
        print(f"MongoDB Read Error (Check IP Whitelist / URI): {e}")
        return 0


def update_user_amount_sync(user: str, current_date: str, amount: int):
    """פונקציה שרצה ברקע לשמירת הנתונים"""
    if collection is None:
        return
    try:
        collection.update_one(
            {"user": user, "date": current_date},
            {"$set": {"amount": amount}},
            upsert=True
        )
    except PyMongoError as e:
        print(f"MongoDB Write Error: {e}")


class user_select_screen:
    def __init__(self, on_select):
        ui.label("who are you?").classes('text-white text-3xl font-semibold')
        with ui.row().classes('gap-6 mt-4'):
            ui.button("Developer", on_click=lambda: on_select('Developer'), color='teal').classes('font-bold text-xl px-6 py-2')
            ui.button("Guest", on_click=lambda: on_select('Guest'), color='grey').classes('font-bold text-xl px-6 py-2')


class Main_tracker_screen:
    def __init__(self, on_back, on_finish):
        self.on_back = on_back
        self.on_finish = on_finish
        self.current_user = None 
        self.tracker = WaterTracker(0)
        self.current_date = date.today().isoformat()

        self.label = ui.label("Drink Water!").classes('text-red-500 text-2xl font-semibold')
        self.total_label = ui.label("").classes('text-white text-md font-mono')

        with ui.row().classes('items-center justify-center gap-4'):
            self.drink_btn = ui.button("500 ml", on_click=lambda: self.on_drink(self.tracker.add_tub0), color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')
            self.drink_btn_250 = ui.button("250 ml", on_click=lambda: self.on_drink(self.tracker.add_tub1), color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')
            self.drink_sip = ui.button("shlook", on_click=self.show_sip_input, color='light-blue-4').classes('font-mono font-bold text-lg text-black').props('dense')

        with ui.button("Caffeine", color='brown').classes('font-mono font-bold text-lg text-black').props('dense') as self.caffeine_btn:
            with ui.menu():
                ui.menu_item("Coffee", on_click=lambda: self.on_drink(self.tracker.add_caffe))
                ui.menu_item("XL", on_click=lambda: self.on_drink(self.tracker.add_xl))

        with ui.row().classes('items-center gap-2') as self.sip_input_container:
            self.sip_input_container.set_visibility(False)
            self.sip_input = ui.number(value=1, min=1, format='%.0f').classes('w-24 bg-white rounded').props('dense')
            ui.button("✓", on_click=self.on_custom_sip, color='green-4').classes('min-w-[40px]')
            ui.button("✗", on_click=self.hide_sip_input, color='red-4').classes('min-w-[40px]')
        
        ui.button("Back", on_click=self.on_back, color='white').classes('absolute right-2 top-1/2 -translate-y-1/2 text-black')

    def load_user(self, user_type):
        self.current_user = user_type
        self.current_date = date.today().isoformat()
        
        # מציג מיידית את המסך בלי לחכות למסד הנתונים
        self.tracker = WaterTracker(init_amount=0)
        self.total_label.set_text(f"Loading... ({self.current_user})")
        
        # טעינת הנתונים מ-MongoDB ברקע בלי לתקוע את החלון
        ui.timer(0.01, self._load_user_async, once=True)

    async def _load_user_async(self):
        saved_amount = await run.io_bound(fetch_user_amount_sync, self.current_user, self.current_date)
        self.tracker.consumed = saved_amount
        self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")

    async def on_drink(self, add_func):
        today_str = date.today().isoformat()
        
        if self.current_date != today_str:
            self.tracker.consumed = 0
            self.current_date = today_str

        add_func()
        current_amount = self.tracker.consumed
        self.total_label.set_text(f"{current_amount} ml today ({self.current_user})")
        self.on_finish()

        await run.io_bound(update_user_amount_sync, self.current_user, today_str, current_amount)

    def show_sip_input(self):
        self.drink_sip.set_visibility(False)
        self.sip_input_container.set_visibility(True)

    def hide_sip_input(self):
        self.sip_input_container.set_visibility(False)
        self.drink_sip.set_visibility(True)

    async def on_custom_sip(self):
        sips = self.sip_input.value or 0
        if sips > 0:
            self.hide_sip_input()
            amount_ml = int(sips) * 20
            await self.on_drink(lambda: self.tracker.add_amount(amount_ml))




    




        
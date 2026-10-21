import os
import json
import requests
from datetime import date
from nicegui import ui, run
from dotenv import load_dotenv
from logic import WaterTracker

load_dotenv() 
# הכתובת מ-Firebase Realtime Database (ללא סלאש בסוף)
FIREBASE_URL = (os.getenv("FIREBASE_URL") or "").rstrip("/")
LOCAL_BACKUP_FILE = "local_water_backup.json"


def _read_local(user: str, current_date: str) -> int:
    if os.path.exists(LOCAL_BACKUP_FILE):
        try:
            with open(LOCAL_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(f"{user}_{current_date}", 0)
        except Exception:
            pass
    return 0


def _write_local(user: str, current_date: str, amount: int):
    data = {}
    if os.path.exists(LOCAL_BACKUP_FILE):
        try:
            with open(LOCAL_BACKUP_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    data[f"{user}_{current_date}"] = amount
    try:
        with open(LOCAL_BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def fetch_user_amount_sync(user: str, current_date: str) -> int:
    """מושך את הכמות מ-Firebase דרך HTTPS רגיל (פורט 443 שלא נחסם) או מגיבוי מקומי"""
    if FIREBASE_URL:
        try:
            url = f"{FIREBASE_URL}/daily_logs/{user}/{current_date}.json"
            res = requests.get(url, timeout=3)
            if res.ok and res.json() is not None:
                amount = int(res.json().get("amount", 0))
                _write_local(user, current_date, amount)
                return amount
        except Exception as e:
            print(f"Cloud sync warning: {e}")
    return _read_local(user, current_date)


def add_user_amount_sync(user: str, current_date: str, delta: int) -> int:
    current = fetch_user_amount_sync(user, current_date)
    new_amount = current + delta
    _write_local(user, current_date, new_amount)

    if FIREBASE_URL:
        try:
            url = f"{FIREBASE_URL}/daily_logs/{user}/{current_date}.json"
            requests.put(url, json={"amount": new_amount}, timeout=3)
        except Exception as e:
            print(f"Cloud write warning: {e}")

    return new_amount


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
        self.is_updating = False

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
        
        ui.button("Back", on_click=self.on_back, color='white').classes('absolute right-3 top-1/3 -translate-y-1/2 text-black')

        ui.timer(3.0, self.sync_from_db)

    def load_user(self, user_type):
        self.current_user = user_type
        self.current_date = date.today().isoformat()
        
        self.tracker = WaterTracker(init_amount=0)
        self.total_label.set_text(f"0 ml today ({self.current_user})")
        
        ui.timer(0.01, self.sync_from_db, once=True)

    async def sync_from_db(self):
        if not self.current_user or self.is_updating:
            return
        
        today_str = date.today().isoformat()
        if self.current_date != today_str:
            self.current_date = today_str
            self.tracker.consumed = 0

        saved_amount = await run.io_bound(fetch_user_amount_sync, self.current_user, self.current_date)
        if saved_amount is not None and not self.is_updating:
            self.tracker.consumed = saved_amount
            self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")

    async def on_drink(self, add_func):
        today_str = date.today().isoformat()
        
        if self.current_date != today_str:
            self.tracker.consumed = 0
            self.current_date = today_str

        self.is_updating = True
        try:
            previous_amount = self.tracker.consumed
            add_func()
            delta = self.tracker.consumed - previous_amount

            self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")
            self.on_finish()

            synced_amount = await run.io_bound(
                add_user_amount_sync, 
                self.current_user, 
                today_str, 
                delta
            )
            if synced_amount is not None:
                self.tracker.consumed = synced_amount
                self.total_label.set_text(f"{self.tracker.consumed} ml today ({self.current_user})")
        finally:
            self.is_updating = False

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




    




        
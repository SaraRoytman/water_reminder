
from datetime import date
from nicegui import ui, app
from logic import WaterTracker


app.native.window_args['width'] = 370
app.native.window_args['height'] = 370

@ui.page('/')
def main_page():
    WaterReminderGUI()

class WaterReminderGUI:
    def __init__(self):
        
        

        ui.query('body').classes('bg-stone-700 overflow-hidden')

        today_str = date.today().isoformat() 
        saved_date = app.storage.user.get('last_date', today_str)

        if saved_date != today_str:
            app.storage.user['water_consumed'] = 0
            app.storage.user['last_date'] = today_str
            saved_amount = 0
        else:
            saved_amount = app.storage.user.get('water_consumed', 0)
        
        self.tracker = WaterTracker(init_amount=saved_amount)
        
        with ui.column().classes('w-full h-screen items-center justify-center gap-6'):
            self.label = ui.label("Drink Water!").classes('text-red-500 text-2xl font-semibold')
            self.total_label = ui.label(f"{self.tracker.consumed} ml today").classes('text-white text-md font-mono')
            
            self.drink_btn = ui.button("500 מ״ל", on_click=lambda: self.on_drink(self.tracker.add_tub0), color='light-blue-4').classes('font-mono font-bold text-lg text-black')
            self.drink_btn_250 = ui.button("250 מ״ל", on_click=lambda: self.on_drink(self.tracker.add_tub1), color='light-blue-4').classes('font-mono font-bold text-lg text-black')
            self.drink_sip = ui.button("שלוק" , on_click=self.show_sip_input, color='light-blue-4').classes('font-mono font-bold text-lg text-black')

            with ui.row().classes('items-center gap-2') as self.sip_input_container:
                self.sip_input_container.set_visibility(False)
                self.sip_input = ui.number(value=1, format='%.0f').classes('w-24 bg-white rounded').props('dense')
                ui.button("✓", on_click=self.on_custom_sip, color='green-4').classes('min-w-[40px]')
                ui.button("✗", on_click=self.hide_sip_input, color='red-4').classes('min-w-[40px]')

            self.tmp_btn = ui.button(on_click=self.hide_window, color='white').classes('absolute right-2 top-1/2 -translate-y-1/2')
            
        ui.timer(360, self.show_window)

    def hide_window(self):
        if app.native.main_window:
            app.native.main_window.hide()
        else:
            self.label.set_visibility(False)
            self.drink_btn.set_visibility(False)
            self.drink_btn_250.set_visibility(False)
            self.drink_sip.set_visibility(False)
            self.sip_input_container.set_visibility(False)
        
    def show_window(self):
        if app.native.main_window:
            app.native.main_window.show()
        else:
            self.label.set_visibility(True)
            self.drink_btn.set_visibility(True)
            self.drink_btn_250.set_visibility(True) 
            self.drink_sip.set_visibility(True) 
            self.sip_input_container.set_visibility(False)

    def on_drink(self, add_func):
        today_str = date.today().isoformat()
        if app.storage.user.get('last_date') != today_str:
            self.tracker.consumed = 0
            app.storage.user['last_date'] = today_str

        add_func()
        
        app.storage.user['water_consumed'] = self.tracker.consumed
        
        self.total_label.set_text(f"{self.tracker.consumed} ml today")
        
        ui.timer(10, self.hide_window, once=True)

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








        





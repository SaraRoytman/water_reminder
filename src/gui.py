
from nicegui import ui, app
from logic import WaterTracker

class WaterReminderGUI:
    def __init__(self):
        
        app.native.window_args['width'] = 350
        app.native.window_args['height'] = 350

        ui.query('body').classes('bg-stone-700 overflow-hidden')

        self.tracker = WaterTracker()
        
        with ui.column().classes('w-full h-screen items-center justify-center gap-6'):
            self.label = ui.label("Drink Water!").classes('text-red-500 text-2xl font-semibold')
            self.total_label = ui.label(f"{self.tracker.consumed} ml today").classes('text-white text-md font-mono')
            
            self.drink_btn = ui.button("500 מ״ל", on_click=lambda: self.on_drink(self.tracker.add_tub0), color='light-blue-4').classes('font-mono font-bold text-lg text-black')
            self.drink_btn_250 = ui.button("250 מ״ל", on_click=lambda: self.on_drink(self.tracker.add_tub1), color='light-blue-4').classes('font-mono font-bold text-lg text-black')
            self.tmp_btn = ui.button(on_click=self.hide_window, color='white').classes('absolute right-2 top-1/2 -translate-y-1/2')

            
        ui.timer(120, self.show_window, once=True)

    def hide_window(self):
        if app.native.main_window:
            app.native.main_window.hide()
        else:
            self.label.set_visibility(False)
            self.drink_btn.set_visibility(False)
        
    def show_window(self):
        if app.native.main_window:
            app.native.main_window.show()
        else:
            self.label.set_visibility(True)
            self.drink_btn.set_visibility(True)   

    def on_drink(self, add_func):

        add_func()
        self.total_label.set_text(f"{self.tracker.consumed} ml today")
        
        ui.timer(10, self.hide_window, once=True)
        ui.timer(360, self.show_window, once=True)






        





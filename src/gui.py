
from nicegui import ui, app

class WaterReminderGUI:
    def __init__(self):
        
        app.native.window_args['width'] = 350
        app.native.window_args['height'] = 350

        ui.query('body').classes('bg-stone-700 overflow-hidden')
        
        with ui.column().classes('w-full h-screen items-center justify-center gap-6'):
            self.label = ui.label("Drink Water!").classes('text-red-500 text-2xl font-semibold')
            self.drink_btn = ui.button("!שתיתי כבר", on_click=self.on_drink, color='light-blue-4').classes('font-mono font-bold text-lg text-black')


            
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

    def on_drink(self):
        self.hide_window()
        ui.timer(360, self.show_window, once=True)






        





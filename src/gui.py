
from nicegui import ui, app

class WaterReminderGUI:
    def __init__(self):
        # הגדרת גודל החלון במצב native (רוחב, גובה)
        app.native.window_args['width'] = 500
        app.native.window_args['height'] = 400

        ui.query('body').style('background-color: oklch(80.8% 0.114 19.571);')
        
        with ui.column().classes('w-full h-screen items-center justify-center gap-6'):
            self.label = ui.label("Drink Water!").style(
                "color: #1e3a8a; font-size: 32px; font-weight: bold;"
            )
            self.drink_btn = ui.button("!שתיתי כבר", on_click=self.on_drink).classes(
                'px-6 py-3 text-lg bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700'
            )
            
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






        





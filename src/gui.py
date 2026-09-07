from nicegui import ui, app


class WaterReminderGUI:
    def __init__(self):
        self.label = ui.label("Drink Water!").style(
            "color: blue; font-size: 28px; font-weight: bold;"
        )
        self.drink_btn = ui.button("שתיתי מים!", on_click=self.on_drink).style(
            "font-size: 16px;"
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
        





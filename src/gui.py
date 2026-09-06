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
        app.native.main_window.hide()

    def show_window(self):
        app.native.main_window.show()

    def on_drink(self):
        self.hide_window()
        ui.timer(60, self.show_window, once=True)
        






from nicegui import ui, app
from screens import user_select_screen, Main_tracker_screen

app.native.window_args['width'] = 470
app.native.window_args['height'] = 470

@ui.page('/')
def main_page():
    WaterReminderGUI()

class WaterReminderGUI:
    def __init__(self): 

        ui.query('body').classes('bg-stone-700 overflow-hidden')

        self.selection_container = ui.column().classes('w-full h-screen items-center justify-center gap-6')
        self.tracker_container = ui.column().classes('w-full h-screen items-center justify-center gap-6')

        self.tracker_container.set_visibility(False)

        with self.selection_container:
            self.selection_screen = user_select_screen(on_select=self.on_user_selected)

        with self.tracker_container:
            self.tracker_screen = Main_tracker_screen(on_back=self.show_selection_screen, on_finish=self.hide_window)

        if app.native.main_window:
            self.selection_container.set_visibility(False)
            self.tracker_screen.load_user('Developer')
            self.tracker_container.set_visibility(True)
        else:
            self.tracker_container.set_visibility(False)
            self.selection_container.set_visibility(True)

        ui.timer(360, self.show_window)

    def on_user_selected(self, user_type):
        self.selection_container.set_visibility(False)
        self.tracker_screen.load_user(user_type)
        self.tracker_container.set_visibility(True)
        
    def show_selection_screen(self):
        self.tracker_container.set_visibility(False)
        self.selection_container.set_visibility(True)

    def hide_window(self):
        self.show_selection_screen()
        if app.native.main_window:
           app.native.main_window.hide()
        else:
            self.selection_container.set_visibility(False)
            self.tracker_container.set_visibility(False)
        
    def show_window(self):
        if app.native.main_window:
            app.native.main_window.show()
        else:
            self.selection_container.set_visibility(True)
            self.tracker_container.set_visibility(False)
            










        






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

        self.selection_box = ui.column().classes('w-full h-screen items-center justify-center gap-6')
        self.tracker_box = ui.column().classes('w-full h-screen items-center justify-center gap-6')

        self.tracker_box.set_visibility(False)

        with self.selection_box:
            self.selection_screen = user_select_screen(on_select=self.on_user_selected)

        with self.tracker_box:
            self.tracker_screen = Main_tracker_screen(on_back=self.show_selection_screen, on_finish=self.hide_window)

        if app.native.main_window:
            self.selection_box.set_visibility(False)
            self.tracker_screen.load_user('Developer')
            self.tracker_box.set_visibility(True)
        else:
            self.tracker_box.set_visibility(False)
            self.selection_box.set_visibility(True)

        ui.timer(360, self.show_window)

    def on_user_selected(self, user_type):
        self.selection_box.set_visibility(False)
        self.tracker_screen.load_user(user_type)
        self.tracker_box.set_visibility(True)
        
    def show_selection_screen(self):
        if not app.native.main_window:
            self.tracker_box.set_visibility(False)
            self.selection_box.set_visibility(True)       

    def hide_window(self):
        if app.native.main_window:
            app.native.main_window.hide()
        else:
            self.show_selection_screen()
            self.selection_box.set_visibility(False)
            self.tracker_box.set_visibility(False)
        
    def show_window(self):
        if app.native.main_window:
            app.native.main_window.show()
            ui.timer(10, self.hide_window, once=True)
        else:
            self.selection_box.set_visibility(True)
            self.tracker_box.set_visibility(False)
            










        





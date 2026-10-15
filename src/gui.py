
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
        self.hide_timer = None

        self.selection_box = ui.column().classes('w-full h-screen items-center justify-center gap-6')
        self.tracker_box = ui.column().classes('w-full h-screen items-center justify-center gap-6')

        self.tracker_box.set_visibility(False)

        with self.selection_box:
            self.selection_screen = user_select_screen(on_select=self.on_user_selected)

        with self.tracker_box:
            self.tracker_screen = Main_tracker_screen(
                on_back=self.show_selection_screen, 
                on_finish=self.schedule_hide
            )

        if app.native.main_window:
            self.selection_box.set_visibility(False)
            self.tracker_screen.load_user('Developer')
            self.tracker_box.set_visibility(True)
        else:
            self.tracker_box.set_visibility(False)
            self.selection_box.set_visibility(True)

       
        ui.timer(360, self.show_window, immediate=False)

    def cancel_hide_timer(self):
        if self.hide_timer:
            self.hide_timer.cancel()
            self.hide_timer = None

    def schedule_hide(self, delay=10):
        self.cancel_hide_timer()
        self.hide_timer = ui.timer(delay, self.hide_window, once=True)

    def on_user_selected(self, user_type):
        self.cancel_hide_timer()
        self.selection_box.set_visibility(False)
        self.tracker_screen.load_user(user_type)
        self.tracker_box.set_visibility(True)
        
    def show_selection_screen(self):
        self.cancel_hide_timer()
        self.tracker_box.set_visibility(False)
        self.selection_box.set_visibility(True)       

    def hide_window(self):
        self.cancel_hide_timer()
        if app.native.main_window:
            app.native.main_window.hide()
        else:
            self.show_selection_screen()
        
    def show_window(self):
        if app.native.main_window:
            ui.timer(0.01, self.tracker_screen.sync_from_db, once=True)
            app.native.main_window.show()
            self.schedule_hide(10)
        else:
            self.selection_box.set_visibility(True)
            self.tracker_box.set_visibility(False)
            










        





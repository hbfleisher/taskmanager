from kivy.app import App
from ui.pages import LandingPage


class TaskApp(App):
    def build(self):
        self.title = "Task Manager"
        self.icon = "icon.png"
        return LandingPage()
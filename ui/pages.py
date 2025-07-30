from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

Builder.load_file("ui/templates/landing.kv")

class LandingPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.size_hint_y = None
        self.height = '100dp'
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex("#1E1E1E"))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(text="Welcome to TaskManager", font_size='32sp', color=get_color_from_hex("#FFFFFF"))
        subtitle = Label(text="Organize your tasks efficiently", font_size='20sp', color=get_color_from_hex("#AAAAAA"))
        
        btn_start = Button(text="Get Started", size_hint=(None, None), size=('200dp', '50dp'), background_color=get_color_from_hex("#4CAF50"), color=get_color_from_hex("#FFFFFF"))
        btn_start.bind(on_release=self.on_start)

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(btn_start)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_start(self, instance):
        print("Start button pressed")
        # Logic to transition to the main application page
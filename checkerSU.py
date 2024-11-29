import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle  # Добавлен импорт Color

class RootCheckApp(App):
    def build(self):
        # Основной layout
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=20, size_hint=(1, 1))

        # Размещение кнопки по центру и в нижней части с увеличением размера
        self.button_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), size=(600, 150))
        self.button_layout.add_widget(Button(
            text="Check SuperUser",
            font_size=72,  # Увеличенный размер шрифта
            size_hint=(1, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        ))
        self.layout.add_widget(self.button_layout)

        # Центрируем кнопку по X
        self.button_layout.pos_hint = {"center_x": 0.5}

        # Обновляем фон
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Белый цвет (RGBA)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        # Обновляем размер прямоугольника при изменении размера layout
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Привязываем действие к кнопке
        self.check_button = self.button_layout.children[0]  # Достаем кнопку из layout
        self.check_button.bind(on_press=self.check_root_access)

        return self.layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def check_root_access(self, instance):
        try:
            with os.popen("su -c 'echo Root access granted'") as process:
                output = process.read().strip()
            if "Root access granted" in output:
                self.show_popup("Root Access Found", "Your device has root access.", (0, 1, 0, 1))
            else:
                self.show_popup("Root Access Not Found", "Your device does not have root access.", (1, 0, 0, 1))
        except Exception:
            self.show_popup("Error", "An error occurred while checking for root access.", (1, 0, 0, 1))

    def show_popup(self, title, message, text_color):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_label = Label(text=message, font_size=36, color=text_color)  # Увеличенный размер шрифта
        popup_layout.add_widget(popup_label)

        # Создаем popup без фона заданного цвета
        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.5))
        popup.open()

if __name__ == "__main__":
    RootCheckApp().run()
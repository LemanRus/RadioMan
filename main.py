import os

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton

import screens


class RadioMan(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.android_back_click)
        Window.softinput_mode = 'below_target'
        self.theme_cls.primary_palette = "DeepPurple"
        kv = os.listdir("kv")
        for kv_file in kv:
            if kv_file != "misc.kv":
                Builder.load_file(f"kv/{kv_file}")
        return Builder.load_file("kv/main.kv")

    def android_back_click(self, window, key, *args):
        pass


RadioMan().run()

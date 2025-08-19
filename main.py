import os

from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

screens = {
    "Маркировки": [
        "resistors_markings_select_screen",
        "th_resistors_marking_screen",
        "smd_resistors_marking_screen",
        "capacitors_marking_select_screen",
        "th_capacitors_marking_screen",
        "smd_capacitors_marking_screen",
    ],
    "Расчёты": [
        "converter_calculation_screen",
        "led_resistor_calculation_screen",
        "inductor_calculation_select_screen",
        "parallel_resistor_calculation_screen",
        "serial_capacitor_calculate_screen",
        "voltage_divider_calculate_select_screen",
        "lm_regulator_calculate_select_screen",
    ],
    "Справочник": [
        "theory_screen",
        "schematics_screen",
        "pinout_screen",
        "connections_screen",
        "chips_screen",
        "chips_analogs_select_screen",
        "chips_analogs_screen",
        "lifehacks_screen",
    ],
    "Помощь": [
        "how_to_screen",
        "about_screen",
    ]
}

backs = {}
for parent, children in screens.items():
    for child in children:
        if parent in screens and child not in screens:
            backs[child] = parent


class RadioMan(MDApp):
    def build(self):
        self.window = Window
        Window.bind(on_keyboard=self.android_back_click)
        Window.softinput_mode = 'below_target'
        self.theme_cls.primary_palette = "Lavender"

        kv_files = []
        for path, subdirs, files in os.walk('kv'):
            for name in files:
                kv_files.append(os.path.join(path, name))
        for file_path in kv_files:
            Builder.load_file(file_path)
        return Builder.load_file("kv/main.kv")

    def on_switch_tabs(
            self,
            bar: MDNavigationBar,
            item: MDNavigationItem,
            item_icon: str,
            item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def back_to_screen(self):
        self.root.ids.screen_manager.transition = SlideTransition(direction='right')
        current_screen = self.root.ids.screen_manager.current
        if current_screen in backs:
            self.root.ids.screen_manager.current = backs[current_screen]
        else:
            # Например, закрыть приложение или вернуться к главному экрану
            pass
        self.root.ids.screen_manager.transition = SlideTransition(direction='left')

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.back_to_screen()
        return True


RadioMan().run()

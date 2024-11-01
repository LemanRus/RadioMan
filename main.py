import os

from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

backs = {
    "resistors_markings_select_screen": "Маркировки",
    "th_resistors_marking_screen": "resistors_markings_select_screen",
    "smd_resistors_marking_screen": "resistors_markings_select_screen",
    "capacitors_marking_select_screen": "Маркировки",
    "th_capacitors_marking_screen": "capacitors_marking_select_screen",
    "smd_capacitors_marking_screen": "capacitors_marking_select_screen",
    "converter_calculation_screen": "Расчёты",
    "led_resistor_calculation_screen": "Расчёты",
    "inductor_calculation_select_screen": "Расчёты",
    "inductor_calculate_induction_screen":
    "inductor_calculation_select_screen",
    "inductor_calculate_size_screen": "inductor_calculation_select_screen",
    "parallel_resistor_calculation_screen": "Расчёты",
    "serial_capacitor_calculate_screen": "Расчёты",
    "voltage_divider_calculate_select_screen": "Расчёты",
    "voltage_divider_calculate_voltage_screen":
    "voltage_divider_calculate_select_screen",
    "voltage_divider_calculate_resistance_screen":
    "voltage_divider_calculate_select_screen",
    "lm_regulator_calculate_select_screen": "Расчёты",
    "lm_regulator_voltage_screen": "lm_regulator_calculate_select_screen",
    "lm_regulator_current_screen": "lm_regulator_calculate_select_screen",
    "theory_screen": "Справочник",
    "schematics_screen": "Справочник",
    "pinout_screen": "Справочник",
    "connections_screen": "Справочник",
    "chips_screen": "Справочник",
    "chips_analogs_select_screen": "chips_screen",
    "chips_analogs_screen": "chips_analogs_select_screen",
    "lifehacks_screen": "Справочник",
    "how_to_screen": "Помощь",
    "about_screen": "Помощь",
}


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
        self.root.ids.screen_manager.transition = SlideTransition(
            direction='right'
        )
        if self.root.ids.screen_manager.current in backs:
            self.root.ids.screen_manager.current = backs[
                self.root.ids.screen_manager.current
            ]
        self.root.ids.screen_manager.transition = SlideTransition(
            direction='left'
        )

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.back_to_screen()
        return True


RadioMan().run()

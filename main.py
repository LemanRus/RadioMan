import os

from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

import screens

backs = {"resistors_markings_select_screen": "markings_screen",
         "th_resistors_marking_screen": "resistors_markings_select_screen",
         "smd_resistors_marking_screen": "resistors_markings_select_screen",
         "capacitors_marking_select_screen": "markings_screen",
         "th_capacitors_marking_screen": "capacitors_marking_select_screen",
         "smd_capacitors_marking_screen": "capacitors_marking_select_screen",
         "led_resistor_calculation_screen": "calculations_screen",
         "inductor_calculation_select_screen": "calculations_screen",
         "inductor_calculate_induction_screen": "inductor_calculation_select_screen",
         "inductor_calculate_size_screen": "inductor_calculation_select_screen",
         "parallel_resistor_calculation_screen": "calculations_screen",
         "serial_capacitor_calculate_screen": "calculations_screen",
         "voltage_divider_calculate_select_screen": "calculations_screen",
         "voltage_divider_calculate_voltage_screen": "voltage_divider_calculate_select_screen",
         "voltage_divider_calculate_resistance_screen": "voltage_divider_calculate_select_screen",
         "lm_regulator_calculate_select_screen": "calculations_screen",
         "lm_regulator_voltage_screen": "lm_regulator_calculate_select_screen",
         "lm_regulator_current_screen": "lm_regulator_calculate_select_screen",
         "theory_screen": "handbook_screen",
         "schematics_screen": "handbook_screen",
         "pinout_screen": "handbook_screen",
         "connections_screen": "handbook_screen",
         "chips_screen": "handbook_screen",
         "lifehacks_screen": "handbook_screen",
         "how_to_screen": "help_screen",
         "about_screen": "help_screen",
         }


class RadioMan(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.android_back_click)
        Window.softinput_mode = 'below_target'
        self.theme_cls.primary_palette = "DeepPurple"
        Builder.load_file("kv/toplevel_screens.kv")
        Builder.load_file("kv/markings_screens.kv")
        Builder.load_file("kv/calculations_screens.kv")
        Builder.load_file("kv/help_screens.kv")
        Builder.load_file("kv/handbook_screens.kv")
        return Builder.load_file("kv/main.kv")

    def back_to_screen(self):
        try:
            markings_tab_sm = self.root.children[1].children[0].children[0]
        except IndexError:
            pass
        else:
            if markings_tab_sm.current in backs:
                markings_tab_sm.current = backs[markings_tab_sm.current]

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.back_to_screen()
        return True


RadioMan().run()

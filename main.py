import os
import asyncio

from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

import misc
import screens

backs = {"resistors_markings_select_screen": "Маркировки",
         "th_resistors_marking_screen": "resistors_markings_select_screen",
         "smd_resistors_marking_screen": "resistors_markings_select_screen",
         "capacitors_marking_select_screen": "Маркировки",
         "th_capacitors_marking_screen": "capacitors_marking_select_screen",
         "smd_capacitors_marking_screen": "capacitors_marking_select_screen",
         "converter_calculation_screen": "Расчёты",
         "led_resistor_calculation_screen": "Расчёты",
         "inductor_calculation_select_screen": "Расчёты",
         "inductor_calculate_induction_screen": "inductor_calculation_select_screen",
         "inductor_calculate_size_screen": "inductor_calculation_select_screen",
         "parallel_resistor_calculation_screen": "Расчёты",
         "serial_capacitor_calculate_screen": "Расчёты",
         "voltage_divider_calculate_select_screen": "Расчёты",
         "voltage_divider_calculate_voltage_screen": "voltage_divider_calculate_select_screen",
         "voltage_divider_calculate_resistance_screen": "voltage_divider_calculate_select_screen",
         "lm_regulator_calculate_select_screen": "Расчёты",
         "lm_regulator_voltage_screen": "lm_regulator_calculate_select_screen",
         "lm_regulator_current_screen": "lm_regulator_calculate_select_screen",
         "theory_screen": "Справочник",
         "schematics_screen": "Справочник",
         "pinout_screen": "Справочник",
         "connections_screen": "Справочник",
         "chips_screen": "Справочник",
         "lifehacks_screen": "Справочник",
         "how_to_screen": "Помощь",
         "about_screen": "Помощь",
         }

var = ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue',
       'Blueviolet', 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral', 'Cornflowerblue',
       'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan', 'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen',
       'Darkkhaki', 'Darkmagenta', 'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon',
       'Darkseagreen', 'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet', 'Deeppink',
       'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick', 'Floralwhite', 'Forestgreen', 'Fuchsia',
       'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink',
       'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen', 'Lemonchiffon', 'Lightblue',
       'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow', 'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink',
       'Lightsalmon', 'Lightseagreen', 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue',
       'Lightyellow', 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue',
       'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen', 'Mediumturquoise',
       'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose', 'Moccasin', 'Navajowhite', 'Navy', 'Oldlace',
       'Olive', 'Olivedrab', 'Orange', 'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise',
       'Palevioletred', 'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown',
       'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue',
       'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato',
       'Turquoise', 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']

class RadioMan(MDApp):
    def build(self):
        Window.bind(on_keyboard=self.android_back_click)
        Window.softinput_mode = 'below_target'
        self.theme_cls.primary_palette = "Plum"

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
        if self.root.ids.screen_manager.current in backs:
            self.root.ids.screen_manager.current = backs[self.root.ids.screen_manager.current]
        self.root.ids.screen_manager.transition = SlideTransition(direction='left')

    def android_back_click(self, window, key, *args):
        if key == 27:
            self.back_to_screen()
        return True


RadioMan().run()

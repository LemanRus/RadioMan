# -*- coding: utf-8 -*-
"""Экраны маркировок резисторов"""

import weakref

from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivymd.uix.button import MDButtonIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from screens.widgets import ResistorBand
from data_loader import load_resistor_markings, load_smd_resistor_markings


class MarkingsScreen(MDScreen):
    pass


class ResistorsMarkingsSelectScreen(MDScreen):
    pass


class THResistorsMarkingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        resistor_data = load_resistor_markings()
        self.nominal = resistor_data['nominal']
        self.multiplier = resistor_data['multiplier']
        self.tolerance = resistor_data['tolerance']
        self.thermal = resistor_data['thermal']

    def build_menu(self, *args, **kwargs):
        self.menu_items = [{"text": "3",
                            "on_release": lambda x="3": self.set_item(x),
                            },
                           {"text": "4",
                            "on_release": lambda x="4": self.set_item(x),
                            },
                           {"text": "5",
                            "on_release": lambda x="5": self.set_item(x),
                            },
                           {"text": "6",
                            "on_release": lambda x="6": self.set_item(x),
                            }, ]
        self.menu = MDDropdownMenu(
            caller=self.ids.bands_select_menu,
            items=self.menu_items,
            width=dp(101),
        )

    def set_item(self, text_item):
        self.ids.bands_select_menu.text = text_item
        self.menu.dismiss()
        self.build_bands(self.ids.bands_select_menu.text)

    def build_bands(self, value):
        self.bands_qty = int(value)
        self.ids.bands.clear_widgets()
        self.ids.bands.ids.clear()
        self.ids.bands.spacing = sp(
            (Window.width * 3 / 5) / (self.bands_qty * 5)
        )
        self.ids.result.text = "Результат:"
        for i in range(0, self.bands_qty):
            band = ResistorBand(
                MDButtonIcon(
                    icon='chevron-down',
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    theme_icon_color="Custom"
                ),
                band_no=i,
                band_qty=self.bands_qty,
            )
            self.ids.bands.add_widget(band)
            self.ids.bands.ids["band" + str(i)] = weakref.ref(band)
        self.calculate_resistor()

    def calculate_resistor(self):
        thermal = ""
        tolerance = ""

        if "band5" in self.ids.bands.ids.keys():
            thermal = self.thermal[self.ids.bands.ids.band5.color_name]
        if "band4" in self.ids.bands.ids.keys():
            tolerance = self.tolerance[self.ids.bands.ids.band4.color_name]
        if len(self.ids.bands.ids.keys()) in (3, 4):
            multiplier = self.multiplier[self.ids.bands.ids.band2.color_name]
            resistance = (
                self.nominal[self.ids.bands.ids.band0.color_name] * 10 +
                self.nominal[self.ids.bands.ids.band1.color_name]
                ) * multiplier

            if "band3" in self.ids.bands.ids.keys():
                tolerance = self.tolerance[self.ids.bands.ids.band3.color_name]
            else:
                tolerance = "±20%"
        else:
            multiplier = self.multiplier[self.ids.bands.ids.band3.color_name]
            resistance = (
                self.nominal[self.ids.bands.ids.band0.color_name] * 100 +
                self.nominal[self.ids.bands.ids.band1.color_name] * 10 +
                self.nominal[self.ids.bands.ids.band2.color_name]
                ) * multiplier

        if resistance < 1000:
            self.ids.result.text = "Результат: {:g} Ом {}{}".format(
                resistance, tolerance, (", ТКС: " + thermal) if thermal else ""
                )
        elif resistance < 1000000:
            self.ids.result.text = "Результат: {:g} кОм {}{}".format(
                resistance / 1000, tolerance, (", ТКС: " + thermal)
                if thermal else ""
                )
        else:
            self.ids.result.text = "Результат: {:g} МОм {}{}".format(
                resistance / 1000000, tolerance, (", ТКС: " + thermal)
                if thermal else "")


class SMDResistorsMarkingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        smd_data = load_smd_resistor_markings()
        self.eia96 = smd_data['eia96']
        self.eia96_multiplier = smd_data['eia96_multiplier']

    def calculate_resistor(self, marking):
        try:
            self.ids.smd_result.text = ""
            resistance = ""
            precision = False
            marking = marking.lower()
            if marking in ["0", "00", "000", "0000"]:
                resistance = 0
            elif "r" in marking:
                if len(marking) in (3, 4):
                    markings = marking.split("r")
                    resistance = float("{}.{}".format(
                        markings[0], markings[1]
                        ))
                    if len(marking) == 4:
                        precision = True
                else:
                    self.ids.smd_result.text = "Неверный ввод"
            elif len(marking) == 3:
                if marking[2].isalpha() and marking[2].lower() \
                        in self.eia96_multiplier.keys():
                    multiplier = self.eia96_multiplier[marking[2]]
                    resistance = self.eia96[marking[:2]] * multiplier
                    precision = True
                else:
                    resistance = float(marking[:2]) * 10 ** (float(marking[2]))
            elif len(marking) == 4:
                resistance = float(marking[:3]) * 10 ** (float(marking[3]))
                precision = True
            else:
                self.ids.smd_result.text = "Неверный ввод"

            if resistance != "":
                try:
                    resistance = float(resistance)
                    self.ids.smd_result.text = "Результат: "
                    if resistance == 0:
                        self.ids.smd_result.text += "0 Ом (перемычка)"
                    elif resistance < 1000:
                        self.ids.smd_result.text += "{:g} Ом".format(
                            resistance
                            )
                    elif resistance < 1000000:
                        self.ids.smd_result.text += "{:g} кОм".format(
                            resistance / 1000
                            )
                    else:
                        self.ids.smd_result.text += "{:g} МОм".format(
                            resistance / 1000000
                            )
                    if precision and resistance != 0:
                        self.ids.smd_result.text += " ±1%"
                    elif resistance != 0:
                        self.ids.smd_result.text += " ±5%"
                except ValueError:
                    return "Неверный ввод"
        except ValueError:
            self.ids.smd_result.text = "Неверный ввод"

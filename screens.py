import itertools
import math
import weakref
import webbrowser

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import SmoothRoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import BoundedNumericProperty, ObjectProperty, StringProperty, NumericProperty, \
    VariableListProperty
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText, BaseButton, MDButtonIcon
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField

from e24_nominals import E24Nominals as e24
from misc import MDGridScreen
from output_value_methods import format_output_resistor, format_output_capacitor


class MarkingsScreenManager(MDScreenManager):
    pass


class MarkingsScreen(MDScreen):
    pass


class ResistorsMarkingsSelectScreen(MDScreen):
    pass


class ResistorBandDropdownMennu(MDDropdownMenu):
    def open(self) -> None:
        """Animate the opening of a menu window."""

        self.set_menu_properties()
        Window.add_widget(self)
        self.position = self.adjust_position()

        self.width = dp(130)

        self.height = Window.height / 2
        self._tar_x, self._tar_y = self.get_target_pos()
        self.x = self._tar_x
        self.y = self._tar_y - self.target_height
        self.scale_value_center = self.caller.center
        self.set_menu_pos()
        self.on_open()


class ResistorBand(MDButton):
    colors = {
        "Золотой": [1, 0.84, 0, 1], "Серебристый": [0.8, 0.8, 0.8, 1], "Чёрный": [0, 0, 0, 1],
        "Коричневый": [0.4, 0.22, 0, 1], "Красный": [1, 0, 0, 1], "Оранжевый": [0.98, 0.45, 0.02, 1],
        "Жёлтый": [1, 1, 0, 1], "Зелёный": [0.05, 0.64, 0.05, 1], "Синий": [0.05, 0.54, 0.95, 1],
        "Фиолетовый": [0.54, 0.14, 0.59, 1], "Серый": [0.5, 0.5, 0.5, 1], "Белый": [1, 1, 1, 1]
    }
    bands_accordance = {
        3: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
        },
        4: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
        }, 5: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 2, None)),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            4: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
        }, 6: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 2, None)),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            4: dict(itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            5: dict(itertools.islice(colors.items(), 0, 2)) | dict(itertools.islice(colors.items(), 3, 7)) |
               dict(itertools.islice(colors.items(), 8, 10)) | dict(itertools.islice(colors.items(), 11, 12))
        }
    }

    def __init__(self, *args, **kwargs):
        self.app = App.get_running_app()
        self.band_no = kwargs.pop("band_no")
        self.band_qty = kwargs.pop("band_qty")
        super().__init__(*args, **kwargs)
        self.menu = ResistorBandDropdownMennu(
            caller=self,
            items=self.get_band(self.band_no, self.band_qty),
            position="center",
            border_margin=dp(12),
        )
        self.theme_bg_color = self.theme_text_color = self.theme_width = self.theme_height = "Custom"
        self.menu.width = self.menu.minimum_width
        self.my_color = self.bands_accordance[self.band_qty][self.band_no]
        self.md_bg_color = list(self.my_color.values())[0]
        self.theme_width = self.theme_font_size = "Custom"
        self.size_hint = (1, 1)
        self.pos_hint = {"center_y": 0.5}
        self.radius = [1, ]
        self.color_name = list(self.my_color.keys())[0]
        if self.color_name in ["Чёрный", "Коричневый"]:
            self.children[0].icon_color = self.text_color = "white"
        else:
            self.children[0].icon_color = self.text_color = "black"
        self.bind(on_release=self.menu_open)
        self.menu.bind(on_dismiss=lambda _: self.__setattr__("icon", "chevron-down"))

    def get_band(self, band_no, band_qty):
        band = []
        for k, v in self.bands_accordance[band_qty][band_no].items():
            temp = {"text": k}
            temp.update({"md_bg_color": v})
            temp.update({"on_release": lambda x=(k, v): self.set_item(x)})
            if k in ["Чёрный", "Коричневый"]:
                temp.update({"text_color": "white"})
                temp.update({"icon_color": "white"})
            else:
                temp.update({"text_color": "black"})
                temp.update({"icon_color": "black"})
            band.append(temp)
        return band

    def menu_open(self, *args):
        self.children[0].icon = "chevron-up"
        self.menu.open()

    def set_item(self, param_item):
        self.color_name = param_item[0]
        self.md_bg_color = param_item[1]
        self.children[0].icon = "chevron-down"
        if param_item[0] in ["Чёрный", "Коричневый"]:
            self.children[0].icon_color = self.text_color = "white"
        else:
            self.children[0].icon_color = self.text_color = "black"
        self.parent.parent.parent.parent.parent.calculate_resistor()
        self.menu.dismiss()


class THResistorsMarkingScreen(MDScreen):
    nominal = {"Чёрный": 0, "Коричневый": 1, "Красный": 2, "Оранжевый": 3, "Жёлтый": 4, "Зелёный": 5,
               "Синий": 6, "Фиолетовый": 7, "Серый": 8, "Белый": 9}

    multiplier = {"Золотой": 0.1, "Серебристый": 0.01, "Чёрный": 1, "Коричневый": 10, "Красный": 100, "Оранжевый": 1000,
                  "Жёлтый": 10000,
                  "Зелёный": 100000, "Синий": 1000000, "Фиолетовый": 10000000, "Серый": 100000000}

    tolerance = {"Золотой": "±5%", "Серебристый": "±10%", "Чёрный": "±0,005%", "Коричневый": "±1%", "Красный": "±2%",
                 "Оранжевый": "±0,01%",
                 "Жёлтый": "±0,02%", "Зелёный": "±0,5%", "Синий": "±0,25%", "Фиолетовый": "±0,1%", "Серый": "±0,05%"}

    thermal = {"Золотой": "±500 ppm/°С", "Серебристый": "±1000 ppm/°С", "Коричневый": "±100 ppm/°С",
               "Красный": "±50 ppm/°С",
               "Оранжевый": "±15 ppm/°С", "Жёлтый": "±25 ppm/°С", "Синий": "±10 ppm/°С", "Фиолетовый": "±5 ppm/°С",
               "Белый": "±1 ppm/°С"}

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
            resistance = (self.nominal[self.ids.bands.ids.band0.color_name] * 10 +
                          self.nominal[self.ids.bands.ids.band1.color_name]) * multiplier

            if "band3" in self.ids.bands.ids.keys():
                tolerance = self.tolerance[self.ids.bands.ids.band3.color_name]
            else:
                tolerance = "±20%"
        else:
            multiplier = self.multiplier[self.ids.bands.ids.band3.color_name]
            resistance = (self.nominal[self.ids.bands.ids.band0.color_name] * 100 +
                          self.nominal[self.ids.bands.ids.band1.color_name] * 10 +
                          self.nominal[self.ids.bands.ids.band2.color_name]) * multiplier

        if resistance < 1000:
            self.ids.result.text = "Результат: {:g} Ом {}{}".format(resistance, tolerance,
                                                                    (", ТКС: " + thermal) if thermal else "")
        elif resistance < 1000000:
            self.ids.result.text = "Результат: {:g} кОм {}{}".format(resistance / 1000, tolerance,
                                                                     (", ТКС: " + thermal) if thermal else "")
        else:
            self.ids.result.text = "Результат: {:g} МОм {}{}".format(resistance / 1000000, tolerance,
                                                                     (", ТКС: " + thermal) if thermal else "")


class SMDResistorsMarkingScreen(MDScreen):
    eia96 = {"01": 100, "02": 102, "03": 105, "04": 107, "05": 110, "06": 113, "07": 115, "08": 118, "09": 121,
             "10": 124, "11": 127, "12": 130, "13": 133, "14": 137, "15": 140, "16": 143, "17": 147, "18": 150,
             "19": 154, "20": 158, "21": 162, "22": 165, "23": 169, "24": 174, "25": 178, "26": 182, "27": 187,
             "28": 191, "29": 196, "30": 200, "31": 205, "32": 210, "33": 215, "34": 221, "35": 226, "36": 232,
             "37": 237, "38": 243, "39": 249, "40": 255, "41": 261, "42": 267, "43": 274, "44": 280, "45": 287,
             "46": 294, "47": 301, "48": 309, "49": 316, "50": 324, "51": 332, "52": 340, "53": 348, "54": 357,
             "55": 365, "56": 374, "57": 383, "58": 392, "59": 402, "60": 412, "61": 422, "62": 432, "63": 442,
             "64": 453, "65": 464, "66": 475, "67": 487, "68": 499, "69": 511, "70": 523, "71": 536, "72": 549,
             "73": 562, "74": 576, "75": 590, "76": 604, "77": 619, "78": 634, "79": 649, "80": 665, "81": 681,
             "82": 698, "83": 715, "84": 732, "85": 750, "86": 768, "87": 787, "88": 806, "89": 825, "90": 845,
             "91": 866, "92": 887, "93": 909, "94": 931, "95": 953, "96": 976}

    eia96_multiplier = {"z": 0.001, "y": 0.01, "r": 0.01, "x": 0.1, "s": 0.1, "a": 1, "b": 10, "h": 10, "c": 100,
                        "d": 1000, "e": 10000, "f": 100000}

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
                    resistance = float("{}.{}".format(markings[0], markings[1]))
                    if len(marking) == 4:
                        precision = True
                else:
                    self.ids.smd_result.text = "Неверный ввод"
            elif len(marking) == 3:
                if marking[2].isalpha() and marking[2].lower() in self.eia96_multiplier.keys():
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
                        self.ids.smd_result.text += "{:g} Ом".format(resistance)
                    elif resistance < 1000000:
                        self.ids.smd_result.text += "{:g} кОм".format(resistance / 1000)
                    else:
                        self.ids.smd_result.text += "{:g} МОм".format(resistance / 1000000)
                    if precision and resistance != 0:
                        self.ids.smd_result.text += " ±1%"
                    elif resistance != 0:
                        self.ids.smd_result.text += " ±5%"
                except ValueError:
                    return "Неверный ввод"
        except ValueError:
            self.ids.smd_result.text = "Неверный ввод"


class CapacitorsMarkingSelectScreen(MDScreen):
    pass


class THCapacitorsMarkingScreen(MDScreen):
    decimal_point = {"μ": 1000000, "u": 1000000, "p": 1, "n": 1000, "мк": 1000000, "н": 1000, "п": 1}

    def calculate_capacitor(self, value):
        capacity = ""
        if value.isdigit():
            if len(value) <= 2:
                capacity = int(value)
            else:
                capacity = int(value[-2::-1][::-1]) * 10 ** int(value[-1])
        elif "r" in value.lower():
            capacity = float("{}.{}".format(value.lower().split("r")[0], value.lower().split("r")[1]))
        elif any(ext in value for ext in self.decimal_point.keys()):
            intersection = "".join([inter for inter in self.decimal_point.keys() if (inter in value)])
            capacity = float("{}.{}".format(value.split(intersection)[0], value.split(intersection)[1])) * \
                       self.decimal_point[intersection]
        else:
            self.ids.th_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.th_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.th_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.th_capacitor_result.text += "{:g} пФ".format(capacity)
                elif capacity < 1000000:
                    self.ids.th_capacitor_result.text += "{:g} нФ".format(capacity / 1000)
                elif capacity < 1000000000:
                    self.ids.th_capacitor_result.text += "{:g} мкФ".format(capacity / 1000000)
                else:
                    self.ids.th_capacitor_result.text += "{:g} мФ".format(capacity / 1000000000)
            except ValueError:
                return "Неверный ввод!"


class SMDCapacitorsMarkingScreen(MDScreen):
    voltage = {"e": 2.5, "G": 4, "J": 7, "A": 10, "C": 16, "D": 20, "E": 25, "V": 35, "H": 50}
    smd_capacity = {"A": 1., "B": 1.1, "C": 1.2, "D": 1.3, "E": 1.5, "F": 1.6, "G": 1.8, "H": 2.0, "J": 2.2, "K": 2.4,
                    "L": 2.7, "M": 3.0, "N": 3.3, "P": 3.6, "Q": 3.9, "R": 4.3, "S": 4.7, "T": 5.1, "U": 5.6, "V": 6.2,
                    "W": 6.8, "X": 7.5, "Y": 8.2, "Z": 9.1, "a": 2.5, "b": 3.5, "d": 4.0, "e": 4.5, "f": 5.0, "m": 6.0,
                    "n": 7.0, "t": 8.0}

    def calculate_smd_capacitor(self, value):
        capacity = ""
        voltage = "?"
        values = list(value)
        if len(values) == 2:
            if values[0] in self.smd_capacity.keys():
                capacity = self.smd_capacity[values[0]] * 10 ** int(values[1])
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
        elif len(values) == 3:
            if values[0] in self.voltage.keys():
                voltage = self.voltage[values[0]]
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
            if values[1] in self.smd_capacity.keys():
                capacity = self.smd_capacity[values[1]] * 10 ** int(values[2])
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
        elif len(values) == 4:
            if values[0] in self.voltage.keys():
                voltage = self.voltage[values[0]]
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
            capacity = int(''.join((str(i) for i in values[1:3]))) * 10 ** int(values[3])
        else:
            self.ids.smd_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.smd_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.smd_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.smd_capacitor_result.text += "{:g} пФ".format(capacity)
                elif capacity < 1000000:
                    self.ids.smd_capacitor_result.text += "{:g} нФ".format(capacity / 1000)
                elif capacity < 1000000000:
                    self.ids.smd_capacitor_result.text += "{:g} мкФ".format(capacity / 1000000)
                else:
                    self.ids.smd_capacitor_result.text += "{:g} мФ".format(capacity / 1000000000)
            except ValueError:
                return "Неверный ввод!"
            self.ids.smd_capacitor_result.text += ", " + str(voltage) + " В"


class CalculationsScreenManager(MDScreenManager):
    pass


class CalculationsScreen(MDScreen):
    pass


class ConverterCalculationScreen(MDScreen):
    from_to = {"милдюйм": 0.001, "дюйммил": 1000, "дюймсм": 2.54, "смдюйм": 0.3937007874, "сммил": 393.7007874016,
               "милсм": 0.00254, "сммм": 10, "ммсм": 0.1, "дюйммм": 25.4, "ммдюйм": 0.0393700787, "милмм": 0.0254,
               "мил²дюйм²": 0.000001, "дюйм²мил²": 1000000, "дюйм²см²": 6.4516, "см²дюйм²": 0.15500031,
               "см²мил²": 155000.31000062, "мил²см²": 0.0000064516, "см²мм²": 100, "мм²см²": 0.01, "дюйм²мм²": 645.16,
               "мм²дюйм²": 0.0015500031, "мил²мм²": 0.00064516, "круг. милмил²": 0.7853981634,
               "мил²круг. мил": 1.2732395447, "круг. милсм²": 0.000005067, "см²круг. мил": 197352.5241389985,
               "круг. милмм²": 0.00050670748, "мм²круг. мил": 1973.52524138998, "дюйм²круг. мил": 1273239.5447351627,
               "круг. милдюйм²": 0.0000007854, "Ваттэрг/с": 10000000, "эрг/сВатт": 0.0000001, "нФпФ": 1000,
               "пФнФ": 0.001, "нФмкФ": 0.001, "мкФнФ": 1000, "пФмкФ": 0.000001, "мкФпФ": 1000000
               }

    def build_menu(self):
        self.build_menu_from()
        self.build_menu_to()

    def build_menu_from(self, *args, **kwargs):
        self.menu_items = [{"text": "мил",
                            "on_release": lambda x="мил": self.set_item_from(x),
                            },
                           {"text": "дюйм",
                            "on_release": lambda x="дюйм": self.set_item_from(x),
                            },
                           {"text": "см",
                            "on_release": lambda x="см": self.set_item_from(x),
                            },
                           {"text": "мм",
                            "on_release": lambda x="мм": self.set_item_from(x),
                            },
                           {"text": "мил²",
                            "on_release": lambda x="мил²": self.set_item_from(x),
                            },
                           {"text": "дюйм²",
                            "on_release": lambda x="дюйм²": self.set_item_from(x),
                            },
                           {"text": "см²",
                            "on_release": lambda x="см²": self.set_item_from(x),
                            },
                           {"text": "мм²",
                            "on_release": lambda x="мм²": self.set_item_from(x),
                            },
                           {"text": "круг. мил",
                            "on_release": lambda x="круг. мил": self.set_item_from(x),
                            },
                           {"text": "пФ",
                            "on_release": lambda x="пФ": self.set_item_from(x),
                            },
                           {"text": "нФ",
                            "on_release": lambda x="нФ": self.set_item_from(x),
                            },
                           {"text": "мкФ",
                            "on_release": lambda x="мкФ": self.set_item_from(x),
                            },
                           {"text": "Ватт",
                            "on_release": lambda x="Ватт": self.set_item_from(x),
                            },
                           {"text": "эрг/с",
                            "on_release": lambda x="эрг/с": self.set_item_from(x),
                            },
                           ]

        self.menu_from = MDDropdownMenu(
            caller=self.ids.convert_from,
            items=self.menu_items,
            width=dp(101),
        )

    def set_item_from(self, text_item):
        self.ids.convert_from.text = text_item
        self.menu_from.dismiss()
        self.convert(self.ids.convert_from_input.text, self.ids.convert_from.text, self.ids.convert_to.text)

    def build_menu_to(self, *args, **kwargs):
        self.menu_items = [{"text": "мил",
                            "on_release": lambda x="мил": self.set_item_to(x),
                            },
                           {"text": "дюйм",
                            "on_release": lambda x="дюйм": self.set_item_to(x),
                            },
                           {"text": "см",
                            "on_release": lambda x="см": self.set_item_to(x),
                            },
                           {"text": "мм",
                            "on_release": lambda x="мм": self.set_item_to(x),
                            },
                           {"text": "мил²",
                            "on_release": lambda x="мил²": self.set_item_to(x),
                            },
                           {"text": "дюйм²",
                            "on_release": lambda x="дюйм²": self.set_item_to(x),
                            },
                           {"text": "см²",
                            "on_release": lambda x="см²": self.set_item_to(x),
                            },
                           {"text": "мм²",
                            "on_release": lambda x="мм²": self.set_item_to(x),
                            },
                           {"text": "круг. мил",
                            "on_release": lambda x="круг. мил": self.set_item_to(x),
                            },
                           {"text": "пФ",
                            "on_release": lambda x="пФ": self.set_item_to(x),
                            },
                           {"text": "нФ",
                            "on_release": lambda x="нФ": self.set_item_to(x),
                            },
                           {"text": "мкФ",
                            "on_release": lambda x="мкФ": self.set_item_to(x),
                            },
                           {"text": "Ватт",
                            "on_release": lambda x="Ватт": self.set_item_to(x),
                            },
                           {"text": "эрг/с",
                            "on_release": lambda x="эрг/с": self.set_item_to(x),
                            },
                           ]

        self.menu_to = MDDropdownMenu(
            caller=self.ids.convert_from,
            items=self.menu_items,
            width=dp(101),
        )

    def set_item_to(self, text_item):
        self.ids.convert_to.text = text_item
        self.menu_to.dismiss()
        self.convert(self.ids.convert_from_input.text, self.ids.convert_from.text, self.ids.convert_to.text)

    def convert(self, convert_from_val, convert_from_unit, convert_to_unit):
        try:
            if convert_from_unit == convert_to_unit:
                self.ids.convert_to_result.text = str(float(convert_from_val))
            else:
                direction = convert_from_unit + convert_to_unit
                if direction in self.from_to.keys():
                    result = float(convert_from_val) * self.from_to[direction]
                    self.ids.convert_to_result.text = "{:g}".format(result)
                else:
                    self.ids.convert_to_result.text = "Непереводимые величины"
        except ValueError:
            self.ids.convert_to_result.text = "Неверный ввод!"


class LEDResistorCalculationScreen(MDScreen):
    diodes = {'3 мм зелёный': (2.3, 20), '3 мм красный': (1.9, 20), '3 мм жёлтый': (2.1, 20), '3 мм синий': (2.9, 20),
              '5 мм зелёный': (2.3, 20), '5 мм красный': (1.9, 20), '5 мм жёлтый': (2.1, 20), '5 мм синий': (3.6, 75),
              '5 мм белый': (3.6, 75), '10 мм синий': (3.2, 20), '10 мм белый': (3.2, 20), 'Cree MX-3': (3.7, 350)}

    def build_menu(self, *args, **kwargs):
        # [{"center_text": "3",
        #   "viewclass": "CenterList",
        #   "on_release": lambda x="3": self.set_item(x),
        #   "height": dp(56), },
        #  {"center_text": "4",
        #   "viewclass": "CenterList",
        #   "on_release": lambda x="4": self.set_item(x),
        #   "height": dp(56), },
        #  {"center_text": "5",
        #   "viewclass": "CenterList",
        #   "on_release": lambda x="5": self.set_item(x),
        #   "height": dp(56), },
        #  {"center_text": "6",
        #   "viewclass": "CenterList",
        #   "on_release": lambda x="6": self.set_item(x),
        #   "height": dp(56), }, ]

        self.menu_items = []
        for i in range(len(self.diodes.keys())):
            self.menu_items.append({"text": list(self.diodes.keys())[i],
                                    "on_release": lambda x=list(self.diodes.keys())[i]: self.set_item(x),
                                    "height": dp(56), "text_color": "black", "md_bg_color": "red"})
        self.menu = MDDropdownMenu(
            caller=self,
            items=self.menu_items,
        )

    def set_item(self, text_item):
        self.ids.resistor_marking_menu_name.text = text_item
        self.menu.dismiss()

    def led_calculate(self, vol, led_vol, led_cur, led_quant):
        try:
            led_resistance = (float(vol) - (float(led_vol) * float(led_quant))) / (float(led_cur) / 1000)
            if led_resistance < 0:
                self.ids.led_result.text = "Слишком малое напряжение источника питания!"
                self.ids.led_res_power.text = ''
                self.ids.led_cur.text = ''
                self.ids.led_e24.text = ''
            else:
                self.ids.led_result.text = format_output_resistor(led_resistance)
                e24_result = e24.calculate_standard_resistor(led_resistance, True)
                self.ids.led_e24.text = format_output_resistor(e24_result)

                self.ids.led_res_power.text = "{:g} мВт".format((float(vol) - float(led_vol)) *
                                                                float(led_cur) * float(led_quant))
                self.ids.led_cur.text = "{:g} мА".format(float(led_cur) * float(led_quant))
        except ValueError:
            self.ids.led_e24.text = "Неверный ввод!"
            self.ids.led_result.text = "Неверный ввод!"
            self.ids.led_res_power.text = "Неверный ввод!"
            self.ids.led_cur.text = "Неверный ввод!"


class InductorCalculationSelectScreen(MDScreen):
    pass


class InductorCalculateInductionScreen(MDScreen):
    def inductor_calculate_henrys(self, turns, diameter, length):
        try:

            turns = float(turns)
            diameter = float(diameter)
            length = float(length)

            formfactor = length / diameter

            induction = 0.0002 * math.pi * diameter * turns ** 2 * (math.log(1 + math.pi / (2 * formfactor)) +
                                                                    1 / (2.3004 + 3.437 * formfactor + 1.7636 *
                                                                         formfactor ** 2 - 0.47 / (0.755 + 1 /
                                                                                                   formfactor) ** 1.44))
            self.ids.induction.text = "{:g} мкГн".format(induction)
        except Exception:
            self.ids.induction.text = "Неверный ввод!"


class InductorCalculateSizeScreen(MDScreen):
    def inductor_calculate_turns(self, henrys, diameter, oneturn):
        try:
            henrys = float(henrys)
            diameter = float(diameter) / 10  # в формуле сантиметры, во вводе миллиметры
            oneturn = float(oneturn) / 10
            inductor_length = (50 * oneturn ** 2 * henrys + math.sqrt(5) * math.sqrt(500 * oneturn ** 4 * henrys ** 2 +
                                                                                     9 * oneturn ** 2 * diameter ** 3 * henrys)) / diameter ** 2

            inductor_turns = inductor_length / oneturn
            inductor_turns_int = round(inductor_turns, 0)
            inductor_length_int = inductor_turns_int * oneturn * 10

            self.ids.inductor_length.text = "{:g} мм".format(inductor_length * 10)
            self.ids.inductor_length_int.text = "{:g} мм".format(inductor_length_int)
            self.ids.inductor_turns.text = "{:g} витка(ов)".format(inductor_turns)
            self.ids.inductor_turns_int.text = "{:g} витка(ов)".format(inductor_turns_int)
        except Exception:
            self.ids.inductor_length.text = "Неверный ввод!"
            self.ids.inductor_length_int.text = "Неверный ввод!"
            self.ids.inductor_turns.text = "Неверный ввод!"
            self.ids.inductor_turns_int.text = "Неверный ввод!"


class ParallelResistorCalculationScreen(MDScreen):
    counter = 0

    def reset(self):
        self.ids.par_res_box.clear_widgets()
        self.ids.par_res_output.text = ""
        self.counter = 0
        for i in range(0, 2):
            self.add_resistor()

    def add_resistor(self):
        self.counter += 1
        input_card = MDCard(size_hint_y=None,
                            padding=(sp(15), 0),
                            spacing=sp(15))
        self.ids.par_res_box.add_widget(input_card)
        label = MDLabel(text="Резистор " + str(self.counter) + ", Ом",
                        size_hint_y=None, )
        resistor_input = MDTextField(halign="center",
                                     size_hint_x=0.6,
                                     size_hint_y=None, )
        input_card.add_widget(label)
        input_card.add_widget(resistor_input)
        self.ids.par_res_box.ids["resistor_input" + str(self.counter)] = weakref.ref(resistor_input)

    def par_res_calculate(self):
        res_list = []
        try:
            for widget in self.ids.par_res_box.children:
                res_list.append(1 / float(widget.children[0].text))
            resistance = 1 / (sum(res_list))
            self.ids.par_res_output.text = format_output_resistor(resistance)
        except ValueError:
            self.ids.par_res_output.text = "Неверный ввод!"
        except ZeroDivisionError:
            self.ids.par_res_output.text = format_output_resistor(0)


class SerialCapacitorCalculateScreen(MDScreen):
    counter = 0

    def reset(self):
        self.ids.ser_cap_box.clear_widgets()
        self.counter = 0
        self.ids.ser_cap_output.text = ""
        for i in range(0, 2):
            self.add_capacitor()

    def add_capacitor(self):
        self.counter += 1
        input_card = MDCard(size_hint_y=None,
                            padding=(sp(15), 0),
                            spacing=sp(15))
        self.ids.ser_cap_box.add_widget(input_card)
        label = MDLabel(text="Конденсатор " + str(self.counter) + ", пФ",
                        size_hint_y=None, )
        capacitor_input = MDTextField(halign="center",
                                      size_hint_x=0.6,
                                      size_hint_y=None, )
        input_card.add_widget(label)
        input_card.add_widget(capacitor_input)
        self.ids.ser_cap_box.ids["capacitor_input" + str(self.counter)] = weakref.ref(capacitor_input)

    def ser_cap_calculate(self):
        cap_list = []
        try:
            for widget in self.ids.ser_cap_box.children:
                cap_list.append(1 / float(widget.children[0].text))
            capacitance = 1 / (sum(cap_list))
            self.ids.ser_cap_output.text = format_output_capacitor(capacitance)
        except ValueError:
            self.ids.ser_cap_output.text = "Неверный ввод!"
        except ZeroDivisionError:
            self.ids.ser_cap_output.text = format_output_capacitor(0)


class VoltageDividerCalculateSelectScreen(MDScreen):
    pass


class VoltageDividerCalculateVoltageScreen(MDScreen):
    def divider_calculate_vout(self, vin, r1, r2):
        try:
            vin = float(vin)
            r1 = float(r1)
            r2 = float(r2)

            vout = r2 * vin / (r1 + r2)
            rate = vin / vout

            self.ids.v_out.text = "{:g}".format(vout)
            self.ids.divider_rate.text = "{:g}".format(rate)
        except Exception:
            self.ids.v_out.text = "Неверный ввод!"
            self.ids.divider_rate.text = ""


class VoltageDividerCalculateResistanceScreen(MDScreen):
    def divider_calculate_r(self, vin, vout, r1):
        try:
            vin = float(vin)
            vout = float(vout)
            r1 = float(r1)

            if vin <= vout:
                self.ids.r2_calculated.text = "Проверьте напряжения!"
                self.ids.divider_rate_r.text = ""
            else:
                r2 = r1 * vout / (vin - vout)
                rate = vin / vout

                self.ids.r2_calculated.text = "{:g}".format(r2)
                if r2 == 0:
                    self.ids.r2_calculated.text = "0 Ом (перемычка)"
                elif r2 < 1000:
                    self.ids.r2_calculated.text = "{:g} Ом".format(r2)
                elif r2 < 1000000:
                    self.ids.r2_calculated.text = "{:g} кОм".format(r2 / 1000)
                else:
                    self.ids.r2_calculated.text = "{:g} МОм".format(r2 / 1000000)

                self.ids.divider_rate_r.text = "{:g}".format(rate)

                e6_result = e24.calculate_standard_resistor(r2, False)
                if e6_result == 0:
                    self.ids.r2_e24.text = "0 Ом (перемычка)"
                elif e6_result < 1000:
                    self.ids.r2_e24.text = "{:g} Ом".format(e6_result)
                elif e6_result < 1000000:
                    self.ids.r2_e24.text = "{:g} кОм".format(e6_result / 1000)
                else:
                    self.ids.r2_e24.text = "{:g} МОм".format(e6_result / 1000000)

                vout_corrected = e6_result * vin / (r1 + e6_result)
                self.ids.vout_e24.text = "{:g} В".format(vout_corrected)
        except (ZeroDivisionError, ValueError):
            self.ids.r2_calculated.text = "Неверный ввод!"
            self.ids.divider_rate_r.text = ""


class LMRegulatorCalculateSelectScreen(MDScreen):
    pass


class LMRegulatorCalculateVoltageScreen(MDScreen):
    def calculate_lm317_voltage(self, vout, r1, iout, vin):
        try:
            vout = float(vout)
            r1 = float(r1)
            iout = float(iout)
            vin = float(vin)
            if iout > 5:
                self.ids.lm317_r2_output.text = "Ток нагрузки должен быть меньше 5А!"
                self.ids.lm317_r2_corrected_output.text = "Ток нагрузки должен быть меньше 5А!"
                self.ids.lm317_r2_output.text = ""
                self.ids.lm317_vout_output.text = ""
                self.ids.lm317_recommend_output.text = ""
                self.ids.lm317_power_output.text = ""
            else:
                r2 = r1 * (vout / 1.25 - 1)
                result = format_output_resistor(r2)

                r2_corrected = e24.calculate_standard_resistor(r2, False)

                power = (vin - vout) * iout

                vout_corrected = 1.25 * (1 + r2_corrected / r1)

                if iout > 3:
                    recommend = "LM338"
                elif iout > 1.5:
                    recommend = "LM350"
                else:
                    recommend = "LM317"
                result_corrected = format_output_resistor(r2_corrected)

                self.ids.lm317_r2_corrected_output.text = result_corrected
                self.ids.lm317_r2_output.text = result
                self.ids.lm317_vout_output.text = "{:g} В".format(vout_corrected)
                self.ids.lm317_recommend_output.text = recommend
                self.ids.lm317_power_output.text = "{:g} Вт".format(power)

        except Exception:
            self.ids.lm317_r2_output.text = "Неверный ввод!"
            self.ids.lm317_r2_corrected_output.text = "Неверный ввод!"
            self.ids.lm317_r2_output.text = "Неверный ввод!"
            self.ids.lm317_vout_output.text = "Неверный ввод!"
            self.ids.lm317_recommend_output.text = "Неверный ввод!"
            self.ids.lm317_power_output.text = "Неверный ввод!"


class LMRegulatorCalculateCurrentScreen(MDScreen):
    def calculate_lm317_current(self, iout, vout):
        try:
            iout = float(iout)
            if iout <= 5:
                r1 = 1.25 / iout

                r1_corrected = e24.calculate_standard_resistor(r1, True)

                if iout > 3:
                    recommend = "LM338"
                elif iout > 1.5:
                    recommend = "LM350"
                else:
                    recommend = "LM317"
                result = format_output_resistor(r1)
                result_corrected = format_output_resistor(r1_corrected)

                iout_corrected = 1.25 / r1_corrected

                power_r1 = iout ** 2 * r1
                power_corrected = iout_corrected ** 2 * r1_corrected

                if vout:
                    vout = float(vout)
                    if not (3 <= vout <= 38):
                        self.ids.lm317_vin_output_cur.text = "Падение напряжения должно быть больше 2В и меньше 38В!"
                        self.ids.lm317_vin_output_cur.font_size = "10sp"
                    else:
                        vin_corrected = vout + 3.7
                        self.ids.lm317_vin_output_cur.text = "{:g} В".format(vin_corrected)
                else:
                    self.ids.lm317_vin_output_cur.text = ""

                self.ids.lm317_r1_output_cur.text = result
                self.ids.lm317_r1_corrected_output_cur.text = result_corrected
                self.ids.lm317_r1_power_output_cur.text = "{:g} Вт".format(power_r1)
                self.ids.lm317_r1_power_corrected_output_cur.text = "{:g} Вт".format(power_corrected)
                self.ids.lm317_iout_corrected_output_cur.text = "{:g} А".format(iout_corrected)
                self.ids.lm317_recommend_output_cur.text = recommend
            else:
                self.ids.lm317_r1_output_cur.text = "Ток должен быть менее 5А!"
                self.ids.lm317_r1_corrected_output_cur.text = ""
                self.ids.lm317_r1_power_output_cur.text = ""
                self.ids.lm317_r1_power_corrected_output_cur.text = ""
                self.ids.lm317_iout_corrected_output_cur.text = ""
                self.ids.lm317_recommend_output_cur.text = ""
                self.ids.lm317_vin_output_cur.text = ""

        except Exception:
            self.ids.lm317_r1_output_cur.text = "Неверный ввод!"
            self.ids.lm317_r1_corrected_output_cur.text = "Неверный ввод!"
            self.ids.lm317_r1_power_output_cur.text = "Неверный ввод!"
            self.ids.lm317_r1_power_corrected_output_cur.text = "Неверный ввод!"
            self.ids.lm317_iout_corrected_output_cur.text = "Неверный ввод!"
            self.ids.lm317_recommend_output_cur.text = "Неверный ввод!"
            self.ids.lm317_vin_output_cur.text = "Неверный ввод!"


class HandbookScreenManager(MDScreenManager):
    pass


class HandbookScreen(MDScreen):
    pass


class TheoryScreen(MDScreen):
    pass


class SchematicsScreen(MDScreen):
    pass


class PinoutScreen(MDScreen):
    pass


class ConnectionsScreen(MDScreen):
    pass


class ChipsScreen(MDScreen):
    pass


class ChipsAnalogsSelectScreen(MDScreen):
    pass


class ChipsAnalogs133Screen(MDScreen):
    pass


class ChipsAnalogs140Screen(MDScreen):
    pass


class ChipsAnalogs140(MDGridLayout):
    series140 = {"140УД5А,Б": "CA3015", "КР140УД5А,Б": "CA3015", "140УД6А,Б": "MG1556G", "КР140УД6": "MC1556C",
                 "140УД7": "(A741", "КР140УД7": "(A741C", "КФ140УД7": "SFC2741", "Н140УД7": "SE535",
                 "140УД8А,Б": "(A740", "КР140УД8А-Г": "(A740C", "140УД11": "LM318", "КР140УД11": "LM318",
                 "140УД12": "(A776", "КР140УД12": "(A776C", "140УД13": "(A727M", "140УД14": "LM108",
                 "КР140УД14А": "LM308", "КР140УД14Б": "LM308", "140УД17А": "OP-07", "140УД17Б": "OP-07A",
                 "КР140УД17А": "OP-07E", "КР140УД17Б": "OP-07C", "Н140УД17А": "OP-07", "Н140УД17Б": "OP-07A",
                 "КР140УД18": "LF355", "140УД20А": "(A747", "140УД20Б": "(A747", "КР140УД20А": "(A747C",
                 "КР140УД20Б": "(A747C", "КМ140УД20": "(A747C", "Н140УД20А": "(A747", "Н140УД20Б": "(A747",
                 "140УД21": "HA2900", "КР140УД22": "LF356", "КР140УД22А": "LF356", "140УД23": "LF157",
                 "140УД24": "ICL7650", "140УД25А": "OP-27A", "140УД25Б": "OP-27B", "140УД25В": "OP-27C",
                 "КР140УД25А": "OP-27A", "КР140УД25Б": "OP-27B", "КР140УД25В": "OP-27C", "КР140УД25Г": "OP-27B",
                 "140УД26А": "OP-37A", "140УД26Б": "OP-37B", "140УД26В": "OP-37C", "КР140УД26А": "OP-37A",
                 "КР140УД26Б": "OP-37B", "КР140УД26В": "OP-37C", "КР140УД26Г": "OP-37B", "140УД501А": "CA3015",
                 "140УД501Б": "CA3015", "140УД601А": "MC1556G", "140УД601Б": "MC1556G", "КР140УД608": "MC1456CP1",
                 "140УД701": "(A741", "КР140УД708": "(A741C", "КР140УД1101": "LM318", "140УД1201": "(A776",
                 "КР140УД1208": "(A776C", "140УД1301": "(A727M", "140УД1401": "LM108", "КР140УД1408А": "LM308",
                 "КР140УД1408Б": "LM308", "140УД1701А": "OP-07", "140УД1701Б": "OP-07A"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True
        self.padding = 10
        self.cols = 2
        for k, v in self.series140.items():
            self.add_widget(MDLabel(text=k, size_hint=(1, None), adaptive_height=True))
            self.add_widget(MDLabel(text=v, size_hint=(1, None), adaptive_height=True))
            self.add_widget(MDDivider())
            self.add_widget(MDDivider())



class ChipsAnalogs580Screen(MDScreen):
    pass


class ChipsAnalogs580(MDGridLayout):
    series580 = {"КР580ВА86": "8286", "КР580ВА87": "8287", "580ВВ51": "8251", "КР580ВВ51А": "8251A", "580ВВ55": "8255",
                 "КР580ВВ55А": "8255A", "580ВВ79": "8279", "КР580ВВ79": "8279", "КР580ВГ18": "8218",
                 "КР580ВГ75": "8275", "КР580ВГ92": "8292", "580ВИ53": "8253", "КР580ВИ53": "8253", "КР580ВК28": "8228",
                 "КР580ВК38": "8238", "КР580ВК91А": "8291", "580ВМ80": "8280", "КР580ВМ80А": "8280",
                 "КР580ВР43": "8243", "КР580ВТ42": "8242", "580ВТ57": "8257", "КР580ВТ57": "8257", "КР580ГФ24": "8224",
                 "КР580ИР82": "8282", "КР580ИР83": "8283"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True
        self.padding = 10
        self.cols = 2
        for k, v in self.series580.items():
            self.add_widget(MDLabel(text=k, size_hint=(1, None), adaptive_height=True))
            self.add_widget(MDLabel(text=v, size_hint=(1, None), adaptive_height=True))
            self.add_widget(MDDivider())
            self.add_widget(MDDivider())


class LifehacksScreen(MDScreen):
    pass


class HelpScreenManager(MDScreenManager):
    pass


class HelpScreen(MDScreen):
    pass


class HowToScreeen(MDScreen):
    pass


class AboutScreen(MDScreen):
    def mailto(self):
        webbrowser.open("mailto:electronics@hand-made-tlt.ru")

    def pay(self):
        webbrowser.open("https://yoomoney.ru/fundraise/2SFAdwO6BB0.230827")

    def git(self):
        webbrowser.open("https://github.com/LemanRus/RadioMan")

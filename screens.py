import itertools
import math
import weakref
import webbrowser

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivymd.uix.button import MDButton, MDButtonIcon
from kivymd.uix.card import MDCard
from kivymd.uix.divider import MDDivider
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField

from e24_nominals import E24Nominals as e24
from output_value_methods import format_output_resistor, \
    format_output_capacitor


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
        "Золотой": [1, 0.84, 0, 1], "Серебристый": [0.8, 0.8, 0.8, 1],
        "Чёрный": [0, 0, 0, 1], "Коричневый": [0.4, 0.22, 0, 1],
        "Красный": [1, 0, 0, 1], "Оранжевый": [0.98, 0.45, 0.02, 1],
        "Жёлтый": [1, 1, 0, 1], "Зелёный": [0.05, 0.64, 0.05, 1],
        "Синий": [0.05, 0.54, 0.95, 1], "Фиолетовый": [0.54, 0.14, 0.59, 1],
        "Серый": [0.5, 0.5, 0.5, 1], "Белый": [1, 1, 1, 1]
    }
    bands_accordance = {
        3: {
            0: dict(
                itertools.islice(colors.items(), 3, None)
                ),
            1: dict(
                itertools.islice(colors.items(), 2, None)
                ),
            2: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()))
                ),
        },
        4: {
            0: dict(
                itertools.islice(colors.items(), 3, None)
                ),
            1: dict(
                itertools.islice(colors.items(), 2, None)
                ),
            2: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)
                ),
            3: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)
                ),
        }, 5: {
            0: dict(
                itertools.islice(colors.items(), 3, None)
                ),
            1: dict(
                itertools.islice(colors.items(), 2, None)
                ),
            2: dict(
                itertools.islice(colors.items(), 2, None)
                ),
            3: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)
                ),
            4: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)
                ),
        }, 6: {
            0: dict(
                itertools.islice(colors.items(), 3, None)
                ),
            1: dict(
                itertools.islice(colors.items(), 2, None)),
            2: dict(
                itertools.islice(colors.items(), 2, None)),
            3: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            4: dict(
                itertools.islice(colors.items(), 0, len(colors.keys()) - 1)),
            5: dict(
                itertools.islice(colors.items(), 0, 2)
                ) | dict(
                    itertools.islice(colors.items(), 3, 7)
                    ) | dict(
                        itertools.islice(colors.items(), 8, 10)
                        ) | dict(
                            itertools.islice(colors.items(), 11, 12)
                            )
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
        self.theme_bg_color = self.theme_text_color = \
            self.theme_width = self.theme_height = "Custom"
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
        self.menu.bind(on_dismiss=lambda _: self.__setattr__(
            "icon", "chevron-down"
            ))

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
    nominal = {"Чёрный": 0, "Коричневый": 1, "Красный": 2, "Оранжевый": 3,
               "Жёлтый": 4, "Зелёный": 5, "Синий": 6, "Фиолетовый": 7,
               "Серый": 8, "Белый": 9}

    multiplier = {"Золотой": 0.1, "Серебристый": 0.01, "Чёрный": 1,
                  "Коричневый": 10, "Красный": 100, "Оранжевый": 1000,
                  "Жёлтый": 10000, "Зелёный": 100000, "Синий": 1000000,
                  "Фиолетовый": 10000000, "Серый": 100000000}

    tolerance = {"Золотой": "±5%", "Серебристый": "±10%", "Чёрный": "±0,005%",
                 "Коричневый": "±1%", "Красный": "±2%", "Оранжевый": "±0,01%",
                 "Жёлтый": "±0,02%", "Зелёный": "±0,5%", "Синий": "±0,25%",
                 "Фиолетовый": "±0,1%", "Серый": "±0,05%"}

    thermal = {"Золотой": "±500 ppm/°С", "Серебристый": "±1000 ppm/°С",
               "Коричневый": "±100 ppm/°С", "Красный": "±50 ppm/°С",
               "Оранжевый": "±15 ppm/°С", "Жёлтый": "±25 ppm/°С",
               "Синий": "±10 ppm/°С", "Фиолетовый": "±5 ppm/°С",
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
    eia96 = {"01": 100, "02": 102, "03": 105, "04": 107, "05": 110, "06": 113,
             "07": 115, "08": 118, "09": 121, "10": 124, "11": 127, "12": 130,
             "13": 133, "14": 137, "15": 140, "16": 143, "17": 147, "18": 150,
             "19": 154, "20": 158, "21": 162, "22": 165, "23": 169, "24": 174,
             "25": 178, "26": 182, "27": 187, "28": 191, "29": 196, "30": 200,
             "31": 205, "32": 210, "33": 215, "34": 221, "35": 226, "36": 232,
             "37": 237, "38": 243, "39": 249, "40": 255, "41": 261, "42": 267,
             "43": 274, "44": 280, "45": 287, "46": 294, "47": 301, "48": 309,
             "49": 316, "50": 324, "51": 332, "52": 340, "53": 348, "54": 357,
             "55": 365, "56": 374, "57": 383, "58": 392, "59": 402, "60": 412,
             "61": 422, "62": 432, "63": 442, "64": 453, "65": 464, "66": 475,
             "67": 487, "68": 499, "69": 511, "70": 523, "71": 536, "72": 549,
             "73": 562, "74": 576, "75": 590, "76": 604, "77": 619, "78": 634,
             "79": 649, "80": 665, "81": 681, "82": 698, "83": 715, "84": 732,
             "85": 750, "86": 768, "87": 787, "88": 806, "89": 825, "90": 845,
             "91": 866, "92": 887, "93": 909, "94": 931, "95": 953, "96": 976}

    eia96_multiplier = {"z": 0.001, "y": 0.01, "r": 0.01, "x": 0.1, "s": 0.1,
                        "a": 1, "b": 10, "h": 10, "c": 100, "d": 1000,
                        "e": 10000, "f": 100000}

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


class CapacitorsMarkingSelectScreen(MDScreen):
    pass


class THCapacitorsMarkingScreen(MDScreen):
    decimal_point = {"μ": 1000000, "u": 1000000, "p": 1, "n": 1000,
                     "мк": 1000000, "н": 1000, "п": 1}

    def calculate_capacitor(self, value):
        capacity = ""
        if value.isdigit():
            if len(value) <= 2:
                capacity = int(value)
            else:
                capacity = int(value[-2::-1][::-1]) * 10 ** int(value[-1])
        elif "r" in value.lower():
            capacity = float(
                "{}.{}".format(
                    value.lower().split("r")[0], value.lower().split("r")[1]
                        )
                    )
        elif any(ext in value for ext in self.decimal_point.keys()):
            intersection = "".join(
                [inter for inter in self.decimal_point.keys()
                 if (inter in value)]
                 )
            capacity = float(
                "{}.{}".format(
                    value.split(intersection)[0], value.split(intersection)[1]
                    )
                        ) * self.decimal_point[intersection]
        else:
            self.ids.th_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.th_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.th_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.th_capacitor_result.text += "{:g} пФ".format(
                        capacity
                        )
                elif capacity < 1000000:
                    self.ids.th_capacitor_result.text += "{:g} нФ".format(
                        capacity / 1000
                        )
                elif capacity < 1000000000:
                    self.ids.th_capacitor_result.text += "{:g} мкФ".format(
                        capacity / 1000000
                        )
                else:
                    self.ids.th_capacitor_result.text += "{:g} мФ".format(
                        capacity / 1000000000
                        )
            except ValueError:
                return "Неверный ввод!"


class SMDCapacitorsMarkingScreen(MDScreen):
    voltage = {"e": 2.5, "G": 4, "J": 7, "A": 10, "C": 16, "D": 20, "E": 25,
               "V": 35, "H": 50}

    smd_capacity = {"A": 1., "B": 1.1, "C": 1.2, "D": 1.3, "E": 1.5, "F": 1.6,
                    "G": 1.8, "H": 2.0, "J": 2.2, "K": 2.4, "L": 2.7,
                    "M": 3.0, "N": 3.3, "P": 3.6, "Q": 3.9, "R": 4.3,
                    "S": 4.7, "T": 5.1, "U": 5.6, "V": 6.2, "W": 6.8,
                    "X": 7.5, "Y": 8.2, "Z": 9.1, "a": 2.5, "b": 3.5,
                    "d": 4.0, "e": 4.5, "f": 5.0, "m": 6.0, "n": 7.0,
                    "t": 8.0}

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
            capacity = int(''.join((str(i) for i in values[1:3]))) * \
                10 ** int(values[3])
        else:
            self.ids.smd_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.smd_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.smd_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.smd_capacitor_result.text += "{:g} пФ".format(
                        capacity
                        )
                elif capacity < 1000000:
                    self.ids.smd_capacitor_result.text += "{:g} нФ".format(
                        capacity / 1000
                        )
                elif capacity < 1000000000:
                    self.ids.smd_capacitor_result.text += "{:g} мкФ".format(
                        capacity / 1000000
                        )
                else:
                    self.ids.smd_capacitor_result.text += "{:g} мФ".format(
                        capacity / 1000000000
                        )
            except ValueError:
                return "Неверный ввод!"
            self.ids.smd_capacitor_result.text += ", " + str(voltage) + " В"


class CalculationsScreenManager(MDScreenManager):
    pass


class CalculationsScreen(MDScreen):
    pass


class ConverterCalculationScreen(MDScreen):
    from_to = {
        "милдюйм": 0.001, "дюйммил": 1000, "дюймсм": 2.54,
        "смдюйм": 0.3937007874, "сммил": 393.7007874016, "милсм": 0.00254,
        "сммм": 10, "ммсм": 0.1, "дюйммм": 25.4, "ммдюйм": 0.0393700787,
        "милмм": 0.0254, "мил²дюйм²": 0.000001, "дюйм²мил²": 1000000,
        "дюйм²см²": 6.4516, "см²дюйм²": 0.15500031,
        "см²мил²": 155000.31000062, "мил²см²": 0.0000064516, "см²мм²": 100,
        "мм²см²": 0.01, "дюйм²мм²": 645.16, "мм²дюйм²": 0.0015500031,
        "мил²мм²": 0.00064516, "круг. милмил²": 0.7853981634,
        "мил²круг. мил": 1.2732395447, "круг. милсм²": 0.000005067,
        "см²круг. мил": 197352.5241389985, "круг. милмм²": 0.00050670748,
        "мм²круг. мил": 1973.52524138998,
        "дюйм²круг. мил": 1273239.5447351627, "круг. милдюйм²": 0.0000007854,
        "Ваттэрг/с": 10000000, "эрг/сВатт": 0.0000001, "нФпФ": 1000,
        "пФнФ": 0.001, "нФмкФ": 0.001, "мкФнФ": 1000, "пФмкФ": 0.000001,
        "мкФпФ": 1000000,
        }

    def build_menu(self):
        self.build_menu_from()
        self.build_menu_to()

    def build_menu_from(self, *args, **kwargs):
        self.menu_items = [{
                "text": "мил",
                "on_release": lambda x="мил": self.set_item_from(x),
            }, {
                "text": "дюйм",
                "on_release": lambda x="дюйм": self.set_item_from(x),
            }, {
                "text": "см",
                "on_release": lambda x="см": self.set_item_from(x),
            }, {
                "text": "мм",
                "on_release": lambda x="мм": self.set_item_from(x),
            }, {
                "text": "мил²",
                "on_release": lambda x="мил²": self.set_item_from(x),
            }, {
                "text": "дюйм²",
                "on_release": lambda x="дюйм²": self.set_item_from(x),
            }, {
                "text": "см²",
                "on_release": lambda x="см²": self.set_item_from(x),
            }, {
                "text": "мм²",
                "on_release": lambda x="мм²": self.set_item_from(x),
            }, {
                "text": "круг. мил",
                "on_release": lambda x="круг. мил": self.set_item_from(x),
            }, {
                "text": "пФ",
                "on_release": lambda x="пФ": self.set_item_from(x),
            }, {
                "text": "нФ",
                "on_release": lambda x="нФ": self.set_item_from(x),
            }, {
                "text": "мкФ",
                "on_release": lambda x="мкФ": self.set_item_from(x),
            }, {
                "text": "Ватт",
                "on_release": lambda x="Ватт": self.set_item_from(x),
            }, {
                "text": "эрг/с",
                "on_release": lambda x="эрг/с": self.set_item_from(x),
            }, ]

        self.menu_from = MDDropdownMenu(
            caller=self.ids.convert_from,
            items=self.menu_items,
            width=dp(101),
        )

    def set_item_from(self, text_item):
        self.ids.convert_from.text = text_item
        self.menu_from.dismiss()
        self.convert(
            self.ids.convert_from_input.text,
            self.ids.convert_from.text,
            self.ids.convert_to.text
            )

    def build_menu_to(self, *args, **kwargs):
        self.menu_items = [{
                "text": "мил",
                "on_release": lambda x="мил": self.set_item_to(x),
            }, {
                "text": "дюйм",
                "on_release": lambda x="дюйм": self.set_item_to(x),
            }, {
                "text": "см",
                "on_release": lambda x="см": self.set_item_to(x),
            }, {
                "text": "мм",
                "on_release": lambda x="мм": self.set_item_to(x),
            }, {
                "text": "мил²",
                "on_release": lambda x="мил²": self.set_item_to(x),
            }, {
                "text": "дюйм²",
                "on_release": lambda x="дюйм²": self.set_item_to(x),
            }, {
                "text": "см²",
                "on_release": lambda x="см²": self.set_item_to(x),
            }, {
                "text": "мм²",
                "on_release": lambda x="мм²": self.set_item_to(x),
            }, {
                "text": "круг. мил",
                "on_release": lambda x="круг. мил": self.set_item_to(x),
            }, {
                "text": "пФ",
                "on_release": lambda x="пФ": self.set_item_to(x),
            }, {
                "text": "нФ",
                "on_release": lambda x="нФ": self.set_item_to(x),
            }, {
                "text": "мкФ",
                "on_release": lambda x="мкФ": self.set_item_to(x),
            }, {
                "text": "Ватт",
                "on_release": lambda x="Ватт": self.set_item_to(x),
            }, {
                "text": "эрг/с",
                "on_release": lambda x="эрг/с": self.set_item_to(x),
            }, ]

        self.menu_to = MDDropdownMenu(
            caller=self.ids.convert_from,
            items=self.menu_items,
            width=dp(101),
        )

    def set_item_to(self, text_item):
        self.ids.convert_to.text = text_item
        self.menu_to.dismiss()
        self.convert(
            self.ids.convert_from_input.text,
            self.ids.convert_from.text,
            self.ids.convert_to.text
            )

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
    def led_calculate(self, vol, led_vol, led_cur, led_quant):
        try:
            led_resistance = (
                float(vol) - (float(led_vol) * float(led_quant))
                ) / (float(led_cur) / 1000)
            if led_resistance < 0:
                self.ids.led_result.text = "Слишком малое напряжение \
                                            источника питания!"
                self.ids.led_res_power.text = ''
                self.ids.led_cur.text = ''
                self.ids.led_e24.text = ''
            else:
                self.ids.led_result.text = format_output_resistor(
                    led_resistance
                    )
                e24_result = e24.calculate_standard_resistor(
                    led_resistance, True
                    )
                self.ids.led_e24.text = format_output_resistor(
                    e24_result
                    )

                self.ids.led_res_power.text = "{:g} мВт".format(
                        (float(vol) - float(led_vol)) *
                        float(led_cur) * float(led_quant)
                        )
                self.ids.led_cur.text = "{:g} мА".format(
                    float(led_cur) * float(led_quant)
                    )
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

            induction = 0.0002 * math.pi * diameter * turns ** 2 * (
                math.log(
                    1 + math.pi / (2 * formfactor)
                    ) + 1 / (
                        2.3004 + 3.437 * formfactor + 1.7636 *
                        formfactor ** 2 -
                        0.47 / (0.755 + 1 / formfactor) ** 1.44
                        )
                )
            self.ids.induction.text = "{:g} мкГн".format(induction)
        except Exception:
            self.ids.induction.text = "Неверный ввод!"


class InductorCalculateSizeScreen(MDScreen):
    def inductor_calculate_turns(self, henrys, diameter, oneturn):
        try:
            henrys = float(henrys)
            diameter = float(diameter) / 10
            oneturn = float(oneturn) / 10
            inductor_length = (
                50 * oneturn ** 2 * henrys + math.sqrt(5) * math.sqrt(
                    500 * oneturn ** 4 * henrys ** 2 + 9 * oneturn ** 2
                    * diameter ** 3 * henrys
                    )
                ) / diameter ** 2

            inductor_turns = inductor_length / oneturn
            inductor_turns_int = round(inductor_turns, 0)
            inductor_length_int = inductor_turns_int * oneturn * 10

            self.ids.inductor_length.text = "{:g} мм".format(
                inductor_length * 10
                )
            self.ids.inductor_length_int.text = "{:g} мм".format(
                inductor_length_int
                )
            self.ids.inductor_turns.text = "{:g} витка(ов)".format(
                inductor_turns
                )
            self.ids.inductor_turns_int.text = "{:g} витка(ов)".format(
                inductor_turns_int
                )
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
        self.ids.par_res_box.ids[
            "resistor_input" + str(self.counter)
            ] = weakref.ref(resistor_input)

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
        self.ids.ser_cap_box.ids[
            "capacitor_input" + str(self.counter)
            ] = weakref.ref(capacitor_input)

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
                    self.ids.r2_calculated.text = "{:g} МОм".format(
                        r2 / 1000000
                        )

                self.ids.divider_rate_r.text = "{:g}".format(rate)

                e6_result = e24.calculate_standard_resistor(r2, False)
                if e6_result == 0:
                    self.ids.r2_e24.text = "0 Ом (перемычка)"
                elif e6_result < 1000:
                    self.ids.r2_e24.text = "{:g} Ом".format(e6_result)
                elif e6_result < 1000000:
                    self.ids.r2_e24.text = "{:g} кОм".format(e6_result / 1000)
                else:
                    self.ids.r2_e24.text = "{:g} МОм".format(
                        e6_result / 1000000
                        )

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
                self.ids.lm317_r2_output.text = """
                Ток нагрузки должен быть меньше 5А!
                """
                self.ids.lm317_r2_corrected_output.text = """
                Ток нагрузки должен быть меньше 5А!
                """
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
                self.ids.lm317_vout_output.text = "{:g} В".format(
                    vout_corrected
                    )
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
                        self.ids.lm317_vin_output_cur.text = """
                        Падение напряжения должно быть больше 2В и меньше 38В!
                        """
                        self.ids.lm317_vin_output_cur.font_size = "10sp"
                    else:
                        vin_corrected = vout + 3.7
                        self.ids.lm317_vin_output_cur.text = "{:g} В".format(
                            vin_corrected
                            )
                else:
                    self.ids.lm317_vin_output_cur.text = ""

                self.ids.lm317_r1_output_cur.text = result
                self.ids.lm317_r1_corrected_output_cur.text = result_corrected
                self.ids.lm317_r1_power_output_cur.text = "{:g} Вт".format(
                    power_r1
                    )
                self.ids.lm317_r1_power_corrected_output_cur.text = \
                    "{:g} Вт".format(power_corrected)
                self.ids.lm317_iout_corrected_output_cur.text = \
                    "{:g} А".format(iout_corrected)
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
            self.ids.lm317_r1_power_corrected_output_cur.text = \
                "Неверный ввод!"
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


class ChipsAnalogsScreen(MDScreen):
    pass


class ChipsAnalogs(MDGridLayout):
    series133 = {"133АГ1": "SN54121", "133ИД1": "SN54141", "133ИЕ4": "SN5492A",
                 "133ИЕ8": "SN5497", "133ИМ1": "SN5480", "133ИМ2": "SN5482",
                 "133ИМ3": "SN5483A", "133ИП2": "SN54180", "133ИР1": "SN5495",
                 "133ИР13": "SN54198", "Н133ИР13": "SN54198",
                 "133ИР17": "Am2504", "133КП1": "SN54150",
                 "133КП5": "SN54152", "133ЛА6": "SN5440", "133ЛА7": "SN5422",
                 "М133ЛА7": "SN5422", "133ЛА10": "SN5412", "133ЛЕ3": "SN5425",
                 "133ЛЕ5": "SN5428", "133ЛЕ6": "SN54128",
                 "133ЛИ5": "SN55451B", "133ЛН3": "SN5406", "133ЛН5": "SN5416",
                 "133ЛП7": "SN55450", "133ЛП9": "SN5407", "Н133ЛП9": "SN5407",
                 "133ТВ1": "SN5472", "Н133ТВ1": "SN5472", "133ТЛ1": "SN5413",
                 "М133ТМ2": "SN5474", "133ТМ5": "SN5477",
                 }

    series140 = {"140УД5А,Б": "CA3015", "КР140УД5А,Б": "CA3015",
                 "140УД6А,Б": "MG1556G", "КР140УД6": "MC1556C",
                 "140УД7": "μA741", "КР140УД7": "μA741C",
                 "КФ140УД7": "SFC2741", "Н140УД7": "SE535",
                 "140УД8А,Б": "μA740", "КР140УД8А-Г": "μA740C",
                 "140УД11": "LM318", "КР140УД11": "LM318", "140УД12": "μA776",
                 "КР140УД12": "μA776C", "140УД13": "μA727M",
                 "140УД14": "LM108", "КР140УД14А": "LM308",
                 "КР140УД14Б": "LM308", "140УД17А": "OP-07",
                 "140УД17Б": "OP-07A", "КР140УД17А": "OP-07E",
                 "КР140УД17Б": "OP-07C", "Н140УД17А": "OP-07",
                 "Н140УД17Б": "OP-07A", "КР140УД18": "LF355",
                 "140УД20А": "μA747", "140УД20Б": "μA747",
                 "КР140УД20А": "μA747C", "КР140УД20Б": "μA747C",
                 "КМ140УД20": "μA747C", "Н140УД20А": "μA747",
                 "Н140УД20Б": "μA747", "140УД21": "HA2900",
                 "КР140УД22": "LF356", "КР140УД22А": "LF356",
                 "140УД23": "LF157", "140УД24": "ICL7650",
                 "140УД25А": "OP-27A", "140УД25Б": "OP-27B",
                 "140УД25В": "OP-27C", "КР140УД25А": "OP-27A",
                 "КР140УД25Б": "OP-27B", "КР140УД25В": "OP-27C",
                 "КР140УД25Г": "OP-27B", "140УД26А": "OP-37A",
                 "140УД26Б": "OP-37B", "140УД26В": "OP-37C",
                 "КР140УД26А": "OP-37A", "КР140УД26Б": "OP-37B",
                 "КР140УД26В": "OP-37C", "КР140УД26Г": "OP-37B",
                 "140УД501А": "CA3015", "140УД501Б": "CA3015",
                 "140УД601А": "MC1556G", "140УД601Б": "MC1556G",
                 "КР140УД608": "MC1456CP1", "140УД701": "μA741",
                 "КР140УД708": "μA741C", "КР140УД1101": "LM318",
                 "140УД1201": "μA776", "КР140УД1208": "μA776C",
                 "140УД1301": "μA727M", "140УД1401": "LM108",
                 "КР140УД1408А": "LM308", "КР140УД1408Б": "LM308",
                 "140УД1701А": "OP-07", "140УД1701Б": "OP-07A"}

    series142 = {"142ЕН1А,Б": "μA723", "КР142ЕН1А-Г": "μA723",
                 "142ЕН2А,Б": "μA723", "КР142ЕН2А-Г": "μA723",
                 "142ЕН3": "μA78G", "КР142ЕН3": "μA78G", "142ЕН5А": "μA7805",
                 "142ЕН5Б": "μA7806", "142ЕН5В": "μA7805",
                 "142ЕН5Г": "μA7806", "142ЕН6А-Г": "LM125",
                 "КР142ЕН6": "SG3501A", "142ЕН8А": "μA7809",
                 "142ЕН8Б": "μA7812", "142ЕН8В": "μA7815",
                 "КР142ЕН8А": "μA7809", "КР142ЕН8Б": "μA7812C",
                 "КР142ЕН8В": "μA7815C", "КР142ЕН8Г": "μA7809",
                 "КР142ЕН8Д": "μA7812C", "КР142ЕН8Е": "μA7815C",
                 "КР142ЕН8Ж": "μA7815C", "КР142ЕН8И": "μA7815C",
                 "142ЕН9А": "μA7820", "142ЕН9Б": "μA7824",
                 "142ЕН9В": "μA7827", "КР142ЕН9А": "μA7820",
                 "КР142ЕН9Б": "μA7824C", "КР142ЕН9В": "μA7827",
                 "КР142ЕН9Г": "μA7820", "КР142ЕН9Д": "μA7824C",
                 "КР142ЕН9Е": "μA7827", "КР142ЕН9Ж": "μA7827",
                 "КР142ЕН9И": "μA7824C", "КР142ЕН9К": "μA7824C",
                 "142ЕН10": "μA79G", "КР142ЕН10": "μA79G", "142ЕП1": "LM100",
                 "КР142ЕП1А,Б": "LG200"}

    series153 = {"153УД5А,Б": "μA725", "153УД6": "LM107", "Н153УД6": "LM107",
                 "153УД501А": "μA725", "153УД501Б": "μA725",
                 "153УД601": "LM107"}

    series154 = {"154УД1А,Б": "HA2700", "КН154УД1Б,Б": "HA2700",
                 "КР154УД1А,Б": "HA2700", "Н154УД1А,Б": "HA2700",
                 "154УД2": "HA2530", "154УД3А,Б": "AD509S",
                 "КН154УД3А,Б": "AD509V", "КР154УД3А,Б": "AD509V",
                 "Н154УД3А": "AD509", "Н154УД3Б": "AD509S",
                 "154УД4А,Б": "HA2520", "КР154УД4А": "HA2520",
                 "КР154УД4Б": "HA2520"}

    series155 = {"155АГ1": "SN74121", "К155АГ1": "SN74121",
                 "155ИД1": "SN74141", "К155ИД1": "SN74141",
                 "КМ155ИД1": "SN74141", "155ИЕ4": "SN7492A",
                 "К155ИЕ4": "SN7492A", "КМ155ИЕ4": "SN7492A",
                 "155ИЕ8": "SN7497", "К155ИЕ8": "SN7497",
                 "КМ155ИЕ8": "SN7497", "155ИМ1": "SN7480",
                 "К155ИМ1": "SN7480", "155ИМ2": "SN7482", "155ИМ3": "SN7483A",
                 "К155ИМ3": "SN7483A", "155ИП2": "SN74180",
                 "К155ИП2": "SN74180", "КМ155ИП2": "SN74180",
                 "155ИР1": "SN7495", "К155ИР1": "SN7495",
                 "155ИР13": "SN74198", "К155ИР13": "SN74198",
                 "155ИР17": "AM2504", "К155ИР17": "AM2504",
                 "155КП1": "SN74150", "К155КП1": "SN74150",
                 "155КП2": "SN74153", "155КП5": "SN74152",
                 "К155КП5": "SN74152", "КМ155КП5": "SN74152",
                 "155ЛА6": "SN7440", "К155ЛА6": "SN7440",
                 "КМ155ЛА6": "SN7440", "155ЛА7": "SN7422",
                 "К155ЛА7": "SN7422", "155ЛА10": "SN7412",
                 "К155ЛА10": "SN7412", "К155ЛА10В": "SN7412",
                 "155ЛА18": "SN75452", "К155ЛА18": "SN75452",
                 "155ЛЕ3": "SN7425", "К155ЛЕ3": "SN7425",
                 "КМ155ЛЕ3": "SN7425", "155ЛЕ5": "SN7428",
                 "К155ЛЕ5": "SN7428", "155ЛЕ6": "SN74128",
                 "К155ЛЕ6": "SN74128", "155ЛИ5": "SN75451",
                 "К155ЛИ5": "SN75451", "155ЛЛ2": "SN75453",
                 "К155ЛЛ2": "SN75453", "155ЛН3": "SN7406",
                 "К155ЛН3": "SN7406", "К155ЛН3А,В": "SN7406",
                 "155ЛН5": "SN7416", "К155ЛН5": "SN7416",
                 "К155ЛН5А": "SN7416", "К155ЛН5В": "SN7416",
                 "К155ЛП4": "SN7417", "155ЛП7": "SN75450",
                 "К155ЛП7": "SN75450", "155ЛП9": "SN7407",
                 "К155ЛП9": "SN7407", "КМ155ЛП9": "SN7407",
                 "К155ЛП9А": "SN7407", "К155ЛП9В": "SN7407",
                 "К155РУ5": "F93410DC", "К155РУ7": "F93425APC",
                 "155ТВ1": "SN7472", "К155ТВ1": "SN7472",
                 "КМ155ТВ1": "SN7472", "155ТЛ1": "SN7413",
                 "К155ТЛ1": "SN7413", "155ТМ5": "SN7477",
                 "К155ТМ5": "SN7477"}

    series157 = {"К157ДА1": "-", "К157УД1": "μA759C", "К157УД2": "LM301",
                 "К157УД3": "-", "К157УЛ1А,Б": "-", "К157УН1А,Б": "-",
                 "К157УП1А,Б": "-", "К157УП2А,Б": "-", "К157ХА1А,Б": "-",
                 "К157ХА2": "-", "К157ХАЗ": "-", "К157ХП1": "-",
                 "К157ХП2": "-", "К157ХП3": "-", "КА157ХП3": "-",
                 "К157ХП4": "LM1894", "КИ157ХП4": "LM1894"}

    series169 = {"169АА1": "-", "169АА2": "SN55453", "169АА3": "SN55325",
                 "169АА4": "-", "169АА6": "SN463", "169АП1": "SN55110",
                 "169АП2": "SN55113", "169УЛ1": "-", "169УЛ2": "-",
                 "169УЛ4": "-", "169УЛ5": "-", "169УЛ6": "SN5522",
                 "169УЛ8": "-", "169УП1": "SN55107", "169УП2": "SN55154"}

    series170 = {"170АА1": "-", "К170АА1": "-", "170АА2": "SN75453",
                 "К170АА2": "SN75453", "170АА3": "SN75325",
                 "К170АА3": "SN75325", "170АА4": "-", "К170АА4": "-",
                 "170АА6": "-", "К170АА6": "-", "170АА7": "SN75327",
                 "К170АА7": "SN75327", "170АП1": "SN75110",
                 "К170АП1": "SN75110", "170АП2": "SN75154",
                 "К170АП2,2В": "SN75154", "170АП3": "MMH0026C",
                 "К170АП3,3В": "MMH0026C", "К170АП4": "3245", "170УЛ1": "-",
                 "К170УЛ1": "-", "170УЛ2": "-", "К170УЛ2": "-", "170УЛ4": "-",
                 "К170УЛ4": "-", "К170УЛ5": "-", "К170УЛ6": "SN7522",
                 "170УП1": "SN75107", "К170УП1,1В": "SN75107",
                 "170УП2": "SN75154", "К170УП2,2В": "SN75154"}

    series171 = {"171УВ1А,Б": "SL610", "171УВ2": "μA733", "171УВ3": "SL521C"}

    series174 = {"К174ГЛ1": "TDA1170S", "ЭК174ГЛ1": "TDA1170S",
                 "К174ГФ2": "XR2206", "К174КН1": "SAS560/570",
                 "К174КН2": "SAS580", "К174КП1": "TDA1029", "К174КП3": "-",
                 "174ПС1": "SO42P", "КМ174ПС1": "SO42P", "К174ПС1": "SO42P",
                 "КФ174ПС1": "SO42", "174ПС2": "-", "КМ174ПС2": "-",
                 "КН174ПС3": "-", "Н174ПС3": "-", "К174ПС4": "-",
                 "Н174ПС5": "-", "174УВ1": "SL550", "Н174УВ2": "SL1030",
                 "Н174УВ4": "SL531C", "К174УВ5": "NE592", "К174УН7": "TBA810S",
                 "ЭК174УН7": "TBA810S", "К174УН9": "TDA2003",
                 "К174УН10А": "TCA740", "К174УН10Б": "TCA740",
                 "К174УН12": "TCA730", "К174УН13": "TDA1002",
                 "К174УН14": "TDA2003", "КФ174УН17": "TA7688",
                 "К174УН18": "AN7145", "К174УН19": "TDA2030", "К174УН20": "-",
                 "К174УН21": "TDA7050", "К174УН22": "-", "КФ174УН23": "-",
                 "К174УН24": "TDA7052",
                 "К174УН25": "TDA2004", "К174УН26": "TDA7050",
                 "К174УН27": "TDA2005", "К174УН2101": "TDA7050",
                 "КФ174УН2301": "-", "К174УП1": "TBA970", "174УП2": "TL441CN",
                 "КМ174УП2": "TL441C", "К174УР3,3М": "TBA120",
                 "К174УР4": "TBA120U", "К174УР5": "TDA2541",
                 "174УР7": "TCA770", "К174УР7": "TCA770", "КМ174УР7": "TCA770",
                 "К174УР8": "TDA2545", "К174УР10": "SL1430",
                 "К174УР11": "TDA1236", "174ХА2": "TCA440",
                 "К174ХА2": "TCA440", "КМ174ХА2": "TCA440",
                 "К174ХА3А,Б": "LM1101", "К174ХА4": "NE561",
                 "К174ХА5": "TDA1047", "К174ХА6": "TDA1047", "174ХА7": "-",
                 "КМ174ХА7": "-", "К174ХА10": "TDA1083",
                 "КФ174ХА10": "TDA1083", "К174ХА11": "TDA2593",
                 "К174ХА11Ч": "TDA2593", "К174ХА14": "TDA4500",
                 "К174ХА15": "TDA1062", "К174ХА16": "TDA3520B",
                 "К174ХА17": "TDA3501", "174ХА18": "XR-215",
                 "К174ХА19": "TDA1093B", "К174ХА25": "TDA4610",
                 "К174ХА26": "MC3359", "К174ХА27": "TDA4565",
                 "К174ХА28": "TDA3510", "К174ХА31": "TDA3530",
                 "К174ХА32": "TDA4555", "К174ХА32А": "TDA4555",
                 "К174ХА33": "TDA3505", "К174ХА34": "TDA7021",
                 "КФ174ХА34": "TDA7021", "К174ХА35": "-",
                 "К174ХА36А": "TEA5570", "К174ХА36Б": "TEA5570",
                 "КФ174ХА37": "-", "К174ХА38А": "TDA8305A",
                 "К174ХА38Б": "TDA8305A", "К174ХА38В": "TDA8305A",
                 "К174ХА39": "TDA4502", "К174ХА41": "TDA3810",
                 "К174ХА42А": "TCA7000", "К174ХА42Б": "TCA7000",
                 "КМ174ХА201": "TCA440", "К174ХА3401": "TDA7021",
                 "К174ХА4201А": "TCA7000", "К174ХА4201Б": "TCA7000"}

    series175 = {"175ДА1": "-", "К175ДА1": "-", "175ПК1": "-",
                 "175УВ1А,Б": "SA-21", "175УВ2Б": "-", "175УВ3А,Б": "-",
                 "175УВ4": "CA3005", "Н175УВ4": "CA3005"}

    series176 = {"К176ИД2": "-", "К176ИД3": "-", "К176ИЕ1": "CD4024",
                 "К176ИЕ2": "TC5971", "К176ИЕ3": "HEF4017",
                 "К176ИЕ4": "CD4026E", "К176ИЕ5": "CD4033E",
                 "К176ИЕ12": "MM5368", "К176ИЕ13": "-", "К176ИЕ17": "-",
                 "К176ИЕ18": "-", "К176ИР3": "CD40115E", "К176ИР4": "CD4031E",
                 "К176ИР10": "CD4006E", "К176ЛИ1": "-", "К176ЛП1": "CD4007E",
                 "К176ЛИ11": "-", "К176ЛИ12": "-", "К176ЛП12": "-",
                 "К176ПУ1": "CD4010"}

    series193 = {"КС193ИЕ1": "SP8602A", "Н193ИЕ1": "SP8602A",
                 "С193ИЕ1": "SP8602A", "КС193ИЕ2": "SP8685A",
                 "Н193ИЕ2": "SP8685A", "С193ИЕ2": "SP8685A",
                 "КС193ИЕ3": "SP8690A", "Н193ИЕ3": "SP8690A",
                 "С193ИЕ3": "SP8690A", "КС193ИЕ4": "SP8655A",
                 "С193ИЕ4": "SP8655A", "С193ИЕ5А,Б": "SP8655A",
                 "КР193ИЕ6": "SP8772B", "КС193ИЕ7А,Б": "SP8611M",
                 "С193ИЕ7": "SP8612B", "КС193ПЦ1": "-", "Н193ПЦ3": "-",
                 "Н193ПЦ4А,Б": "-", "Н193ПЦ5": "SP8612B", "Н193ПЦ6": "SP8606"}

    series198 = {"198НТ1А,Б": "CA3086", "КР198НТ1А,Б": "CA3086",
                 "198НТ5А,Б": "-", "КР198НТ5А,Б": "-", "КР198НТ10": "-",
                 "КР198НТ11": "-", "КР198НТ12": "CA3050"}

    series249 = {"КР249КН2А-Г": "-", "КР249КН3А-Г": "-", "КР249КН4А-П": "-",
                 "КР249КН5А-П": "-", "КР249КН6А-П": "-", "КР249КН7А-Г": "-",
                 "КР249КН8А-Г": "-", "249КП1": "R5607", "249КП1А,Б": "R5607",
                 "К249КП1": "R5607", "К249КП2": "R5607", "249ЛП1А-В": "-",
                 "К249ЛП1А-Г": "-", "249ЛП4": "-", "249ЛП5": "-",
                 "249ЛП6А": "-", "249ЛП8": "-"}

    series427 = {"427ПА2": "DAC370-18", "427ПА3": "DAC377B-18",
                 "427ПА4": "DAC9377-16"}

    series490 = {"490ИП1": "-", "К490ИП1": "-", "490ИП2": "TIL308",
                 "К490ИП2": "TIL308", }

    series511 = {"К511ИД1": "H158", "К511ИЕ1": "H157", "К511ЛА1": "H102",
                 "К511ЛА2": "H103", "К511ЛА3": "H124", "К511ЛА4": "H104",
                 "К511ЛА5": "H122", "К511ЛИ1": "H109", "К511ПУ1": "H133",
                 "К511ПУ2": "H114", "К511ТВ1": "H110", }

    series512 = {"КА512ВИ1": "MC146818", "КР512ВИ1": "MC146818", "512ПС5": "-",
                 "512ПС6": "-", "К512ПС7Б": "KS5206", "512ПС8": "-",
                 "512ПС10": "-", "КР512ПС10": "MK5009", "512ПС11": "ICL7217",
                 "КР512ПС12": "ICM7227", "КА512ПС13А-Е": "-", "КР512ПС14": "-"}

    series514 = {"КР514АП1А,Б": "SAA1060", "514ИД1": "MSD047",
                 "КР514ИД1": "MSD047", "514ИД2": "MSD101",
                 "КР514ИД2": "MSD101", "514ИР2А,Б": "HDSP-2000",
                 "КР514КТ1": "-", "КР514КТ2": "-"}

    series521 = {"521СА1": "μA711", "Р521СА1": "μA711", "521СА2": "μA710",
                 "К521СА2": "μA710C", "Р521СА2": "μA710", "521СА3": "LM111",
                 "Н521СА3": "LM311J", "521СА4": "SE257K", "521СА5": "TL810",
                 "ЭК521СА5": "TL810", "521СА101": "μA711", "521СА201": "μA710",
                 "521СА301": "LM111", "521СА401": "SE527"}

    series522 = {"522КН1А,Б": "74C908", "522КН2А-В": "74C908"}

    series525 = {"525ПС1": "MC1595", "КР525ПС1А,Б": "MC1495",
                 "Н525ПС1": "MC1595", "525ПС2А-В": "AD530",
                 "КР525ПС2А,Б": "AD530", "525ПС3А,Б": "AD534S",
                 "КМ525ПС3А-Г": "AD534L", "Н525ПС4": "AD539S"}

    series526 = {"526ПС1": "MC1596", "526УР1": "TBA120", }

    series528 = {"528БР1": "-", "528БР2": "MN3001", "КА528БР2": "MN3001",
                 "М528БР3": "CCD321A-3", "М528БР5": "MS1001", "528ФВ1": "-",
                 "528ХК1": "CR-4", }

    series529 = {"529УП1": "TAA960"}

    series530 = {"530АП2": "SN54S216", "Н530АП2": "SN54S216",
                 "530АП3": "SN54S240", "530АП4": "SN54S241",
                 "530ГГ1": "SN54S124", "Н530ГГ1": "SN54S124",
                 "530ИД7": "SN54S134", "Н530ИД7": "SN54S134",
                 "530ИД14": "SN54S139", "Н530ИД14": "SN54S139",
                 "530ИЕ14": "SN54S196", "530ИЕ15": "SN54S197",
                 "530ИЕ16": "SN54S168", "Н530ИЕ16": "SN54S168",
                 "530ИЕ17": "SN54S169", "Н530ИЕ17": "SN54S169",
                 "530ИП3": "SN54S181", "Н530ИП3": "SN54S181",
                 "530ИП4": "SN54S182", "530ИП5": "SN54S280",
                 "530ИР11": "SN54S194", "530ИР12": "SN54S195",
                 "530ИР22": "SN54S373", "530ИР23": "SN54S374",
                 "530ИР24": "SN54S299", "530КП2": "SN54S153",
                 "Н530КП2": "SN54S153", "530КП7": "SN54S151",
                 "530КП11": "SN54S257", "М530КП11": "SN54S257",
                 "Н530КП11": "SN54S257", "530КП14": "SN54S258",
                 "Н530КП14": "SN54S258", "530КП15": "SN54S251",
                 "530ЛА1": "SN54S20", "Н530ЛА1": "SN54S20",
                 "М530ЛА2": "SN54S30", "Н530ЛА2": "SN54S30",
                 "530ЛА3": "SN54S00", "М530ЛА3": "SN54S00",
                 "Н530ЛА3": "SN54S00", "530ЛА4": "SN54S10",
                 "М530ЛА4": "SN54S10", "Н530ЛА4": "SN54S10",
                 "530ЛА9": "SN54S03", "Н530ЛА9": "SN54S03",
                 "530ЛА13": "SN54S38", "530ЛА16": "SN54S140",
                 "Н530ЛА16": "SN54S140", "530ЛА17": "-", "Н530ЛА17": "-",
                 "530ЛЕ1": "SN54S02", "Н530ЛЕ1": "SN54S02",
                 "М530ЛИ3": "SN54S08", "Н530ЛИ3": "SN54S08",
                 "530ЛЛ1": "SN54S32", "530ЛН1": "SN54S04",
                 "М530ЛН1": "SN54S04", "Н530ЛН1": "SN54S04",
                 "530ЛН2": "SN54S05", "М530ЛН2": "SN54S05",
                 "Н530ЛН2": "SN54S05", "М530ЛП5": "SN54S86",
                 "Н530ЛП5": "SN54S86", "530ЛР9": "SN54S64",
                 "М530ЛР9": "SN54S64", "530ЛР10": "SN54S65",
                 "530ЛР11": "SN54S51", "Н530ЛР11": "SN54S51",
                 "530ТВ9": "SN54S112", "М530ТВ9": "SN54S112",
                 "Н530ТВ9": "SN54S112", "530ТВ10": "SN54S113",
                 "Н530ТВ10": "SN54S113", "530ТЛ3": "SN54S132",
                 "530ТМ2": "SN54S74", "М530ТМ2": "SN54S74",
                 "Н530ТМ2": "SN54S74", "530ТМ8": "SN54S175",
                 "Н530ТМ8": "SN54S175", "530ТМ9": "SN54S174",
                 "Н530ТМ9": "SN54S174"}

    series531 = {"КР531АП2": "-", "КР531АП3": "SN74S240",
                 "КР531АП4": "SN74S241", "КР531ВА1": "SN74S226",
                 "КР531ГГ1": "SN74S124", "КР531ИД7": "SN74S138",
                 "Р531ИД7": "SN74S138", "КР531ИД14": "SN74S139",
                 "Р531ИД14": "SN74S139", "КР531ИЕ10": "SN74S161",
                 "КР531ИЕ11": "SN74S162", "КР531ИЕ14": "SN74S196",
                 "КР531ИЕ15": "SN74S197", "КР531ИЕ16": "SN74S168",
                 "КР531ИЕ17": "SN74S169", "КР531ИЕ18": "SN74S163",
                 "КС531ИК1": "AM25S05", "КС531ИК2": "SN74S381",
                 "КР531ИП3": "SN74S181", "КР531ИП4": "SN74S182",
                 "КР531ИП5": "SN74S280", "КР531ИП10": "AM93S48RC",
                 "КР531ИР11": "SN74S194", "КР531ИР12": "SN74S195",
                 "КС531ИР18": "AM25S07", "КС531ИР19": "AM25S08",
                 "КС531ИР20": "AM25S09", "КР531ИР21": "AM25S010",
                 "КС531ИР21": "AM25S010", "КР531ИР22": "SN74S373",
                 "КР531ИР23": "SN74S374", "КР531ИР24": "SN74S299",
                 "КР531КП2": "SN74S153", "КР531КП7": "SN74S151",
                 "Р531КП7": "SN74S151", "КР531КП11": "SN74S257",
                 "КР531КП12": "SN74S253", "КР531КП14": "SN74S258",
                 "КР531КП15": "SN74S251", "КР531КП16": "SN74S157",
                 "КР531КП18": "SN74S158", "КР531ЛА1": "SN74S20",
                 "КР531ЛА2": "SN74S30", "КР531ЛА3": "SN74S00",
                 "КР531ЛА4": "SN74S10", "КР531ЛА7": "SN74S22",
                 "КР531ЛА9": "SN74S03", "Р531ЛА9": "SN74S03",
                 "КС531ЛА12": "SN74S37", "КР531ЛА13": "SN74S38",
                 "КР531ЛА16": "SN74S140", "КР531ЛА17": "-",
                 "КР531ЛА19": "SN74S139", "Р531ЛА19": "SN74S139",
                 "КР531ЛЕ1": "SN74S02", "Р531ЛЕ1": "SN74S02",
                 "КР531ЛЕ7": "SN74S260", "Р531ЛЕ7": "SN74S260",
                 "КС531ЛИ1": "SN74S08", "КР531ЛИ3": "SN74S11",
                 "КР531ЛН1": "SN74S04", "Р531ЛН1": "SN74S04",
                 "КР531ЛН2": "SN74S05", "Р531ЛН2": "SN74S05",
                 "КР531ЛП5": "SN74S86", "КР531ЛР9": "SN74S64",
                 "КР531ЛР10": "SN74S65", "КР531ЛР11": "SN74S51",
                 "КР531РУ8": "SN74S189", "КР531РУ9": "SN74S289",
                 "КР531РУ10": "SN74S225", "КР531РУ11": "DM85S68",
                 "КР531СП1": "SN74S85", "КР531ТВ9": "SN74S175",
                 "КР531ТВ10": "SN74S113", "КР531ТВ11": "SN74S114",
                 "КР531ТЛ3": "SN74S132", "КР531ТМ2": "SN74S74",
                 "Р531ТМ2": "SN74S74", "КР531ТМ8": "SN74S175",
                 "Р531ТМ8": "SN74S175", "КР531ТМ9": "SN74S174",
                 "Р531ТМ9": "SN74S174", "КР531ХЛ1": "-"}

    series533 = {"533АГ3": "SN54LS123", "М533АГ3": "SN54LS123",
                 "Н533АГ3": "SN54LS123", "533АГ4": "SN54LS221",
                 "Н533АГ4": "SN54LS221", "533АП3": "SN54LS240",
                 "Н533АП3": "SN54LS240", "533АП4": "SN54LS241",
                 "Н533АП4": "SN54LS241", "533АП5": "SN54LS244",
                 "Н533АП5": "SN54LS244", "533АП6": "SN54LS245",
                 "Н533АП6": "SN54LS245", "533ВЖ1": "SN54LS630",
                 "533ИВ1": "SN54LS148", "М533ИВ1": "SN54LS148",
                 "533ИВ2": "SN54LS348", "533ИВ3": "SN54LS147", "533ИД3": "-",
                 "533ИД4": "SN54LS155", "М533ИД4": "SN54LS155",
                 "Н533ИД4": "SN54LS155", "533ИД5": "SN54LS156",
                 "Н533ИД5": "SN54LS156", "533ИД6": "SN54LS42",
                 "533ИД7": "SN54LS138", "533ИД10": "SN54LS145",
                 "Н533ИД10": "SN54LS145", "533ИД18": "SN54LS247",
                 "Н533ИД18": "SN54LS247", "533ИД19": "-", "533ИЕ5": "SN54LS93",
                 "533ИЕ6": "SN54LS192", "533ИЕ7": "SN54LS193",
                 "533ИЕ9": "SN54LS160A", "533ИЕ10": "SN54LS161A",
                 "М533ИЕ10": "SN54LS161A", "Н533ИЕ10": "SN54LS161A",
                 "533ИЕ13": "SN54LS191", "533ИЕ14": "SN54LS196",
                 "533ИЕ15": "SN54LS197", "533ИЕ17": "SN54LS169A",
                 "533ИЕ19": "SN54LS393", "Н533ИЕ19": "SN54LS393",
                 "533ИЕ20": "SN54LS390", "533ИК4": "SN54LS281",
                 "533ИМ5": "SN54LS183", "Н533ИМ5": "SN54LS183",
                 "533ИМ6": "SN54LS283", "Н533ИМ6": "SN54LS283",
                 "533ИМ7": "SN54LS385", "533ИП3": "SN54LS181",
                 "Н533ИП3": "SN54LS181", "533ИП4": "SN54LS182",
                 "533ИП5": "SN54LS280", "533ИП6": "SN54LS242",
                 "М533ИП6": "SN54LS242", "Н533ИП6": "SN54LS242",
                 "533ИП7": "SN54LS243", "М533ИП7": "SN54LS243",
                 "Н533ИП7": "SN54LS243", "533ИП8": "SN54LS261",
                 "533ИП9": "SN54LS384", "533ИП12": "-", "533ИП13": "-",
                 "533ИР8": "SN54LS164", "Н533ИР8": "SN54LS164",
                 "533ИР9": "SN54LS165", "Н533ИР9": "SN54LS165",
                 "533ИР10": "SN54LS166", "Н533ИР10": "SN54LS166",
                 "533ИР11А": "SN54LS194", "М533ИР11А": "SN54LS194",
                 "533ИР15": "SN54LS173", "Н533ИР15": "SN54LS173",
                 "533ИР16": "SN54LS295", "533ИР22": "SN54LS373",
                 "533ИР23": "SN54LS374", "М533ИР23": "SN54LS374",
                 "Н533ИР23": "SN54LS374", "533ИР25": "SN54LS395",
                 "533ИР26": "SN54LS670", "Н533ИР26": "SN54LS670",
                 "533ИР27": "SN54LS377", "533ИР28": "SN54LS322",
                 "533ИР29": "SN54LS323", "533ИР30": "SN54LS259",
                 "533ИР32": "SN54LS170", "533ИР35": "SN54LS273",
                 "533КП2": "SN54LS153", "533КП7": "SN54LS151",
                 "533КП11": "SN54LS257", "533КП11А": "SN54LS257B",
                 "533КП12": "SN54LS253", "533КП13": "SN54LS298",
                 "533КП14": "SN54LS258", "533КП14А": "SN54LS258B",
                 "533КП15": "SN54LS251", "Н533КП15": "SN54LS251",
                 "533КП16": "SN54LS157", "533КП17": "SN54LS353",
                 "533ЛА1": "SN54LS20", "М533ЛА1": "SN54LS20",
                 "Н533ЛА1": "SN54LS20", "533ЛА2": "SN54LS30",
                 "М533ЛА2": "SN54LS30", "Н533ЛА2": "SN54LS30",
                 "533ЛА3": "SN54LS00", "М533ЛА3": "SN54LS00",
                 "Н533ЛА3": "SN54LS00", "533ЛА4": "SN54LS10",
                 "М533ЛА4": "SN54LS10", "Н533ЛА4": "SN54LS10",
                 "533ЛА6": "SN54LS40", "533ЛА7": "SN54LS22",
                 "533ЛА9": "SN54LS03", "М533ЛА9": "SN54LS03",
                 "Н533ЛА9": "SN54LS03", "533ЛА10": "SN54LS12",
                 "Н533ЛА10": "SN54LS12", "533ЛА12": "SN54LS37",
                 "М533ЛА12": "SN54LS37", "Н533ЛА12": "SN54LS37",
                 "533ЛА13": "SN54LS38", "Н533ЛА13": "SN54LS38",
                 "533ЛЕ1": "SN54LS02", "Н533ЛЕ1": "SN54LS02",
                 "М533ЛЕ1": "SN54LS02", "533ЛЕ4": "SN54LS27",
                 "М533ЛЕ4": "SN54LS27", "Н533ЛЕ4": "SN54LS27",
                 "533ЛИ1": "SN54LS08", "М533ЛИ1": "SN54LS08",
                 "Н533ЛИ1": "SN54LS08", "533ЛИ2": "SN54LS09",
                 "М533ЛИ2": "SN54LS09", "533ЛИ3": "SN54LS11",
                 "М533ЛИ3": "SN54LS11", "Н533ЛИ3": "SN54LS11",
                 "533ЛИ6": "SN54LS21", "М533ЛИ6": "SN54LS21",
                 "Н533ЛИ6": "SN54LS21", "533ЛЛ1": "SN54LS32",
                 "Н533ЛЛ1": "SN54LS32", "М533ЛЛ1": "SN54LS32",
                 "533ЛН1": "SN54LS04", "М533ЛН1": "SN54LS04",
                 "Н533ЛН1": "SN54LS04", "533ЛН2": "SN54LS05",
                 "М533ЛН2": "SN54LS05", "Н533ЛН2": "SN54LS05",
                 "533ЛП3": "-", "Н533ЛП3": "-", "533ЛП5": "SN54LS86",
                 "М533ЛП5": "SN54LS86", "Н533ЛЛ5": "SN54LS86",
                 "533ЛП8": "SN54LS125", "533ЛР4": "SN54LS55",
                 "М533ЛР4": "SN54LS55", "533ЛР11": "SN54LS51",
                 "М533ЛР11": "SN54LS51", "Н533ЛР11": "SN54LS51",
                 "533ЛР13": "SN54LS54", "Н533ЛР13": "SN54LS54",
                 "533СП1": "SN54LS85", "533ТВ6": "SN54LS107",
                 "Н533ТВ6": "SN54LS107", "533ТВ9": "SN54LS112",
                 "533ТЛ2": "SN54LS14", "М533ТЛ2": "SN54LS14",
                 "Н533ТЛ2": "SN54LS14", "533ТМ2": "SN54LS74",
                 "М533ТМ2": "SN54LS74", "Н533ТМ2": "SN54LS74",
                 "533ТМ7": "SN54LS75", "М533ТМ7": "SN54LS75",
                 "533ТМ8": "SN54LS175", "М533ТМ8": "SN54LS175",
                 "Н533ТМ8": "SN54LS175", "533ТМ9": "SN54LS174",
                 "М533ТМ9": "SN54LS174", "Н533ТМ9": "SN54LS174",
                 "533ТР2": "SN54LS279", "Н533ТР2": "SN54LS279",
                 "533ХП1": "-"}

    series537 = {"537РП1": "IDT7203-80", "КИ537РУ1А": "HM6508IDE",
                 "537РУ2А": "HM6504-3", "537РУ2Б": "TC5504P",
                 "КР537РУ2А": "HM6504-3", "Н537РУ2А": "HM6504-3",
                 "537РУ3А,Б": "HM6504-5", "537РУ6А,Б": "HM6504B-2",
                 "537РУ8А": "TC5516", "537РУ8Б": "MSM5128",
                 "КР537РУ8А": "HM6117", "Н537РУ8А": "HM6117",
                 "537РУ9А,Б": "HM6116", "КР537РУ9А,Б": "HM6116",
                 "Н537РУ9А": "HM6116", "КА537РУ10": "HM6516",
                 "КА537РУ10А,Б": "-", "КР537РУ10": "TC5517",
                 "537РУ13": "HM6148P", "КР537РУ13": "TC5514AC",
                 "КР537РУ13А": "TC5514AD", "КР537РУ14": "HM6147P",
                 "КР537РУ14А": "TC5514AD", "КР537РУ14Б": "TC5514AD",
                 "537РУ14А": "TC5514AD", "537РУ14Б": "TC5514AD",
                 "Н537РУ14А": "TC5514AD", "537РУ16А": "HM6264-15",
                 "537РУ16Б": "HM6264", "Н537РУ16А": "HM6264",
                 "Н537РУ16Б": "HM6264", "КР537РУ17": "MB8464-15",
                 "КР537РУ17А-Д": "MB8464", "537РУ18": "HM6117",
                 "КР537РУ18": "HM6117P", "537РУ19А": "HM6287",
                 "537РУ19Б": "HM6287", "КР537РУ19А": "μPD4361C-70",
                 "КР537РУ19Б": "μPD4361", "Н537РУ19А": "HM6287",
                 "Н537РУ19Б": "HM6287", "КР537РУ23А": "HM6264A",
                 "КР537РУ23Б": "μPD4364C", "КР537РУ24А": "IDT6116L-45",
                 "КР537РУ24Б": "IDT6116L", "КР537РУ25А": "CYT6116-55",
                 "КР537РУ25Б": "CYT6116", "КР537РУ25В": "CYT6116",
                 "537РУ29": "IDT7132-70"}

    series538 = {"538УН1А,Б": "LM381", "538УН3": "LM387",
                 "КР538УН3А,Б": "LM387"}

    series541 = {"541РЕ1": "RC82S290N", "541РТ1": "M3601", "541РТ2": "M3636",
                 "541РУ1": "SN54S401", "541РУ1А": "93471M",
                 "541РУ1К,Л": "93471M", "КР541РУ1": "SN74S401",
                 "КР541РУ1А": "93471C", "541РУ2": "-", "541РУ2А": "-",
                 "541РУ2Б": "MBM2149-45", "КР541РУ2": "IM7147L-3",
                 "КР541РУ2А": "D2114AL-1", "541РУ2К": "-", "541РУ2Л": "-",
                 "541РУ4": "SN54S400", "541РУ5": "-"}

    series543 = {"543КН1": "AY5-4016", "543КН2": "DG506", "543КН3": "DG201"}

    series544 = {"544УД1А,Б": "μA740", "КР544УД1А,Б": "μA740C",
                 "544УД2А,Б": "CA3130", "КР544УД2А-Г": "CA3130",
                 "КР544УД3А,Б": "-", "КР544УД4": "-", "КР544УД5А,Б": "-"}

    series548 = {"К548УН1А,Б": "LM381", "КФ548ХА1": "-", "КФ548ХА2": "-"}

    series551 = {"КР551УД1А,Б": "μA725B", "КР551УД2А,Б": "TBA931"}

    series553 = {"К553УД1А,Б": "μA709C", "К553УД2": "LM201",
                 "К553УД6": "LM207", "К553УД101А": "μA709C",
                 "К553УД101В": "μA709C", "К553УД201": "LM201",
                 "К553УД601": "LM207"}

    series554 = {"К554СА1": "μA711C", "К554СА2": "μA710C", "Р554СА2": "μA710",
                 "К554СА3А": "LM311", "К554СА3Б": "LM311", "Р554СА3": "LM111",
                 "Р554СА3А": "LM111", "К554СА4": "SF527N", "К554СА6": "MAL319",
                 "К554СА201": "μA710C", "К554СА301А": "LM311",
                 "К554СА301Б": "LM311"}

    series555 = {"К555АГ3": "SN74LS123", "КМ555АГ3": "SN74LS123",
                 "К555АГ3В": "SN74LS123", "К555АГ4": "SN74LS221",
                 "КМ555АГ4": "SN74LS221", "КР555АГ4": "SN74LS221",
                 "К555АГ5": "96LS02", "К555АП3": "SN74LS240",
                 "К555АП4": "SN74LS241", "К555АП5": "SN74LS244",
                 "К555АП6": "SN74LS245", "К555АП10": "SN74LS646",
                 "555ВЖ1": "SN74LS630", "К555ВЖ1": "SN74LS630",
                 "К555ИВ1": "SN74LS148", "КМ555ИВ1": "SN74LS148",
                 "К555ИВ2": "SN74LS348", "К555ИВ3": "SN74LS147",
                 "555ИД4": "SN74LS155", "К555ИД4": "SN74LS155",
                 "К555ИД5": "SN74LS156", "К555ИД6": "SN74LS42",
                 "КМ555ИД6": "SN74LS42", "555ИД7": "SN74LS138",
                 "К555ИД7": "SN74LS138", "К555ИД7А": "SN74LS138",
                 "К555ИД10": "SN74LS145", "КМ555ИД10": "SN74LS145",
                 "К555ИД10В": "SN74LS145", "К555ИД18": "SN74LS247",
                 "КМ555ИД18": "SN74LS247", "К555ИЕ2": "SN74LS90",
                 "К555ИЕ5": "SN74LS93", "555ИЕ6": "SN74LS192",
                 "К555ИЕ6": "SN74LS192", "К555ИЕ7": "SN74LS193",
                 "КМ555ИЕ9": "SN74LS160", "К555ИЕ10": "SN74LS161",
                 "КМ555ИЕ10": "SN74LS161", "К555ИЕ13": "SN74LS191",
                 "К555ИЕ14": "SN74LS196", "К555ИЕ15": "SN74LS197",
                 "К555ИЕ17": "SN74LS169A", "КМ555ИЕ17": "SN74LS169A",
                 "К555ИЕ18": "SN74LS163", "К555ИЕ19": "SN74LS393",
                 "КМ555ИЕ19": "SN74LS393", "КР555ИЕ19": "SN74LS393",
                 "К555ИЕ20": "SN74LS290", "КМ555ИЕ20": "SN74LS290",
                 "К555ИК4": "SN74LS281", "К555ИМ5": "SN74LS183",
                 "555ИМ6": "SN74LS283", "К555ИМ6": "SN74LS283",
                 "К555ИМ7": "SN74LS35", "К555ИП3": "SN74LS181",
                 "555ИП5": "SN74LS280", "К555ИП5": "SN74LS280",
                 "К555ИП6": "SN74LS242", "КМ555ИП6": "SN74LS242",
                 "К555ИП7": "SN74LS243", "КМ555ИП7": "SN74LS243",
                 "К555ИП8": "SN74LS261", "К555ИП9": "SN74LS384",
                 "К555ИР8": "SN74LS164", "К555ИР9": "SN74LS165",
                 "КМ555ИР9": "SN74LS165", "К555ИР9В": "SN74LS165",
                 "К555ИР10": "SN74LS166", "КМ555ИР10": "SN74LS166",
                 "К555ИР10В": "SN74LS166", "555ИР11А": "SN74LS194A",
                 "К555ИР11А": "SN74LS194A", "КМ555ИР11А": "SN74LS194A",
                 "К555ИР15": "SN74LS173", "КМ555ИР15": "SN74LS173",
                 "555ИР16": "SN74LS295", "К555ИР16": "SN74LS295",
                 "К555ИР22": "SN74LS373", "К555ИР23": "SN74LS374",
                 "К555ИР26": "SN74LS670", "К555ИР26В": "SN74LS670",
                 "КМ555ИР26": "SN74LS670", "К555ИР27": "SN74LS377",
                 "К555ИР30": "SN74LS259", "К555ИР32": "SN74LS170",
                 "КМ555ИР32": "SN74LS170", "К555ИР35": "SN74LS273",
                 "555КП2": "SN74LS153", "К555КП2": "SN74LS153",
                 "555КП7": "SN74LS151", "К555КП7": "SN74LS151",
                 "555КП11": "SN74LS257", "К555КП11": "SN74LS257",
                 "К555КП11А": "SN74LS257", "К555КП11Б": "SN74LS257",
                 "555КП12": "SN74LS253", "К555КП12": "SN74LS253",
                 "555КП13": "SN74LS298", "К555КП13": "SN74LS298",
                 "555КП14": "SN74LS258", "К555КП14": "SN74LS258",
                 "К555КП14А": "SN74LS258", "555КП15": "SN74LS251",
                 "К555КП15": "SN74LS251", "КМ555КП15": "SN74LS251",
                 "555КП16": "SN74LS157", "К555КП16": "SN74LS157",
                 "К555КП17": "SN74LS353", "КМ555КП17": "SN74LS353",
                 "К555КП18": "SN74LS158", "КМ555КП18": "SN74LS158",
                 "К555КП20": "SN74LS399", "КМ555КП20": "SN74LS399",
                 "555ЛА1": "SN74LS20", "К555ЛА1": "SN74LS20",
                 "КМ555ЛА1": "SN74LS20", "555ЛА2": "SN74LS30",
                 "К555ЛА2": "SN74LS30", "КМ555ЛА2": "SN74LS30",
                 "555ЛА3": "SN74LS00", "К555ЛА3": "SN74LS00",
                 "КМ555ЛА3": "SN74LS00", "К555ЛА4": "SN74LS10",
                 "К555ЛА6": "SN74LS40", "555ЛА7": "SN74LS22",
                 "К555ЛА7": "SN74LS22", "555ЛА9": "SN74LS03",
                 "К555ЛА9": "SN74LS03", "КМ555ЛА9": "SN74LS03",
                 "К555ЛА10": "SN74LS12", "К555ЛА11": "SN74LS26",
                 "КМ555ЛА11": "SN74LS26", "555ЛА12": "SN74LS37",
                 "К555ЛА12": "SN74LS37", "КМ555ЛА12": "SN74LS37",
                 "К555ЛА12В": "SN74LS37", "555ЛА13": "SN74LS38",
                 "К555ЛА13": "SN74LS38", "КМ555ЛА13": "SN74LS38",
                 "К555ЛА13В": "SN74LS38", "555ЛЕ1": "SN74LS02",
                 "К555ЛЕ1": "SN74LS02", "555ЛЕ4": "SN74LS27",
                 "К555ЛЕ4": "SN74LS27", "К555ЛЕ4В": "SN74LS27",
                 "КМ555ЛЕ4": "SN74LS27", "555ЛИ1": "SN74LS08",
                 "К555ЛИ1": "SN74LS08", "КМ555ЛИ1": "SN74LS08",
                 "КС555ЛИ1": "SN74LS08", "К555ЛИ2": "SN74LS09",
                 "555ЛИ3": "SN74LS11", "К555ЛИ3": "SN74LS11",
                 "КМ555ЛИ3": "SN74LS11", "К555ЛИ3В": "SN74LS11",
                 "555ЛИ4": "SN74LS15", "К555ЛИ4": "SN74LS15",
                 "КМ555ЛИ4": "SN74LS15", "555ЛИ6": "SN74LS21",
                 "К555ЛИ6": "SN74LS21", "КМ555ЛИ6": "SN74LS21",
                 "555ЛЛ1": "SN74LS32", "К555ЛЛ1": "SN74LS32",
                 "555ЛН1": "SN74LS04", "К555ЛН1": "SN74LS04",
                 "КМ555ЛН1": "SN74LS04", "555ЛН2": "SN74LS05",
                 "К555ЛН2": "SN74LS05", "КМ555ЛН2": "SN74LS05",
                 "К555ЛН2В": "SN74LS05", "555ЛП5": "SN74LS86",
                 "К555ЛП5": "SN74LS86", "КМ555ЛП5": "SN74LS86",
                 "К555ЛП5В": "SN74LS86", "555ЛП8": "SN74LS125",
                 "К555ЛП8": "SN74LS125", "555ЛП12": "SN74LS136",
                 "К555ЛП12": "SN74LS136", "КМ555ЛП12": "SN74LS136",
                 "К555ЛП14": "SN74LS126A", "555ЛР4": "SN74LS55",
                 "К555ЛР4": "SN74LS55", "555ЛР11": "SN74LS51",
                 "К555ЛР11": "SN74LS51", "К555ЛР13": "SN74LS54",
                 "КМ555ЛР13": "SN74LS54", "К555ПЦ1": "SN74LS292",
                 "К555РЕ4": "5275-1", "555СП1": "SN74LS85",
                 "К555СП1": "SN74LS85", "555ТВ6": "SN74LS107",
                 "К555ТВ6": "SN74LS107", "К555ТВ9": "SN74LS112",
                 "555ТЛ2": "SN74LS14", "К555ТЛ2": "SN74LS14",
                 "КМ555ТЛ2": "SN74LS14", "К555ТЛ2В": "SN74LS14",
                 "555ТМ2": "SN74LS74", "К555ТМ2": "SN74LS74",
                 "КМ555ТМ2": "SN74LS74", "КС555ТМ2": "SN74LS74",
                 "К555ТМ2В": "SN74LS74", "К555ТМ7": "SN74LS75",
                 "555ТМ8": "SN74LS175", "К555ТМ8": "SN74LS175",
                 "КМ555ТМ8": "SN74LS175", "КС555ТМ8": "SN74LS175",
                 "К555ТМ8В": "SN74LS175", "555ТМ9": "SN74LS174",
                 "К555ТМ9": "SN74LS174", "КМ555ТМ9": "SN74LS174",
                 "555ТР2": "SN74LS279", "К555ТР2": "SN74LS279",
                 "КМ555ТР2": "SN74LS279"}

    series556 = {"И556АП1": "-", "556РТ1": "S82S101", "КР556РТ1": "N82S101",
                 "Р556РТ1": "MC82S101M", "556РТ2": "S82S100",
                 "КР556РТ2": "N82S100", "М556РТ2": "N82S100",
                 "Р556РТ2": "N82S100", "556РТ3": "-", "556РТ4": "3601",
                 "Р556РТ4": "3601", "556РТ4А": "3601", "КР556РТ4А": "3601",
                 "Р556РТ4А": "3601", "556РТ5": "3604", "КР556РТ5": "3604",
                 "М556РТ5": "3604", "Р556РТ5": "3604", "556РТ6А": "DM87S190",
                 "КР556РТ6А": "DM87S190", "М556РТ6А": "DM87S190",
                 "Р556РТ6А": "DM87S190", "556РТ7А": "N82S191",
                 "КР556РТ7А": "N82S191", "М556РТ7А": "N82S191",
                 "Р556РТ7А": "N82S191", "КР556РТ9А": "N82S1281",
                 "КР556РТ9Б": "N82S1281", "556РТ10": "-",
                 "КР556РТ11": "93427C", "КР556РТ12": "N82S136",
                 "КР556РТ13": "N82S137", "КР556РТ14": "DM87S184",
                 "КР556РТ15": "DM87S185", "КР556РТ17": "3624A",
                 "КР556РТ20": "AM27S35C", "КР556РТ131": "AM27S33AC",
                 "556РТ161": "N82HS641", "КР556РТ161": "N82HS641",
                 "М556РТ161": "N82HS641", "Р556РТ161": "N82HS641"}

    series558 = {"558РР2А,Б": "HN48016", "КС558РР2А,Б": "HN48016",
                 "КМ558РР4А,Б": "IMS3630", "КС558РР4А,Б": "IMS3630",
                 "КС558ХП1": "MN9106", "КР558ХП2": "SAA1075",
                 "КР558ХП3": "PCF8582AP"}

    series559 = {"КР559ВН1": "DC003", "КР559ВТ1": "DC004", "559ИП1": "DS3881",
                 "К559ИП1": "DS3881", "КМ559ИП1": "DS3881",
                 "КН559ИП1": "DS3881", "КР559ИП1": "DS3881",
                 "М559ИП1": "DS3881", "559ИП2": "DS8640", "К559ИП2": "DS8640",
                 "КМ559ИП2": "DS8640", "КН559ИП2": "DS8640",
                 "КР559ИП2": "DS8640", "М559ИП2": "DS8640", "559ИП3": "DS7641",
                 "К559ИП3": "DS7641", "КМ559ИП3": "DS7641",
                 "КН559ИП3": "DS7641", "КР559ИП3": "DS8641",
                 "М559ИП3": "DS7641", "559ИП4": "8T23", "К559ИП4": "8T23",
                 "КР559ИП4": "8T23", "Р559ИП4": "8T23", "559ИП5": "8T24",
                 "К559ИП5": "8T24", "559ИП6": "MC3440", "К559ИП6": "MC3440",
                 "КР559ИП6": "MC3440", "Р559ИП6": "MC3440", "КР559ИП7": "8T24",
                 "Р559ИП7": "8T24", "КР559ИП8": "DC005", "КР559ИП9": "DS7640",
                 "КР559ИП10": "DS7641", "КН559ИП11": "AM26LS32A",
                 "КР559ИП11": "AM26LS32A", "КН559ИП12": "AM26LS31",
                 "КР559ИП12": "AM26LS31", "КР559ИП13": "DP8307",
                 "КР559ИП14": "DP8308", "КР559ИП19": "MC1488",
                 "КР559ИП20": "MC1489", "КР559СК1": "DC102P",
                 "КР559СК2": "DM8136"}

    series561 = {"К561ИД1": "CD4048A", "К561ИД4": "CD4055A",
                 "К561ИД5": "CD4056A", "К561ИЕ8": "CD4017A",
                 "561ИЕ9": "CD4022A", "К561ИЕ9": "CD4022A",
                 "К561ИЕ9А": "CD4022A", "561ИЕ10": "MC14520A",
                 "К561ИЕ10": "MC14520A", "К561ИЕ10А": "MC14520A",
                 "К561ИЕ11": "MC14516A", "К561ИЕ14": "CD4029A",
                 "К561ИЕ16": "CD4020A", "К561ИЕ19": "CD4018A",
                 "К561ИК1": "CD4053A", "К561ИМ1": "CD4008A",
                 "К561ИП2": "MC14585A", "К561ИП2А": "MC14585A",
                 "К561ИП5": "MC14554CP", "К561ИП5А": "MC14554CP",
                 "К561ИР2": "CD4015A", "К561ИР6": "CD4034A",
                 "К561ИР6А": "CD4034A", "561ИР9": "CD4035A",
                 "К561ИР9": "CD4035A", "К561ИР11": "CD4036A",
                 "К561ИР11А": "CD4036A", "К561ИР12": "MC14580A",
                 "К561ИР12А": "MC14580A", "К561КП1": "CD4052A",
                 "К561КП2": "CD4051A", "К561КТ3": "CD4066A",
                 "К561КТ3А": "CD4066A", "561ЛА7": "CD4011A",
                 "К561ЛА7": "CD4011A", "561ЛА8": "CD4012A",
                 "К561ЛА8": "CD4012A", "К561ЛА9": "CD4023A",
                 "К561ЛА9А": "CD4023A", "К561ЛЕ5": "CD4001",
                 "К561ЛЕ5А": "CD4001", "К561ЛЕ6": "CD4002A",
                 "К561ЛЕ6А": "CD4002A", "К561ЛЕ10": "CD4025A",
                 "К561ЛЕ10А": "CD4025A", "561ЛН1": "MC14502A",
                 "К561ЛН1": "MC14502A", "К561ЛН1А": "MC14502A",
                 "561ЛН2": "CD4049A", "К561ЛН2": "CD4049A",
                 "К561ЛН3": "MC14503", "К561ЛП2": "CD4030A",
                 "К561ЛП2А": "CD4030A", "561ЛП13": "-", "К561ЛП13": "-",
                 "К561ЛС2": "CD4019A", "К561ЛС2А": "CD4019A",
                 "К561ПУ4": "CD4050A", "К561ПУ4A": "CD4050A", "К561ПУ7": "-",
                 "К561ПУ8": "-", "К561РУ2А": "CD4061", "К561РУ2Б": "CD4061A",
                 "К561РУ2В": "CD4061A", "К561СА1": "MC14531A",
                 "К561СА1А": "MC14531A", "К561ТВ1": "CD4028A",
                 "К561ТВ1А": "CD4028A", "К561ТЛ1": "CD4093A",
                 "К561ТЛ1А": "CD4093A", "561ТМ2": "CD4013A",
                 "К561ТМ2": "CD4013A", "К561ТМ3": "CD4042A",
                 "561ТР2": "CD4043A", "К561ТР2": "CD4043A",
                 "К561ТР2А": "CD4043A", "К561УМ1": "CD4054A"}

    series563 = {"563РЕ1": "SMM2364", "К563РЕ1": "SMM2364",
                 "Н563РЕ1": "SMM2364", "563РЕ2А,Б": "SCM23C256-1",
                 "563РЕ2Б": "SCM23C256-1", "Н563РЕ2А,Б": "SCM23C256-1",
                 "КР563РЕ3": "TMS0351"}

    series564 = {"564АГ1": "CD4098A", "564АГ1B": "CD4098B",
                 "564ГГ1": "CD4046A", "564ИД1,1B": "CD4028A",
                 "КР564ИД1B": "CD4028A", "564ИД4": "CD4055A",
                 "564ИД4B": "CD4055A", "564ИД5": "CD4056A",
                 "564ИД5B": "CD4056A", "564ИЕ9": "CD4022A",
                 "564ИЕ9B": "CD4022A", "564ИЕ10": "MC14520A",
                 "564ИЕ10B": "MC14520A", "564ИЕ11,B": "MC14516A",
                 "КР564ИЕ11B": "MC14516A", "564ИЕ14": "CD4029A",
                 "564ИЕ14B": "CD4029B", "КР564ИЕ14B": "CD4029B",
                 "564ИЕ15": "CD4059A", "564ИЕ15B": "CD4059B",
                 "КР564ИЕ15B": "CD4059B", "564ИЕ19": "CD4018A",
                 "КР564ИЕ19B": "CD4018", "564ИЕ22": "MC14553A",
                 "564ИК1,1B": "CD4053A", "КР564ИК1B": "CD4053A",
                 "564ИК2,2B": "-", "564ИМ1,1B": "CD4008A",
                 "564ИП2": "MC14585A", "564ИП2B": "MC14585A",
                 "564ИП3": "MC14581A", "564ИП3B": "MC14581",
                 "КР564ИП3B": "MC14581", "564ИП4": "MC14582A",
                 "564ИП4B": "MC14582A", "КР564ИП4B": "MC14582A",
                 "564ИП5": "MC14554A", "564ИП5B": "MC14554A",
                 "564ИП6": "CD40101B", "564ИР1,1B": "CD4006A",
                 "КР564ИР1B": "CD4006A", "КФ564ИР1B": "CD4006A",
                 "564ИР2,2B": "CD4015A", "КР564ИР2B": "CD4015A",
                 "564ИР6": "CD4034A", "564ИР6B": "CD4034B",
                 "564ИР9,9B": "CD4035A", "КР564ИР9B": "CD4035A",
                 "564ИР11": "CD4036A", "564ИР11B": "CD4036A",
                 "564ИР12": "MC14580A", "564ИР12B": "MC14580A",
                 "564ИР13": "MM54C905", "564ИР13B": "MM54C905",
                 "КР564ИР13B": "MM54C905", "КФ564ИР13B": "MM54C905",
                 "564ИР16": "CD40105B", "564КП1": "CD4052A",
                 "564КП1B": "CD4052", "КР564КП1B": "CD4052",
                 "564КП2": "CD4051A", "564КП2B": "CD4051A",
                 "КР564КП2B": "CD4051A", "564КТ3": "CD4093A",
                 "564КТ3B": "CD4093A", "564ЛА7,7B": "CD4011A",
                 "КР564ЛА7B": "CD4011A", "564ЛА8,8B": "CD4012A",
                 "КР564ЛА8B": "CD4012A", "564ЛА9,9B": "CD4023A",
                 "К564ЛА9B": "CD4023A", "564ЛА10,B": "CD40107B",
                 "КР564ЛА10B": "CD40107B", "564ЛЕ5": "CD4001A",
                 "564ЛЕ5B": "CD4001A", "564ЛЕ6": "CD4002A",
                 "564ЛЕ6B": "CD4002A", "564ЛЕ10": "CD4025A",
                 "564ЛЕ10B": "CD4025A", "564ЛН1": "MC14502A",
                 "564ЛН1B": "MC14502A", "564ЛН2": "CD4049A",
                 "564ЛН2B": "CD4049A", "КР564ЛН2B": "CD4049A",
                 "564ЛП2": "CD4030A", "564ЛП2B": "CD4030A", "564ЛП13": "-",
                 "564ЛП13B": "-", "КР564ЛП13B": "-", "564ЛС1": "-",
                 "КР564ЛС1B": "-", "564ЛС2": "CD4019A", "564ЛС2B": "CD4019A",
                 "564ПР1": "CD4094A", "564ПУ4": "CD4050A",
                 "564ПУ4B": "CD4050A", "564ПУ6": "CD40109A", "564ПУ7": "-",
                 "КР564ПУ7B": "-", "564ПУ8": "-", "КР564ПУ8": "-",
                 "564ПУ9": "CD40116A", "564РП1": "CD4039A",
                 "564РУ2А-В": "CD4061A", "564СА1": "MC14531B",
                 "564СА1B": "MC14531B", "564ТВ1": "CD4027A",
                 "564ТВ1B": "CD4027A", "564ТЛ1": "CD4093A",
                 "564ТЛ1B": "CD4093A", "564ТМ2,2B": "CD4013A",
                 "КР564ТМ2B": "CD4013A", "564ТМ3": "CD4042A",
                 "564ТМ3B": "CD4042A", "564ТР2": "CD4043A",
                 "564ТР2B": "CD4043A", "564УМ1": "CD4054A",
                 "564УМ1B": "CD4054A"}

    series565 = {"565РУ3А-Г": "MK4116P", "КР565РУ5Б-Д": "MK4164",
                 "565РУ5В,Г": "MK4164", "Р565РУ5В-Д": "MK4164N-15",
                 "Р565РУ6В-Д": "2118", "КР565РУ6Б-Д": "2118",
                 "КР565РУ7В,Г": "HM50257", "КР565РУ7Д": "HM50257",
                 "КР565РУ7Д1": "HM50257", "КР565РУ7Д2": "HM50257",
                 "КР565РУ8А-Г": "MB81256", "КР565РУ9В": "μPD411000",
                 "КР565РУ9Г": "μPD411000", "КР565РУ9Д": "μPD411000",
                 "КР565РУ14А-В": "-"}

    series568 = {"568РЕ1": "EA8316BD1"}

    series571 = {"571ХЛ1": "-", "571ХЛ2": "-", "571ХЛ3": "-",
                 "571ХЛ4": "SN54LS368A", "КР571ХЛ4А": "SN54LS368",
                 "571ХЛ5": "SN54LS368", "КР571ХЛ5А": "SN54LS367A",
                 "571ХЛ6": "-", "571ХЛ7": "SN74LS367"}

    series572 = {"572ПА1А": "AD7520KD", "572ПА1Б": "AD7520JD",
                 "572ПА1В": "AD7520JD", "К572ПА1А": "AD7520KN",
                 "К572ПА1Б": "AD7520JN", "КР572ПА1А,Б": "AD7520KN",
                 "Н572ПА1А": "AD7520K", "Н572ПА1Б": "AD7520J",
                 "Н572ПА1В": "AD7520J", "572ПА2А,Б": "AD7541",
                 "К572ПА2А-В": "AD7541", "КР572ПА2А-В": "AD7541",
                 "572ПВ1А,Б": "AD7570", "К572ПВ1А-В": "AD7570",
                 "КР572ПВ1А-В": "AD7570", "КР572ПВ2А-В": "ICL7107",
                 "КР572ПВ3": "AD7574", "Н572ПВ3": "AD7574", "572ПВ4": "AD7574",
                 "КР572ПВ5": "ICL7106", "572ПВ6": "ICL7135"}

    series573 = {"КР573РЕ2": "MM5216", "КС573РЕ4А,Б": "2364",
                 "КР573РЕ6": "2364", "КС573РТ4А,Б": "2764", "КР573РТ5": "2716",
                 "КР573РТ6": "2764", "573РФ2": "2716", "КС573РФ2": "2716",
                 "С573РФ2": "2716", "573РФ4А,Б": "2764", "КС573РФ4А,Б": "2764",
                 "КС573РФ5": "2716", "КМ573РФ8А": "D27256-3",
                 "КМ573РФ8Б,В": "D27256", "573РФ10": "M8755A",
                 "КМ573РФ10": "M8755A", "КМ573РФ81А-В": "27128",
                 "КС573РФ81А-В": "27128", "КМ573РФ82А-В": "27128",
                 "КС573РФ82А-В": "27128", "КМ573ХЛ1": "EP900"}

    series574 = {"574УД1А-В": "μA740", "КР574УД1А-В": "μA740",
                 "574УД2А-Г": "TL083", "КР574УД2А-Д": "TL083",
                 "КР574УД3": "LF251", "574УД3А-В": "LF157",
                 "574УД4А,Б": "TL081"}

    series580 = {"КР580ВА86": "8286", "КР580ВА87": "8287", "580ВВ51": "8251",
                 "КР580ВВ51А": "8251A", "580ВВ55": "8255",
                 "КР580ВВ55А": "8255A", "580ВВ79": "8279",
                 "КР580ВВ79": "8279", "КР580ВГ18": "8218",
                 "КР580ВГ75": "8275", "КР580ВГ92": "8292",
                 "580ВИ53": "8253", "КР580ВИ53": "8253", "КР580ВК28": "8228",
                 "КР580ВК38": "8238", "КР580ВК91А": "8291", "580ВМ80": "8280",
                 "КР580ВМ80А": "8280", "КР580ВР43": "8243",
                 "КР580ВТ42": "8242", "580ВТ57": "8257", "КР580ВТ57": "8257",
                 "КР580ГФ24": "8224", "КР580ИР82": "8282",
                 "КР580ИР83": "8283"}

    series585 = {"585АП16": "3216", "Н585АП16": "3216", "585АП26": "3226",
                 "Н585АП26": "3226", "585ИК01": "3201", "585ИК02": "3202",
                 "585ИК03": "3203", "585ИК14": "3214", "Н585ИК14": "3214",
                 "585ИР12": "3212", "Н585ИР12": "3212"}

    series588 = {"588ВА1,1A": "CP82C86", "Н588ВА1,1A": "CP82C86",
                 "Н588ВА1А": "CP82C86", "КР588ВА1": "CP82C86", "588ВА2": "-",
                 "588ВА3": "-", "КР588ВА4": "COM78804", "КА588ВА5": "-",
                 "588ВГ1": "-", "588ВГ1А,В": "-", "КА588ВГ1": "-",
                 "КР588ВГ1": "-", "Н588ВГ1А,В": "-", "588ВГ2": "-",
                 "КР588ВГ2": "-", "Н588ВГ2": "-", "588ВГ3": "-",
                 "Н588ВГ3": "-", "588ВГ4": "-", "Н588ВГ4": "-", "588ВГ5": "-",
                 "Н588ВГ5": "-", "588ВГ6": "-", "Н588ВГ6": "-", "588ВИ1": "-",
                 "Н588ВИ1": "-", "588ВН1": "-", "Н588ВН1": "-",
                 "588ВР2": "CDP1855", "КР588ВР2": "-", "Н588ВР2": "-",
                 "588ВР2А,В": "-", "КР588ВР2А": "-", "Н588ВР2А,В": "-",
                 "588ВС2А-В": "-", "КА588ВС2А": "-", "КР588ВС2А,Б": "-",
                 "Н588ВС2А-В": "-", "588ВТ1": "-", "КР588ВТ1": "-",
                 "Н588ВТ1": "-", "588ВТ2": "-", "Н588ВТ2": "-",
                 "588ВУ2А-В": "-", "КР588ВУ2А,Б": "-", "Н588ВУ2А-В": "-",
                 "588ИР1": "CP82C82", "КР588ИР1": "-", "Н588ИР1": "-",
                 "588ИР2": "-"}

    series589 = {"589АП16": "3216", "К589АП16": "3216", "КМ589АП16": "3216",
                 "589АП26": "3226", "К589АП26": "3226", "КМ589АП26": "3226",
                 "588ВГ4": "-", "Н588ВГ3": "-", "Н588ВГ4": "-",
                 "589ИК01": "3001", "К589ИК01": "3001", "589ИК02": "3002",
                 "К589ИК02": "3002", "589ИК03": "3003", "К589ИК03": "3003",
                 "589ИК14": "3214", "К589ИК14": "3214", "589ИР12": "3212",
                 "К589ИР12": "3212", "К589ХЛ4": "-"}

    series590 = {"590ИР1": "MT8571", "КР590ИР1": "MT8571", "590КН1": "3708",
                 "А590КН1": "3708", "КА590КН1": "3708", "КР590КН1": "3708",
                 "590КН2": "HI1800", "А590КН2": "HI1800", "КА590КН2": "HI1800",
                 "КР590КН2": "HI1800", "590КН3": "HI509A",
                 "КН590КН3": "HI509A", "КР590КН3": "HI509A",
                 "Н590КН3": "HI509A", "590КН4": "HI5043", "А590КН4": "HI5043",
                 "КА590КН4": "HI5043", "КН590КН4": "HI5043",
                 "КР590КН4": "HI5043", "Н590КН4": "HI5043", "590КН5": "HI201",
                 "А590КН5": "HI201", "КА590КН5": "HI201", "КН590КН5": "HI201",
                 "КР590КН5": "HI201", "Н590КН5": "HI201", "590КН6": "HI508A",
                 "КН590КН6": "HI508A", "КР590КН6": "HI508A",
                 "Н590КН6": "HI508A", "590КН7": "HI5046", "КН590КН7": "HI5046",
                 "КР590КН7": "HI5046", "Н590КН7": "HI5046",
                 "590КН8А": "SD5000", "КН590КН8А": "SD5000",
                 "КР590КН8А": "SD5000", "Н590КН8А": "SD5000",
                 "590КН8Б": "SD5200", "КН590КН8Б": "SD5200",
                 "КР590КН8Б": "SD5200", "Н590КН8Б": "SD5200",
                 "590КН9": "HI5048A", "КН590КН9": "HI5048A",
                 "КР590КН9": "HI5048A", "Н590КН9": "HI5048A",
                 "590КН10": "DG202", "КР590КН10": "DG202",
                 "590КН12": "AD7591D1", "590КН13": "HI401",
                 "КН590КН13": "HI401", "КР590КН13": "HI401",
                 "Н590КН13": "HI401", "590КН14": "CD22100", "590КН17": "HI524",
                 "590КН19": "HI508AL", "Н590КН20": "-", "КН590КН20": "-",
                 "КН590КН22": "-", "КР590КН23": "-", "Н590КН24": "-",
                 "590КН25": "-", "590КН26": "-", "КН590КН27": "MT8816",
                 "КФ590КН27": "MT8816", "590КТ1": "AD7519",
                 "КН590КТ1": "AD7519", "КР590КТ1": "AD7519",
                 "Н590КТ1": "AD7519"}

    series591 = {"591КН1": "MEM5116", "Н591КН1": "MEM5116", "591КН2": "HI506",
                 "Н591КН2": "HI506", "591КН3": "HI507", "Н591КН3": "HI507",
                 "591КН4": "CD22102", "Н591КН5": "CD22102"}

    series593 = {"593БР1": "TAD32"}

    series594 = {"594ПА1": "AD562", "К594ПА1": "AD562"}

    series597 = {"597СА1А,Б": "AM685", "КР597СА1": "AM685",
                 "КС597СА1": "AM685", "Н597СА1": "AM685", "597СА2А,Б": "AM686",
                 "КР597СА2": "AM686", "КС597СА2": "AM686", "Н597СА2": "AM686",
                 "597СА3А,Б": "LM119", "КР597СА3А,Б": "ICB8001C",
                 "КС597СА3А,Б": "ICB8001C", "КР597СА4А,Б": "UC7695",
                 "КС597СА4А,Б": "UC7695"}

    series1002 = {"1002ИР1": "CD40105BE", "КА1002ИР1": "CD40105BE",
                  "КР1002ИП1": "-", "КР1002ИП2": "-", "КМ1002КП1": "CFF26303",
                  "1002ПР1": "-", "КР1002ПР1": "-", "1002ПР2": "CDP1871A",
                  "1002ХЛ1": "TR1602", "КР1002ХЛ1": "TR1602",
                  "КР1002ХЛ2": "HD970040D"}

    series1004 = {"КР1004ХЛ6": "TC8208AF9K", "КА1004ХЛ20": "-"}

    series1005 = {"КР1005ВЕ1": "-", "КР1005ВИ1": "-", "КР1005ПС1": "AN6371",
                  "КР1005ПЦ1А,Б": "M54819L", "КР1005ПЦ2": "AN6342",
                  "КР1005ПЦ4": "AN6345", "КР1005УД1": "AN6551",
                  "КР1005УЛ1А,В": "AN6320", "КР1005УН1А,Б": "AN262",
                  "КМ1005УР1А,Б": "AN304", "КР1005ХА1": "AN6341",
                  "КР1005ХА2": "AN6350", "КС1005ХА2": "AN6350",
                  "КР1005ХА3": "AN6677", "КР1005ХА4": "AN6310",
                  "КР1005ХА5": "AN6332", "КР1005ХА6": "AN6360",
                  "КР1005ХА7": "AN6362"}

    series1006 = {"КР1006ВИ1": "NE555", "КР1006ВИ1А": "NE555",
                  "КФ1006ВИ1": "NE555", "М1006ВИ1": "SE555"}

    series1008 = {"КМ1008ВЖ1": "AY5-9151", "КР1008ВЖ1": "AY5-9151",
                  "КР1008ВЖ2": "S2562", "КР1008ВЖ3": "SAA6002",
                  "КР1008ВЖ4": "S2561", "КР1008ВЖ5А,Б": "S25610",
                  "КР1008ВЖ6": "S7230A/B", "КР1008ВЖ7А,Б": "PCD3325A",
                  "КР1008ВЖ8": "-", "КР1008РЕ1": "-"}

    series1009 = {"1009ЕН2А-Г": "AD584"}

    series1014 = {"КР1014КТ1А-В": "UN2410"}

    series1015 = {"КФ1015ПЛ1": "NJ88C30", "КР1015ХК2А,Б": "μPD2819C"}

    series1016 = {"КР1016БР1": "MN3011", "КР1016ВИ1": "-",
                  "КР1016ПУ1": "XR2277", "КА1016ХЛ1": "-"}

    series1017 = {"КР1017ХА1": "AD301"}

    series1019 = {"1019ЕМ1": "LM135", "К1019ЕМ1": "LM235",
                  "К1019ЕМ1А": "LM235"}

    series1021 = {"КР1021УР1": "TDA3541", "КР1021ХА1А,Б": "TDA2582",
                  "КР1021ХА2": "TDA2578A", "КР1021ХА3,3М": "TDA3591",
                  "КР1021ХА4": "TDA3562A", "КР1021ХА6": "SAA5231",
                  "КР1021ХА8А": "TDA3562Q", "КР1021ХА8Б": "TDA3562Q",
                  "КР1021ХА9": "-"}

    series1022 = {"КР1022ЕП1": "AN6616"}

    series1023 = {"КР1023ХА1А-Г": "M51721L", "КР1023ХА2А": "M51721L"}

    series1025 = {"КС1025КП2": "M51750P"}

    series1026 = {"КМ1026УН1": "ZN470", "КР1026УН1": "ZN470"}

    series1027 = {"КС1027ХА1": "M51720P"}

    series1031 = {"КР1031ХА1": "MC3479P"}

    series1032 = {"КФ1032УД1": "TAB1042"}

    series1033 = {"К1033ЕУ1": "TDA4600", "КР1033ЕУ2": "TDA4605",
                  "КР1033ЕУ5А,Б": "TDA4605", "КР1033ЕУ8": "ML4812"}

    series1038 = {"КР1038ХП1": "LS156"}

    series1039 = {"КР1039ХА1": "TDA4503", "КР1039ХА2": "TDA8305"}

    series1040 = {"КР1040ПД1": "SAB3013", "КР1040СА1": "LM393DP",
                  "КР1040УД1": "LM358", "К1040УД2": "LM272",
                  "КР1040ХЛ1": "TDA3791"}

    series1043 = {"КР1043ВГ1": "TMS3763-28", "КР1043ВГ101": "TMS3763",
                  "КР1043ХА1": "AN3792", "КР1043ХА2": "MN6178",
                  "КР1043ХА3": "AN3795", "КР1043ХА4": "TDA5660P",
                  "КР1043ХА5": "AN6387", "К1043ХА6": "-",
                  "КР1043ХА7": "AN640G", "КР1043ХА8": "TDA3724",
                  "КР1043ХА9": "TDA3730", "КР1043ХА10": "TDA3740",
                  "КР1043ХА11": "TDA3755", "КР1043ХА12": "TDA3760"}

    series1051 = {"КР1051БР1": "-", "К1051КН1": "-", "КС1051КН2": "SAS580",
                  "КР1051ПА1": "TDA8444", "К1051УН1": "TDA1519B",
                  "К1051УН2": "TDA1519A", "КР1051УР1": "TDA4443",
                  "КР1051УР2": "TDA4445", "КР1051УР3": "TDA2557",
                  "КР1051УР4": "TDA8341", "КР1051ХА1": "TDA3654Q",
                  "КР1051ХА2": "SDA3202", "КС1051ХА4": "TDA8443A",
                  "КС1051ХА5": "TDA8440", "КР1051ХА6А,Б": "TDA3047",
                  "КФ1051ХА6А,Б": "TDA3047", "КР1051ХА7": "TDA5030",
                  "КР1051ХА8": "TDA8442", "КР1051ХА11": "TDA5030",
                  "КР1051ХА12": "TDA3566", "КР1051ХА13": "TDA4510",
                  "КР1051ХА15": "TDA6600", "КР1051ХА16": "TDA5330T",
                  "КР1051ХА17": "TDA2579A", "КР1051ХА18": "TDA4650",
                  "КР1051ХА19": "TDA8143", "КР1051ХА27": "TDA3654A",
                  "КР1051ХК1": "TDA8432", "КР1051ХК2": "TEA2029C",
                  "КР1051ХК4": "TDA4660", "КР1051ХЛ1": "MAS1008"}

    series1053 = {"КФ1053СА1": "AN6914S", "КФ1053СА2": "AN6912S",
                  "КФ1053УД1": "NJM4556", "КФ1053УД2": "AN6562S",
                  "КФ1053УД3": "NJN2902M", "КФ1053ХА2": "μPC1514G"}

    series1054 = {"КР1054ВГ1": "-", "КР1054ВП1": "-", "КР1054ГП1": "BA7004",
                  "КР1054РР1": "MN1220", "КР1054УИ1А": "TBA2800",
                  "КФ1054УЛ1": "AN3311S", "КР1054УН1": "TDA7050",
                  "КР1054УР1": "AN3224K", "К1054ХА1": "LA7051",
                  "КС1054ХА3": "TBA2800", "КС1054ХА4": "TEA2014A",
                  "К1054ХП1": "μPC1490HA"}

    series1055 = {"КР1055ХП1": "L497"}

    series1056 = {"КР1056УП1": "TBA2800", "КР1056ХЛ1": "IRT1260"}

    series1057 = {"КР1057ХА1А,Б": "LM1818", "КР1057ХП1": "CX20027"}

    series1058 = {"КР1058ФП1А,Б": "MC5156"}

    series1064 = {"КМ1064ВЖ5А,Б": "-", "КР1064ВЖ5А,Б": "-",
                  "КМ1064ВЖ7А,Б": "PCD3325A", "КР1064ВЖ7А,Б": "PCD3325A",
                  "КР1064КТ1А-Г": "UN2410", "КР1064ПП1": "MA6520",
                  "КМ1064УН1": "TEA1067", "КР1064УН1": "TEA1067",
                  "КР1064УН2": "MC34119"}

    series1066 = {"КС1066ХА1": "TDA7000", "КР1066ХА2": "MC3361",
                  "КС1066ХА2": "MC3361", "КФ1066ХА2": "MC3361"}

    series1071 = {"КР1071ХА1": "-", "КР1071ХА2": "TDA7021"}

    series1072 = {"КР1072ХА1": "TDA5030"}

    series1075 = {"КР1075УЛ1": "TA7784P/Z", "КР1075УЛ2": "BA3516"}

    series1082 = {"КР1082ПП1": "-", "КР1082ХА1": "CX10054",
                  "КФ1082ХА1": "CX10054", "КР1082ХА2": "AN7230",
                  "КФ1082ХА2": "AN7230", "КР1082ХА3": "AN7400",
                  "КФ1082ХА3": "AN7400", "КФ1082ХА4": "UAA2033T"}

    series1084 = {"КР1084УИ1": "TBA2800"}

    series1086 = {"КР1086ХА1": "SAY115"}

    series1087 = {"ЭКР1087ХА1": "TDA4565", "ЭКР1087ХА2": "TDA3505",
                  "ЭКР1087ХА3": "TDA4555", "КА1087ХА4": "-",
                  "ЭКР1087ХА5": "TDA3827", "КР1087ХА6": "TDA4504"}

    series1091 = {"КР1091ГП1": "L3240"}

    series1100 = {"1100СК2А,Б": "LF398", "К1100СК2": "LF398",
                  "КР1100СК2": "LF398", "КР1100СК3,3А": "-", "1100СК4А,Б": "-",
                  "КФ1100СК4А-В": "-", "КФ1100СК5А,Б": "-"}

    series1102 = {"1102АП2": "SN75113", "К1102АП2,2В": "SN75113",
                  "К1102АП3": "DS8831", "К1102АП4": "SN75454",
                  "К1102АП5": "SN75430N", "К1102АП6": "SN75431N",
                  "К1102АП7": "SN75432N", "К1102АП8": "SN75433N",
                  "К1102АП9": "SN75434N", "К1102АП10": "SN75460N",
                  "К1102АП11": "SN75461N", "К1102АП12": "SN75462N",
                  "К1102АП13": "SN75463N", "К1102АП14": "SN75464N",
                  "К1102АП15": "9636A", "К1102АП15А": "9636A",
                  "КР1102АП15": "9636A", "К1102АП16": "9638RC",
                  "КР1102АП16": "9638RC", "К1102ВА1": "8T37",
                  "К1102ИП1": "MC3450", "К1102ИП2": "MC3453",
                  "К1102ЛП1": "9637A", "КР1102ЛП1": "9637A"}

    series1103 = {"1103СК1А,Б": "SHC803"}

    series1107 = {"1107ПВ1": "TDC1014J", "К1107ПВ1А,Б": "TDC1014J",
                  "1107ПВ2А,Б": "TDC1007J", "К1107ПВ2А-В": "TDC1007J",
                  "1107ПВ3А": "SDA5010", "1107ПВ3Б": "SDA6020",
                  "КР1107ПВ3А": "SDA5010", "КР1107ПВ3Б": "SDA6020",
                  "КР1107ПВ5А,Б": "SDA5200", "1107ПВ6": "TDC1019J"}

    series1108 = {"1108ПА1А,Б": "HI562", "К1108ПА1А,Б": "HI562",
                  "Н1108ПА1А,Б": "HI562", "Н1108ПА2": "AD558",
                  "1108ПА3": "MC1506", "1108ПВ1А,Б": "TDC1013J",
                  "К1108ПВ1А,Б": "TDC1013J", "Н1108ПВ1А,Б": "TDC1013J",
                  "1108ПВ2": "AM6112", "К1108ПВ2": "AM6112",
                  "1108ПП1": "VFC32KP", "К1108ПП1": "VFC32KP",
                  "КР1108ПП1": "VFC32KP"}

    series1109 = {"К1109КН1А,Б": "MB941", "К1109КН2": "DI510",
                  "1109КН4": "SN75427", "К1109КН4А,Б": "SN75427",
                  "1109КН5": "MB491", "К1109КТ1А,Б": "DI210",
                  "К1109КТ2": "ULN2001A", "К1109КТ3": "ULN2074B",
                  "1109КТ4А,Б": "UDN2845B", "К1109КТ4А,Б": "UDN2841B",
                  "1109КТ5": "-", "1109КТ7": "-", "1109КТ8": "-",
                  "1109КТ9": "DD420", "К1109КТ21": "ULN2002A",
                  "К1109КТ22": "ULN2003A", "К1109КТ23": "ULN2004A",
                  "К1109КТ24": "ULN2005A", "К1109КТ25": "-"}

    series1113 = {"1113ПВ1А-В": "AD571S", "К1113ПВ1А-В": "AD571K"}

    series1114 = {"1114ЕУ1": "MC3420", "К1114ЕУ1А,Б": "SC1526",
                  "1114ЕУ3": "TL494", "К1114ЕУ3": "TL494",
                  "КР1114ЕУ4": "TL494", "КР1114ЕП1": "TL7702"}

    series1116 = {"К1116КП1": "RAFIH-JC-30", "К1116КП2": "-",
                  "К1116КП3": "IAV2A", "К1116КП4": "DN838",
                  "1116КП6": "SAS241", "1116КП7": "X79115AV",
                  "1116КП8": "UGS3030T", "К1116КП8": "UGS3030T",
                  "К1116КП9": "UGN3013U", "К1116КП10": "UGN3040",
                  "К1116КП11": "UGN3076T", "К1116КП14": "UGN3030"}

    series1118 = {"КС1118ПА1": "MC10318L", "С1118ПА1Б": "MC10318L",
                  "КМ1118ПА2А,Б": "TDC1016J-10", "М1118ПА2А,Б": "TDC1016J-10",
                  "КР1118ПА3": "SP9768", "М1118ПА3А,Б": "SP9768",
                  "КС1118ПА6А,Б": "-"}

    series1121 = {"1121СА1": "MC3430", "К1121СА1": "MC3430"}

    series1125 = {"КР1125КП3А-В": "4E20-28"}

    series1128 = {"КР1128КТ3А,Б": "L293D"}

    series1146 = {"КР1146ФП1": "MK5912", "КР1146ФП2": "2912",
                  "КС1146ФП2": "2912"}

    series1152 = {"КР1152УК1": "HAH533", "КР1152ХА1": "HA11235"}

    series1156 = {"КР1156ЕУ1": "MC3506"}

    series1157 = {"КР1157ЕН5А-Г": "78L05", "КР1157ЕН9А-Г": "78L09",
                  "КР1157ЕН12А-Г": "78L12", "КР1157ЕН15А-Г": "78L15"}

    series1162 = {"КР1162ЕН5А,Б": "μA7905", "КР1162ЕН6А,Б": "μA7906",
                  "КР1162ЕН8А,Б": "μA7908", "КР1162ЕН9А,Б": "μA7909",
                  "КР1162ЕН10А,Б": "μA7910", "КР1162ЕН12А,Б": "μA7912",
                  "КР1162ЕН15А,Б": "μA7915", "КР1162ЕН18А,Б": "μA7918",
                  "КР1162ЕН24А,Б": "μA7924", "КР1162ЕН27А,Б": "μA7927"}

    series1167 = {"КР1167КП1А-В": "4E20-28"}

    series1183 = {"КР1183ЕН5А,Б": "μA7905", "КР1183ЕН6А,Б": "μA7906",
                  "КР1183ЕН8А,Б": "μA7908", "КР1183ЕН9А,Б": "μA7909",
                  "КР1183ЕН12А,Б": "μA7912", "КР1183ЕН15А,Б": "μA7915",
                  "КР1183ЕН18А,Б": "μA7918", "КР1183ЕН20А,Б": "μA7920",
                  "КР1183ЕН24А,Б": "μA7924", "КР1183ЕН27А,Б": "μA7927"}

    series1401 = {"1401СА1": "LM139", "К1401СА3": "LM393",
                  "К1401УД1": "LM2900", "1401УД2А,Б": "LM124D",
                  "К1401УД2А,Б": "LM324", "Н1401УД2А": "LM124",
                  "К1401УД3": "LM246", "1401УД4": "μAF-774BM",
                  "К1401УД4": "MCLP-347", "К1401УД6": "LM392"}

    series1407 = {"1407УД1А,Б": "EK41", "КР1407УД1": "EK41",
                  "КФ1407УД1": "EK41", "КР1407УД2,2А": "LM4250",
                  "1407УД3": "EK41", "КР1407УД3": "EK41"}

    series1408 = {"1408УД1": "LM143", "КР1408УД1": "LM343"}

    series1409 = {"КР1409УД1А-Г": "CA3140"}

    series1413 = {"1413УК1": "-", "КР1413УК2": "SSI101A", "1413УК3": "SSI116"}

    series1420 = {"Н1420УД1": "NE5539"}

    series1422 = {"К1422УД1": "μA791"}

    series1423 = {"К1423УД1": "ICL7612", "1423УД2А-В": "ICL7621",
                  "КМ1423УД4А,Б": "TLC27M41"}

    series1426 = {"КР1426УД1": "NIM2043"}

    series1433 = {"1433УД1": "HA5190"}

    series1435 = {"КР1435УД2": "LM324", "КР1435УД3": "LM346"}

    series1436 = {"ЭКР1436ПП1": "TP3070", "ЭКР1436УЕ1": "-",
                  "КА1436УН1": "MC34119", "ЭКР1436ХА1": "TEA1068"}

    series1500 = {"К1500ВА123": "F100123", "К1500ИВ165": "F100165",
                  "1500ИД170": "F100170", "К1500ИД170": "F100170",
                  "1500ИЕ136": "F100136", "К1500ИЕ136": "F100136",
                  "1500ИЕ160": "F100160", "К1500ИЕ160": "F100160",
                  "1500ИМ180": "F100180", "К1500ИМ180": "F100180",
                  "КН1500ИМ180": "F100180", "1500ИП179": "F100179",
                  "К1500ИП179": "F100179", "К1500ИП181": "F100181",
                  "1500ИП194": "F100194", "К1500ИП194": "F100194",
                  "1500ИР141": "F100141", "1500ИР150": "F100150",
                  "1500ИР151": "F100151", "1500КП155": "F100155",
                  "1500КП163": "F100163", "К1500КП163": "F100163",
                  "1500КП164": "F100164", "1500КП171": "F100171",
                  "К1500КП171": "F100171", "К1500ЛА104": "-",
                  "1500ЛК117": "F100117", "1500ЛК118": "F100118",
                  "1500ЛМ101": "F100101", "К1500ЛМ101": "F100101",
                  "1500ЛМ102": "F100102", "К1500ЛМ102": "F100102",
                  "1500ЛП107": "F100107", "1500ЛП112": "F100112",
                  "К1500ЛП112": "F100112", "1500ЛП114": "F100114",
                  "К1500ЛП114": "F100114", "1500ЛП122": "F100122",
                  "К1500ЛП122": "F100122", "1500ПУ124": "F100124",
                  "К1500ПУ124": "F100124", "1500ПУ125": "F100125",
                  "К1500ПУ125": "F100125", "1500РУ415": "F100415",
                  "1500РУ470": "F100470", "1500РУ470А": "F100470",
                  "1500РУ474": "HM100474", "К1500РУ474": "HM100474",
                  "1500СП166": "F100166", "К1500СП166": "F100166",
                  "1500ТМ130": "F100130", "1500ТМ131": "F100131"}

    series1506 = {"КР1506ВГ3": "SAA1293", "К1506ХЛ1": "SAA1250",
                  "КМ1506ХЛ1": "SAA1250", "КР1506ХЛ1": "SAA1250",
                  "К1506ХЛ2": "SAA1251", "КМ1506ХЛ2": "SAA1251",
                  "КР1506ХЛ2": "SAA1251", "К1506ХЛ3": "SAA3006",
                  "КР1506ХЛ3": "SAA3006", "КФ1506ХЛ3": "SAA3006",
                  "КР1506ХЛ5": "SAA1250"}

    series1507 = {"КР1507ИЕ1": "μPC552C"}

    series1520 = {"1520ХМ1": "MCA600ECL", "К1520ХМ1": "MCA600ECL",
                  "КН1520ХМ1": "MCA600ECL", "1520ХМ2": "MCA1200ECL",
                  "К1520ХМ2": "MCA1200ECL", "1520ХМ3": "FGE2000",
                  "К1520ХМ3": "FGE2000", "1520ХМ5": "SH100"}

    series1521 = {"1521ХМ1": "MCA600ECL"}

    series1526 = {"1526АГ1": "CD4098A", "1526ИД1": "CD4028A",
                  "1526ИЕ9": "CD4022A", "1526ИЕ10": "MC14520",
                  "1526ИЕ11": "MC14516", "1526ИЕ14": "CD4029A",
                  "1526ИЕ15": "CD4059A", "1526ИЕ19": "-", "1526ИК1": "-",
                  "1526ИМ1": "CD4008A", "1526ИП2": "MC14585",
                  "1526ИП3": "MC14585", "1526ИП4": "-", "1526ИП6": "CD40101",
                  "1526ИР1": "CD4006A", "1526ИР2": "CD4015A",
                  "1526ИР6": "CD4034A", "1526ИР9": "CD4035A",
                  "1526ИР11": "CD4036A", "1526ИР13": "MM54C905",
                  "1526КП1": "CD4052A", "1526КП2": "CD4051A",
                  "1526КТ3": "CD4066A", "1526ЛА7": "CD4011A",
                  "1526ЛА8": "CD4012A", "1526ЛА9": "CD4023A",
                  "1526ЛА10": "CD40107A", "1526ЛЕ5": "CD4001A",
                  "1526ЛЕ6": "CD4002A", "1526ЛЕ10": "CD4025A",
                  "1526ЛН1": "MC14502", "1526ЛН2": "CD4049A",
                  "1526ЛП2": "CD4030A", "1526ЛП13": "-", "1526ЛС2": "CD4019A",
                  "1526ПР1": "MC14094", "1526ПУ4": "CD4050A",
                  "1526ПУ6": "CD40109A", "1526ПУ7": "-", "1526ПУ8": "-",
                  "1526ПУ9": "-", "1526СА1": "MC14531", "1526ТВ1": "CD4027A",
                  "1526ТЛ1": "CD4093A", "1526ТМ2": "CD4013A",
                  "1526ТМ3": "CD4042A", "1526ТР2": "CD4043A"}

    series1531 = {"КР1531АП3": "74F240", "КР1531АП4": "74F241",
                  "КР1531АП5": "74F244", "КР1531АП6": "74F245",
                  "КР1531ИД7": "74F138", "КР1531ИД14": "74F139",
                  "КР1531ИД22": "74F537", "КР1531ИЕ10": "74F161",
                  "КР1531ИП3": "74F181", "КР1531ИП4": "74F182",
                  "КР1531ИП5": "74F280", "КР1531ИР11": "74F194",
                  "КР1531ИР22": "74F373", "КР1531ИР23": "74F374",
                  "КР1531ИР40": "74F533", "КР1531ИР41": "74F534",
                  "КР1531ИР42": "74F350", "КР1531КП2": "74F153",
                  "КР1531КП7": "74F151", "КР1531КП11": "74F257",
                  "КР1531КП12": "74F253", "1531КП14": "74F258",
                  "КР1531КП15": "74F251", "1531КП16": "74F157",
                  "КР1531КП16": "74F157", "1531КП18": "74F158",
                  "КР1531КП18": "74F158", "КР1531ЛА1": "74F20",
                  "КР1531ЛА3": "74F00", "КР1531ЛА4": "74F10",
                  "КР1531ЛЕ1": "74F02", "КР1531ЛИ1": "74F08",
                  "КР1531ЛИ3": "74F11", "КР1531ЛЛ1": "74F32",
                  "КР1531ЛН1": "74F04", "1531ЛП5": "54F86",
                  "КР1531ЛП5": "74F86", "1531ЛР9": "54F64",
                  "КР1531ЛР9": "74F64", "КР1531РУ8": "74F189",
                  "КР1531СП2": "74F521", "КР1531ТВ10": "74F113",
                  "КР1531ТВ15": "74F109", "КР1531ТМ2": "74F74",
                  "1531ТМ8": "54F175", "КР1531ТМ8": "74F175",
                  "1531ТМ9": "54F174", "КР1531ТМ9": "74F174"}

    series1533 = {"КР1533АГ3": "SN74LS123", "1533АП3": "SN54ALS240",
                  "КР1533АП3": "SN74ALS240", "1533АП4": "SN54ALS241",
                  "КР1533АП4": "SN74ALS241", "1533АП5": "SN54ALS244",
                  "КР1533АП5": "SN74ALS244", "КР1533АП6": "SN74ALS245",
                  "КР1533АП9": "SN74ALS640A", "КР1533АП14": "SN74ALS465A",
                  "КР1533АП15": "SN74ALS466A", "КР1533АП16": "SN74ALS643A",
                  "1533ИД3": "SN54154", "КР1533ИД3": "SN74154",
                  "1533ИД4": "SN54LS155", "КР1533ИД4": "SN74LS155",
                  "1533ИД7": "SN54ALS138", "КР1533ИД14": "SN74ALS139",
                  "КР1533ИД17": "-", "КР1533ИЕ2": "SN74LS90",
                  "КР1533ИЕ5": "SN74LS93", "1533ИЕ6": "SN54ALS192",
                  "КР1533ИЕ6": "SN74ALS192", "КР1533ИЕ7": "SN74ALS193",
                  "1533ИЕ9": "SN54ALS160A", "КР1533ИЕ9": "SN74ALS160A",
                  "1533ИЕ10": "SN54ALS161", "КР1533ИЕ10": "SN74ALS161",
                  "1533ИЕ11": "SN54ALS162A", "КР1533ИЕ11": "SN74ALS162",
                  "КР1533ИЕ12": "SN74ALS190", "КР1533ИЕ13": "SN54ALS191",
                  "1533ИЕ18": "SN54ALS163A", "КР1533ИЕ18": "SN74ALS163",
                  "КР1533ИЕ19": "SN74ALS393", "1533ИП3": "SN54AS181",
                  "КР1533ИП3": "SN74AS181", "1533ИП4": "SN54182",
                  "КР1533ИП4": "SN74182", "1533ИП5": "SN54LS86",
                  "КР1533ИП5": "SN74LS86", "1533ИП6": "SN54ALS242",
                  "КР1533ИП6": "SN74ALS242", "1533ИП7": "SN54ALS243A",
                  "КР1533ИП7": "SN74ALS243A", "КР1533ИП15": "MB502A",
                  "КР1533ИР9": "SN74ALS165", "КР1533ИР10": "SN74ALS166",
                  "КР1533ИР13": "SN74198", "1533ИР22": "SN54ALS373",
                  "КР1533ИР22": "SN74ALS373", "1533ИР23": "SN54ALS374",
                  "КР1533ИР23": "SN74ALS374", "1533ИР24": "SN54ALS299",
                  "КР1533ИР24": "SN74ALS299", "КР1533ИР26": "SN74LS670",
                  "КР1533ИР27": "SN74LS377", "КР1533ИР29": "SN74ALS323",
                  "КР1533ИР30": "SN74ALS259", "1533ИР31": "-",
                  "КР1533ИР32": "SN74LS170", "1533ИР33": "SN54ALS573",
                  "КР1533ИР33": "SN74ALS573", "1533ИР34": "SN54ALS873",
                  "КР1533ИР34": "SN74ALS873", "КР1533ИР35": "SN74ALS273",
                  "1533ИР37": "SN54ALS574", "КР1533ИР37": "SN74ALS574",
                  "1533ИР38": "SN54ALS874", "КР1533ИР38": "SN74ALS874",
                  "1533ИР39": "-", "1533КП2": "SN54ALS153",
                  "КР1533КП2": "SN74ALS153", "1533КП7": "SN54ALS151",
                  "КР1533КП7": "SN74ALS151", "1533КП11": "SN54ALS257",
                  "1533КП11А": "SN54ALS257", "КР1533КП11А": "SN74ALS257",
                  "1533КП12": "SN54ALS253", "КР1533КП12": "SN74ALS253",
                  "1533КП13": "SN54LS298", "КР1533КП13": "SN74LS298",
                  "1533КП14": "SN54ALS258", "1533КП14А": "SN54ALS258",
                  "КР1533КП14А": "SN74ALS258", "КР1533КП15": "SN54ALS251",
                  "1533КП16": "SN54ALS157", "КР1533КП16": "SN74ALS157",
                  "1533КП17": "SN54ALS353", "КР1533КП17": "SN74ALS353",
                  "1533КП18": "SN54ALS158", "КР1533КП18": "SN74ALS158",
                  "1533КП19": "SN54ALS352", "КР1533КП19": "SN74ALS352",
                  "1533ЛА1": "SN54ALS20", "КР1533ЛА1": "SN74ALS20",
                  "1533ЛА2": "SN54ALS30", "КР1533ЛА2": "SN74ALS30",
                  "1533ЛА3": "SN54ALS00", "КР1533ЛА3": "SN74ALS00",
                  "1533ЛА4": "SN54ALS10", "КР1533ЛА4": "SN74ALS10",
                  "1533ЛА6": "SN54ALS40A", "1533ЛА7": "SN54ALS22",
                  "КР1533ЛА7": "SN74ALS22", "1533ЛА8": "SN54ALS01",
                  "КР1533ЛА8": "SN74ALS01", "1533ЛА9": "SN54ALS03",
                  "КР1533ЛА9": "SN74ALS03", "КР1533ЛА10": "SN74ALS12A",
                  "1533ЛА12": "SN54ALS37", "1533ЛА13": "SN54ALS38",
                  "КР1533ЛА21": "SN74ALS1000A", "КР1533ЛА22": "SN74ALS1020A",
                  "КР1533ЛА23": "SN74ALS1003A", "КР1533ЛА24": "SN74ALS1010A",
                  "1533ЛЕ1": "SN54ALS02", "КР1533ЛЕ1": "SN74ALS02",
                  "КР1533ЛЕ4": "SN74ALS27", "КР1533ЛЕ10": "SN74ALS1002A",
                  "КР1533ЛЕ11": "SN74ALS33A", "1533ЛИ1": "SN54ALS08",
                  "КР1533ЛИ1": "SN74ALS08", "КР1533ЛИ2": "SN74ALS09",
                  "КР1533ЛИ3": "SN74ALS11A", "КР1533ЛИ4": "SN74ALS15A",
                  "КР1533ЛИ6": "SN74ALS21", "КР1533ЛИ8": "SN74ALS1008A",
                  "КР1533ЛИ10": "SN74ALS1011A", "КР1533ЛЛ1": "SN74ALS32",
                  "КР1533ЛЛ4": "SN74ALS1032A", "1533ЛН1": "SN54ALS04",
                  "КР1533ЛН1": "SN74ALS04", "1533ЛН2": "SN54ALS05",
                  "КР1533ЛН2": "SN74ALS05", "КР1533ЛН7": "SN74ALS368",
                  "КР1533ЛН8": "SN74ALS1004", "КР1533ЛН10": "SN74ALS1005",
                  "1533ЛП3": "-", "КР1533ЛП3": "-", "1533ЛП5": "SN74ALS86",
                  "КР1533ЛП5": "SN74ALS86", "КР1533ЛП8": "SN74LS125",
                  "КР1533ЛП12": "SN74ALS136", "КР1533ЛП16": "SN74ALS1034",
                  "КР1533ЛП17": "SN74ALS1035", "1533ЛР4": "SN74ALS55",
                  "КР1533ЛР4": "SN74ALS55", "1533ЛР11": "SN74ALS51",
                  "КР1533ЛР11": "SN74ALS51", "1533ЛР13": "SN74ALS54",
                  "КР1533ЛР13": "SN74ALS54", "1533СП1": "SN54ALS85",
                  "КР1533СП1": "SN74ALS85", "КР1533ТВ6": "SN74LS107",
                  "КР1533ТВ9": "SN74ALS112A", "КР1533ТВ10": "SN74ALS113A",
                  "КР1533ТВ11": "SN74ALS114A", "1533ТВ15": "SN54ALS109",
                  "КР1533ТВ15": "SN74ALS109", "КР1533ТЛ2": "SN74LS14",
                  "1533ТМ2": "SN54ALS74", "КР1533ТМ2": "SN74ALS74",
                  "КР1533ТМ7": "SN74ALS75", "КР1533ТМ8": "SN74ALS175",
                  "1533ТМ9": "SN54ALS174", "КР1533ТМ9": "SN74ALS174",
                  "1533ТР2": "SN54LS279", "КР1533ТР2": "SN74LS279"}

    series1540 = {"1540ХМ1": "MCA1300"}

    series1554 = {"КР1554АП3": "74AC240", "КР1554АП4": "74AC241",
                  "КР1554АП5": "74AC244", "КР1554ИР22": "74AC373",
                  "КР1554ИР23": "74AC374", "КР1554ИР35": "74AC273",
                  "КР1554ИР40": "74AC533", "КР1554ИР41": "74AC534",
                  "КР1554КП2": "74AC153", "КР1554КП12": "74AC253",
                  "КР1554КП16": "74AC157", "КР1554ЛА1": "74AC20",
                  "КР1554ЛА3": "74AC00", "КР1554ЛЕ1": "74AC02",
                  "КР1554ЛИ1": "74AC08", "КР1554ЛИ9": "74AC34",
                  "КР1554ЛЛ1": "74AC32", "КР1554ЛН1": "74AC04",
                  "КР1554ТВ9": "74AC112", "КР1554ТВ15": "74AC109",
                  "КР1554ТМ2": "74AC74"}

    series1556 = {"КР1556ХЛ8": "DMPAL16L8C", "М1556ХЛ8": "PAL16L8M",
                  "КР1556ХП4": "DMPAL16R4C", "М1556ХП4": "PAL16R4M",
                  "КР1556ХП6": "DMPAL16R6C", "М1556ХП6": "PAL16R6M",
                  "КР1556ХП8": "DMPAL16R8C", "М1556ХП8": "PAL16R8M"}

    series1561 = {"КР1561АГ1": "CD4098BE", "КР1561ГГ1": "CD4046B",
                  "КР1561ИД6": "MC14555BE", "КР1561ИЕ10": "CD4520",
                  "КР1561ИЕ20": "MC14040B", "КР1561ИЕ21": "MC14161B",
                  "КФ1561ИР6": "CD4034B", "КР1561ИР14": "MC14076B",
                  "КР1561ИР15": "MC14194B", "КР1561КП1": "CD4052B",
                  "КР1561КП2": "CD4051B", "КР1561КП3": "MC14512B",
                  "КР1561КП4": "MC14519B", "КР1561КП5": "MC14053BCP",
                  "КР1561КТ3": "MC14066BCP", "КФ1561КТ3": "MC14066BCP",
                  "КР1561ЛА9": "CD4023BE", "КФ1561ЛА9": "CD4023DE",
                  "КР1561ЛЕ5": "CD4001B", "КР1561ЛЕ6": "CD4002B",
                  "КР1561ЛЕ10": "CD4025BE", "КФ1561ЛЕ10": "CD4025BE",
                  "КР1561ЛИ2": "CD4081B", "КР1561ЛП14": "CD4070B",
                  "КР1561ПР1": "CD4094B", "КР1561ПУ4": "CD4050B",
                  "КР1561ТВ1": "CD4027B", "КР1561ТЛ1": "MC14093",
                  "КФ1561ТЛ1": "MC14093"}

    series1564 = {"1564АП4": "MM54HC241", "1564ИВ3": "MM54HC147",
                  "1564ИД3": "MM54HC154", "1564ИД7": "MM54HC138",
                  "1564ИД23": "MM54HC4511", "1564ИЕ6": "MM54HC192",
                  "КР1564ИЕ6": "MM74HC192", "1564ИЕ7": "MM54HC193",
                  "КР1564ИЕ7": "MM74HC193", "1564ИЕ10": "MM54HC161",
                  "КР1564ИЕ10": "MM74HC161", "1564ИЕ19": "MM54HC393",
                  "КР1564ИЕ19": "MM74HC393", "1564ИП5": "MM54HC280",
                  "1564ИП7": "MM54HC243", "1564ИР8": "MM54HC164",
                  "1564ИР9": "MM54HC165", "КР1564ИР9": "MM74HC165",
                  "1564КП2": "MM54HC153", "1564КП11": "MM54HC257",
                  "1564КП12": "MM54HC253", "1564КП13": "MM54HC298",
                  "КР1564КП13": "MM74HC298", "1564КП15": "MM54HC251",
                  "1564ЛА1": "MM54HC00", "КР1564ЛА1": "MM74HC00",
                  "1564ЛА2": "MM54HC30", "КР1564ЛА3": "MM74HC20",
                  "1564ЛА4": "MM54HC10", "1564ЛЕ9": "MM54HC4002",
                  "1564ЛЛ1": "MM54HC32", "1564ЛН1": "MM54HC04",
                  "1564ЛН7": "MM54HC368", "1564ЛП5": "MM54HC86",
                  "1564ЛП13": "MM54HC266", "1564ЛР11": "MM54HC51",
                  "1564ПУ1": "MM54HC4049", "1564ПУ2": "MM54HC4050",
                  "1564ТЛ2": "MM54HC14", "1564ТМ2": "MM54HC74",
                  "КР1564ТМ2": "MM74HC74", "1564ТМ5": "MM54HC77"}

    series1566 = {"КС1566ХЛ1": "SAA1250", "КС1566ХЛ2": "SAA1251",
                  "КР1566ХЛ3": "SAA3006"}

    series1568 = {"ЭКР1568ВГ1": "PCA84C640", "ЭКР1568ХЛ1": "SAA3010"}

    series1590 = {"КС1590ИД164": "MC10H164", "КС1590ИЕ160": "MC10H160",
                  "КС1590ЛК117": "MC10H117", "КС1590ЛК121": "MC10H121",
                  "КС1590ЛЛ110": "MC10H110", "КС1590ЛМ101": "MC10H101",
                  "КС1590ЛМ102": "MC10H102", "КС1590ЛМ105": "MC10H105",
                  "КС1590ЛП107": "MC10H107", "КС1590ТМ173": "MC10H173"}

    series1601 = {"1601РР1А,Б": "ER3400"}

    series1603 = {"1603РЕ1": "TA10906D", "КА1603РЕ1": "SCM5316",
                  "1603РУ1": "M5101L-4"}

    series1617 = {"1617РУ13А,Б": "-", "1617РУ14А,Б": "HM6504"}

    series1623 = {"М1623РТ1А,Б": "NCR2316-20", "1623РТ2А,Б": "HM6664"}

    series1625 = {"КР1625РП1": "PCF8571P"}

    series1628 = {"КР1628РР2": "MDA2062"}

    series1630 = {"КР1630РУ1А-Л": "M71C256", "ЭКР1630РУ2А-Л": "-",
                  "ЭКР1630РУ3А-Л": "-", "ЭКР1630РУ4": "μPD411000-15",
                  "ЭКР1630РУ41": "-", "ЭКР1630РУ42": "-", "ЭКР1630РУ43": "-",
                  "ЭКР1630РУ44": "-"}

    series1656 = {"КР1656РЕ1": "5275-1", "М1656РЕ1": "5275-1",
                  "М1656РЕ2": "6275-1", "1656РЕ4": "2364-20",
                  "КР1656РЕ4": "MB7144", "М1656РЕ4": "2364", "1656РЕ6А,Б": "-",
                  "КР1656РП2": "-"}

    series1800 = {"КС1800ВА4": "MC10804L", "КС1800ВА7": "MC10807L",
                  "КР1800ВЖ5": "MC10905", "К1800ВР8": "MC10808",
                  "К1800ВС1": "MC10800", "К1800РП6": "MC10806",
                  "К1800РП16": "-"}

    series1802 = {"1802ВВ1": "-", "КР1802ВВ1": "-", "1802ВВ2": "-",
                  "КР1802ВВ2": "-", "1802ВВ3": "-", "1802ВР1": "AM25510",
                  "КР1802ВР1": "AM25510", "1802ВР2": "SN74S508",
                  "КР1802ВР2": "SN74S508", "1802ВР4": "MPY12HJ",
                  "КМ1802ВР4": "MPY12HJ", "1802ВР5": "MPY16HJ",
                  "КМ1802ВР5": "MPY16HJ"}

    series1809 = {"К1809ВВ1": "-", "М1809ВВ1": "-", "КР1809ВВ3": "SCN2681P",
                  "К1809ВГ3": "TMS9918A", "М1809ВГ4": "μPD7220",
                  "КР1809ВГ4": "μPD7220", "М1809ВГ6": "MC6845",
                  "КР1809ВГ6": "MC6845", "КР1809ВГ7": "82062",
                  "КР1809ВИ1": "AM9513", "КР1809ВИ1А": "AM9513",
                  "КМ1809ВИ1А": "AM9513", "К1809РЕ1": "MK3600",
                  "К1809РУ1": "-", "КР1809РУ1": "-", "КР1809РУ1А": "-"}

    series1810 = {"КР1810ВБ89": "8289", "М1810ВБ89": "8289",
                  "КР1810ВГ72А": "8272", "КР1810ВГ88": "8288",
                  "М1810ВГ88": "8288", "КР1810ВИ54": "8254",
                  "КР1810ВК56": "8256", "КР1810ВМ86": "8086",
                  "КР1810ВМ86Б": "8086", "КР1810ВМ86М": "8086",
                  "КР1810ВМ88": "8088", "КР1810ВМ89": "8089",
                  "КР1810ВН59А": "8259A", "КР1810ВТ3": "8203",
                  "КР1810ВТ37А": "8237A", "КР1810ВТ37Б": "8237",
                  "КР1810ВТ37В": "8237", "КР1810ГФ84": "8284",
                  "КР1810ГФ84А": "8284A", "М1810ГФ84": "8284"}

    series1816 = {"КР1816ВЕ31": "8031", "КР1816ВЕ35": "8035",
                  "КР1816ВЕ39": "8039", "КМ1816ВЕ48": "8048",
                  "КР1816ВЕ49": "8049", "КР1816ВЕ51": "8051"}

    series1818 = {"КР1818ВА19": "DC3191P", "КМ1818ВВ61": "SCN2661",
                  "КР1818ВВ61": "SCN2661", "КМ1818ВГ01": "μPD7201",
                  "КР1818ВГ01": "μPD7201", "М1818ВГ01": "μPD7201",
                  "КМ1818ВГ01А,Б": "μPD7201", "КР1818ВГ01А,Б": "μPD7201",
                  "КР1818ВГ93": "FDC1793", "КР1818ВЖ1": "F9401",
                  "КР1818ВН19": "Am9519A"}

    series1820 = {"КР1820ВГ1,1А": "COP472", "КР1820ВЕ1,1А": "COP402",
                  "КР1820ВЕ2,2А": "COP420L", "КР1820ВЕ3,3А": "COP424C",
                  "КР1820ВП1,1А": "COP498", "КР1820ИД1,1А": "MC2437"}

    series1821 = {"М1821ВВ19": "82C19", "КМ1821ВВ19": "82C19",
                  "М1821ВВ51А": "82C51A", "КМ1821ВВ51А": "82C51A",
                  "М1821ВИ54": "82C54", "КМ1821ВИ54": "82C54",
                  "КМ1821ВИ54А": "82C54", "КР1821ВМ85": "80C85",
                  "М1821ВМ85А": "80C85", "М1821ВН59А": "82C59A",
                  "КМ1821ВН59А": "82C59A", "КР1821ВТ57": "82C57",
                  "М1821РЕ55": "8355", "КР1821РЕ55": "8355",
                  "М1821РУ55": "8155", "КР1821РУ55": "8155-2"}

    series1823 = {"КР1823ВГ1": "-", "КР1823ВГ2": "-", "КР1823ВГ3": "-",
                  "КР1823ИЕ1": "-", "КР1823ИЕ2": "-", "КР1823РЕ1": "RC825290M"}

    series1827 = {"1827ВЕ1": "TMS9940", "К1827ВЕ1": "TMS9940",
                  "К1827ВЕ2": "TMS32020", "М1827ВЕ3": "μPD7720",
                  "К1827ВЕ4": "μPD7721"}

    series1830 = {"КР1830ВЕ31": "80C31", "Н1830ВЕ31": "80C31",
                  "КР1830ВЕ48": "80C48", "КР1830ВЕ51": "80C51",
                  "Н1830ВЕ51": "80C51"}

    series1834 = {"КР1834ВА86": "82C86", "КР1834ВА87": "82C87",
                  "КР1834ВВ55А": "82C55A", "ЭКР1834ВМ86": "80C86",
                  "ЭКР1834ВМ86А": "80C86", "КР1834ГФ84А": "82C84A"}

    series1835 = {"КА1835ВВ1": "-", "КА1835ВГ1": "-", "КА1835ВГ2": "-",
                  "КА1835ВГ3": "-", "КА1835ВГ4": "-", "КА1835ВГ5": "-",
                  "КА1835ВГ6": "-", "КА1835ВГ7": "-",
                  "КА1835ВГ9": "DC2053P105", "КА1835ВГ10": "DC2054P119",
                  "КА1835ВГ11": "DC2052P175", "КА1835ВГ12": "T7778",
                  "КА1835ВГ12А": "T7778", "КА1835ВГ13": "T6961B",
                  "КА1835ВГ13А": "T6961B", "КА1835ВГ15": "DC2053P105",
                  "ЭКР1835ВГ17": "TC8565", "КА1835ИД1": "-", "КА1835РЕ1": "-",
                  "КР1835РЕ2А,Б": "TC531000AP"}

    series1843 = {"КА1843ВБ1": "82C432", "КА1843ВВ1": "-", "КА1843ВГ1": "-",
                  "КА1843ВГ2": "82C434", "КА1843ВГ3": "82C431",
                  "КА1843ВГ4": "82C433", "КА1843ВМ1": "AM29C325",
                  "КА1843ВМ2": "MC68C881", "КА1843ВС1": "AM29C332",
                  "КА1843ВР1": "AM29C323", "КА1843ВУ1": "AM29C331",
                  "КА1843ИР1": "AM29C334"}

    series1850 = {"КР1850ВЕ35": "INS80351-1"}

    series1852 = {"КЕ1852ВГ1": "TMS9914A"}

    series1853 = {"КР1853ВГ1": "SAA1293A-03"}

    series1858 = {"КР1858ВМ1": "Z80", "КР1858ВМ2": "Z80A"}

    series1873 = {"КМ1873ВЕ48": "80C48"}

    series_ipv = {"ИПВ70А-4/5x7к": "HDSP-2010", "ИПВ72А-4/5x7к": "HDSP-2310"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True
        self.padding = 10
        self.cols = 3
        self.spacing = [dp(4)]
        self.series = None

    def build_table(self, series, view, *args):
        self.labels = []
        if not self.series == series:
            view.scroll_y = 1
            self.clear_widgets()
            for k, v in getattr(ChipsAnalogs, series).items():
                label_k = MDLabel(text=k, adaptive_height=True,
                                  halign="right",
                                  size_hint_x=None,
                                  width=Window.width * 0.5 - 16)
                label_v = MDLabel(text=v, adaptive_height=True,
                                  size_hint_x=None,
                                  width=Window.width * 0.5 - 16)
                self.labels.append((label_k, label_v))

                self.add_widget(label_k)
                self.add_widget(MDDivider(orientation="vertical"))
                self.add_widget(label_v)
                self.add_widget(MDDivider())
                self.add_widget(MDDivider())
                self.add_widget(MDDivider())
        self.series = series

        Window.bind(on_resize=self.update_width)

    def update_width(self, *args):
        new_width = Window.width * 0.5 - 16
        for label_k, label_v in self.labels:
            label_k.width = new_width
            label_v.width = new_width


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
        webbrowser.open("https://yoomoney.ru/to/410011259431654")

    def git(self):
        webbrowser.open("https://github.com/LemanRus/RadioMan")

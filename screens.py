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

    series171 = {"171УВ1А,Б": "SL610", "171УВ2": "(A733", "171УВ3": "SL521C"}

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
                 "К174УН14": "TDA2003", "К174УН14А": "TDA2003",
                 "К174УН14": "TDA2003", "К174УН14А": "TDA2003",
                 "КФ174УН17": "TA7688", "К174УН18": "AN7145",
                 "К174УН19": "TDA2030", "К174УН20": "-", "К174УН21": "TDA7050",
                 "К174УН22": "-", "КФ174УН23": "-", "К174УН24": "TDA7052",
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
                 "КР249КН5А-П": "-", "КР249КН6А-П": "-", "КР249КН7А-Г": " ",
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

    series521 = {"521СА1": "(A711", "Р521СА1": "(A711", "521СА2": "(A710",
                 "К521СА2": "(A710C", "Р521СА2": "(A710", "521СА3": "LM111",
                 "Н521СА3": "LM311J", "521СА4": "SE257K", "521СА5": "TL810",
                 "ЭК521СА5": "TL810", "521СА101": "(A711", "521СА201": "(A710",
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
                 "533ХП1": "-", }

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
        webbrowser.open("https://yoomoney.ru/fundraise/2SFAdwO6BB0.230827")

    def git(self):
        webbrowser.open("https://github.com/LemanRus/RadioMan")

import itertools
import weakref

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import BoundedNumericProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton, MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager


class MarkingsScreen(MDScreen):
    pass


class CalculationsScreen(MDScreen):
    pass


class HandbookScreen(MDScreen):
    pass


class HelpScreen(MDScreen):
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


class ResistorBand(MDIconButton):
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
        self.band_no = kwargs.pop("band_no")
        self.band_qty = kwargs.pop("band_qty")
        super().__init__(*args, **kwargs)
        self.menu = ResistorBandDropdownMennu(
            caller=self,
            items=self.get_band(self.band_no, self.band_qty),
            position="center",
            border_margin=dp(12),
            width=dp(100)
        )
        self.menu.width = self.menu.minimum_width
        self.my_color = self.bands_accordance[self.band_qty][self.band_no]
        self.md_bg_color = list(self.my_color.values())[0]
        self.theme_icon_color = self.theme_text_color = "Custom"
        self.icon = "chevron-down"
        self.text = list(self.my_color.keys())[0]
        if self.text in ["Чёрный", "Коричневый"]:
            self.icon_color = self.text_color = "white"
        self.bind(on_release=self.menu_open)
        self.menu.bind(on_dismiss=lambda _: self.__setattr__("icon", "chevron-down"))
        self.rounded_button = False
        self._radius = dp(7)

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
        self.icon = "chevron-up"
        self.menu.open()

    def set_item(self, param_item):
        self.text = param_item[0]
        self.md_bg_color = param_item[1]
        self.icon = "chevron-down"
        if param_item[0] in ["Чёрный", "Коричневый"]:
            self.icon_color = self.text_color = "white"
        else:
            self.icon_color = self.text_color = "black"
        self.parent.parent.parent.parent.parent.ids.result.text = "Результат: "
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
            (Window.width * 3 / 5) / (self.bands_qty * 4)
        )
        self.ids.result.text = "Результат:"
        for i in range(0, self.bands_qty):
            band = ResistorBand(size_hint=(1, 1), band_no=i, band_qty=self.bands_qty)
            self.ids.bands.add_widget(band)
            self.ids.bands.ids["band" + str(i)] = weakref.ref(band)

    def calculate_resistor(self):
        thermal = ""
        tolerance = ""

        if "band5" in self.ids.bands.ids.keys():
            thermal = self.thermal[self.ids.bands.ids.band5.text]
        if "band4" in self.ids.bands.ids.keys():
            tolerance = self.tolerance[self.ids.bands.ids.band4.text]
        if len(self.ids.bands.ids.keys()) in (3, 4):
            multiplier = self.multiplier[self.ids.bands.ids.band2.text]
            resistance = (self.nominal[self.ids.bands.ids.band0.text] * 10 +
                          self.nominal[self.ids.bands.ids.band1.text]) * multiplier

            if "band3" in self.ids.bands.ids.keys():
                tolerance = self.tolerance[self.ids.bands.ids.band3.text]
            else:
                tolerance = "±20%"
        else:
            multiplier = self.multiplier[self.ids.bands.ids.band3.text]
            resistance = (self.nominal[self.ids.bands.ids.band0.text] * 100 +
                          self.nominal[self.ids.bands.ids.band1.text] * 10 +
                          self.nominal[self.ids.bands.ids.band2.text]) * multiplier

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
            capacity = float("{}.{}".format(value.lower().split("R")[0], value.lower().split("R")[1]))
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


class MarkingsScreenManager(MDScreenManager):
    pass


class CalculationsScreenManager(MDScreenManager):
    pass


class HandbookScreenManager(MDScreenManager):
    pass


class HelpScreenManager(MDScreenManager):
    pass

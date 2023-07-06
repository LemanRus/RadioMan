import itertools
import weakref

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, ObjectProperty, StringProperty
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

        self.width = dp(120)

        self.height = self.target_height
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
# TODO: make band to reset result when changed
    bands_accordance = {
        3: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
        },
        4: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
        }, 5: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 2, None)),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
            4: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
        }, 6: {
            0: dict(itertools.islice(colors.items(), 3, None)),
            1: dict(itertools.islice(colors.items(), 2, None)),
            2: dict(itertools.islice(colors.items(), 2, None)),
            3: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
            4: dict(itertools.islice(colors.items(), 0, len(colors.keys()))),
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
        self.ids.bands.clear_widgets()
        self.ids.bands.ids.clear()
        self.ids.result.text = "Результат:"
        for i in range(0, int(value)):
            band = ResistorBand(size_hint=(1, 1), band_no=i, band_qty=int(value))
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
    pass


class CapacitorsMarkingScreen(MDScreen):
    pass


class MarkingsScreenManager(MDScreenManager):
    pass


class CalculationsScreenManager(MDScreenManager):
    pass


class HandbookScreenManager(MDScreenManager):
    pass


class HelpScreenManager(MDScreenManager):
    pass

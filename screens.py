import itertools
import weakref

from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton, MDFlatButton
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


class ResistorBand(MDFlatButton):
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
        self.menu = MDDropdownMenu(
            caller=self,
            items=self.get_band(self.band_no, self.band_qty),
            position="bottom"
        )
        self.my_color = self.bands_accordance[self.band_qty][self.band_no]
        self.md_bg_color = list(self.my_color.values())[0]
        if list(self.my_color.keys())[0] in ["Чёрный", "Коричневый"]:
            self.theme_text_color = "Custom"
            self.text_color = "white"
        self.bind(on_release=self.menu_open)

    def get_band(self, band_no, band_qty):
        band = []
        for k, v in self.bands_accordance[band_qty][band_no].items():
            temp = {"text": k}
            temp.update({"md_bg_color": v})
            if k in ["Чёрный", "Коричневый"]:
                temp.update({"text_color": "white"})
            else:
                temp.update({"text_color": "black"})
            band.append(temp)
        return band

    def menu_open(self, *args):
        self.menu.open()


class THResistorsMarkingScreen(MDScreen):
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
        for i in range(0, int(value)):
            band = ResistorBand(text=f"PM{i}", size_hint=(1, 1), band_no=i, band_qty=int(value),
                                on_text=self.print_me)
            self.ids.bands.add_widget(band)
            self.ids.bands.ids["band" + str(i)] = weakref.ref(band)

    def print_me(self):
        print(self.ids)


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

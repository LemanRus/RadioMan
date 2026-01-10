# -*- coding: utf-8 -*-
"""Кастомные виджеты для RadioMan"""

import itertools

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonIcon
from kivymd.uix.menu import MDDropdownMenu


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

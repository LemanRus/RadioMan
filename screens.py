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
    menu_items_3 = [
        {
            "text": "First",
            "md_bg_color": (1, 1, 0, 1),
        },
        {
            "text": "Second",
            "md_bg_color": (1, 0, 1, 1),
        }
    ]

    def __init__(self, *args, **kwargs):
        self.bands_qty = kwargs.pop("bands_qty")
        super().__init__(*args, **kwargs)
        self.menu = MDDropdownMenu(
            caller=self,
            items=getattr(self, f"menu_items_{self.bands_qty}"),
            position="bottom"
        )
        self.bind(on_release=self.menu_open)

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
            self.ids.bands.add_widget(
                ResistorBand(text=f"PM{i}", size_hint=(1, 1), md_bg_color=(1, i / 10, 0, 1), bands_qty=3,
                             on_text=self.print_me))

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

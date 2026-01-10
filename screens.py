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
from data_loader import (
    load_chips_analogs,
    load_resistor_markings,
    load_smd_resistor_markings,
    load_capacitor_markings
)


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


class CapacitorsMarkingSelectScreen(MDScreen):
    pass


class THCapacitorsMarkingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        capacitor_data = load_capacitor_markings()
        self.decimal_point = capacitor_data['decimal_point']

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        capacitor_data = load_capacitor_markings()
        self.voltage = capacitor_data['voltage']
        self.smd_capacity = capacitor_data['smd_capacity']

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True
        self.padding = 10
        self.cols = 3
        self.spacing = [dp(4)]
        self.series = None
        # Загружаем данные о микросхемах из JSON
        self._chips_data = load_chips_analogs()

    def build_table(self, series, view, *args):
        self.labels = []
        if not self.series == series:
            view.scroll_y = 1
            self.clear_widgets()
            # Используем загруженные данные из JSON вместо getattr
            series_data = self._chips_data.get(series, {})
            for k, v in series_data.items():
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


# Класс HowToScreen теперь в screens/help/__init__.py
# Оставляем для обратной совместимости
from screens.help import HowToScreen


class AboutScreen(MDScreen):
    def mailto(self):
        webbrowser.open("mailto:electronics@hand-made-tlt.ru")

    def pay(self):
        webbrowser.open("https://yoomoney.ru/to/410011259431654")

    def git(self):
        webbrowser.open("https://github.com/LemanRus/RadioMan")

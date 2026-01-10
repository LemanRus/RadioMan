# -*- coding: utf-8 -*-
"""Экран конвертера единиц"""

from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


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

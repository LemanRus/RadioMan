# -*- coding: utf-8 -*-
"""Модуль экранов помощи"""

import webbrowser

from kivymd.uix.screen import MDScreen


class HelpScreen(MDScreen):
    pass


class HowToScreen(MDScreen):
    pass


class AboutScreen(MDScreen):
    def mailto(self):
        webbrowser.open("mailto:electronics@hand-made-tlt.ru")

    def pay(self):
        webbrowser.open("https://yoomoney.ru/to/410011259431654")

    def git(self):
        webbrowser.open("https://github.com/LemanRus/RadioMan")


__all__ = [
    'HelpScreen',
    'HowToScreen',
    'AboutScreen',
]

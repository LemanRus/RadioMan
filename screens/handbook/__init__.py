# -*- coding: utf-8 -*-
"""Модуль справочных экранов"""

from screens.handbook.chips import (
    ChipsScreen,
    ChipsAnalogsSelectScreen,
    ChipsAnalogsScreen,
    ChipsAnalogs
)
from kivymd.uix.screen import MDScreen

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

class LifehacksScreen(MDScreen):
    pass

__all__ = [
    'HandbookScreen',
    'TheoryScreen',
    'SchematicsScreen',
    'PinoutScreen',
    'ConnectionsScreen',
    'ChipsScreen',
    'ChipsAnalogsSelectScreen',
    'ChipsAnalogs',
    'ChipsAnalogsScreen',
    'LifehacksScreen',
]

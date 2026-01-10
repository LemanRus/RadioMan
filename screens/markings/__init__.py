# -*- coding: utf-8 -*-
"""Модуль экранов маркировок компонентов"""

from screens.markings.resistors import (
    MarkingsScreen,
    ResistorsMarkingsSelectScreen,
    THResistorsMarkingScreen,
    SMDResistorsMarkingScreen
)
from screens.markings.capacitors import (
    CapacitorsMarkingSelectScreen,
    THCapacitorsMarkingScreen,
    SMDCapacitorsMarkingScreen
)

__all__ = [
    'MarkingsScreen',
    'ResistorsMarkingsSelectScreen',
    'THResistorsMarkingScreen',
    'SMDResistorsMarkingScreen',
    'CapacitorsMarkingSelectScreen',
    'THCapacitorsMarkingScreen',
    'SMDCapacitorsMarkingScreen',
]

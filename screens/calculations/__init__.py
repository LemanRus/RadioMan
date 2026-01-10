# -*- coding: utf-8 -*-
"""Модуль экранов расчетов"""

from screens.calculations.converter import ConverterCalculationScreen
from screens.calculations.led import LEDResistorCalculationScreen
from screens.calculations.inductor import (
    InductorCalculationSelectScreen,
    InductorCalculateInductionScreen,
    InductorCalculateSizeScreen
)
from screens.calculations.resistors import ParallelResistorCalculationScreen
from screens.calculations.capacitors import SerialCapacitorCalculateScreen
from screens.calculations.voltage_divider import (
    VoltageDividerCalculateSelectScreen,
    VoltageDividerCalculateVoltageScreen,
    VoltageDividerCalculateResistanceScreen
)
from screens.calculations.lm_regulator import (
    LMRegulatorCalculateSelectScreen,
    LMRegulatorCalculateVoltageScreen,
    LMRegulatorCalculateCurrentScreen
)
from kivymd.uix.screen import MDScreen

class CalculationsScreen(MDScreen):
    pass

__all__ = [
    'CalculationsScreen',
    'ConverterCalculationScreen',
    'LEDResistorCalculationScreen',
    'InductorCalculationSelectScreen',
    'InductorCalculateInductionScreen',
    'InductorCalculateSizeScreen',
    'ParallelResistorCalculationScreen',
    'SerialCapacitorCalculateScreen',
    'VoltageDividerCalculateSelectScreen',
    'VoltageDividerCalculateVoltageScreen',
    'VoltageDividerCalculateResistanceScreen',
    'LMRegulatorCalculateSelectScreen',
    'LMRegulatorCalculateVoltageScreen',
    'LMRegulatorCalculateCurrentScreen',
]

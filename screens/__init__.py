# -*- coding: utf-8 -*-
"""Модуль screens - все экраны приложения RadioMan"""

# Импортируем все классы для обратной совместимости
from screens.widgets import ResistorBand, ResistorBandDropdownMennu
from screens.managers import (
    MarkingsScreenManager,
    CalculationsScreenManager,
    HandbookScreenManager,
    HelpScreenManager
)
from screens.markings import (
    MarkingsScreen,
    ResistorsMarkingsSelectScreen,
    THResistorsMarkingScreen,
    SMDResistorsMarkingScreen,
    CapacitorsMarkingSelectScreen,
    THCapacitorsMarkingScreen,
    SMDCapacitorsMarkingScreen
)
from screens.calculations import (
    CalculationsScreen,
    ConverterCalculationScreen,
    LEDResistorCalculationScreen,
    InductorCalculationSelectScreen,
    InductorCalculateInductionScreen,
    InductorCalculateSizeScreen,
    ParallelResistorCalculationScreen,
    SerialCapacitorCalculateScreen,
    VoltageDividerCalculateSelectScreen,
    VoltageDividerCalculateVoltageScreen,
    VoltageDividerCalculateResistanceScreen,
    LMRegulatorCalculateSelectScreen,
    LMRegulatorCalculateVoltageScreen,
    LMRegulatorCalculateCurrentScreen
)
from screens.handbook import (
    HandbookScreen,
    TheoryScreen,
    SchematicsScreen,
    PinoutScreen,
    ConnectionsScreen,
    ChipsScreen,
    ChipsAnalogsSelectScreen,
    ChipsAnalogsScreen,
    LifehacksScreen
)
from screens.help import (
    HelpScreen,
    HowToScreen,
    AboutScreen
)

# Экспортируем ChipsAnalogs из handbook
from screens.handbook.chips import ChipsAnalogs

__all__ = [
    # Widgets
    'ResistorBand',
    'ResistorBandDropdownMennu',
    # Managers
    'MarkingsScreenManager',
    'CalculationsScreenManager',
    'HandbookScreenManager',
    'HelpScreenManager',
    # Markings
    'MarkingsScreen',
    'ResistorsMarkingsSelectScreen',
    'THResistorsMarkingScreen',
    'SMDResistorsMarkingScreen',
    'CapacitorsMarkingSelectScreen',
    'THCapacitorsMarkingScreen',
    'SMDCapacitorsMarkingScreen',
    # Calculations
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
    # Handbook
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
    # Help
    'HelpScreen',
    'HowToScreen',
    'AboutScreen',
]

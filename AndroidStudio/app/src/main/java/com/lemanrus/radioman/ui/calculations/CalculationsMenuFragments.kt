package com.lemanrus.radioman.ui.calculations

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.SectionCards
import com.lemanrus.radioman.ui.common.SectionListFragment

class CalculationsFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.tab_calculations
    override fun cardItems() = SectionCards.calculationsRoot
}

class InductorSelectFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.inductor_select_title
    override fun cardItems() = SectionCards.inductorSelect
}

class VoltageDividerSelectFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.voltage_divider_title
    override fun cardItems() = SectionCards.voltageDividerSelect
}

class LmRegulatorSelectFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.lm_regulator_title
    override fun cardItems() = SectionCards.lmRegulatorSelect
}

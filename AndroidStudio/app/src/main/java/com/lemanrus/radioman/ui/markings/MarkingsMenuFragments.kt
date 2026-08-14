package com.lemanrus.radioman.ui.markings

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.SectionCards
import com.lemanrus.radioman.ui.common.SectionListFragment

class MarkingsFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.tab_markings
    override fun cardItems() = SectionCards.markingsRoot
}

class ResistorsMarkingSelectFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.resistors
    override fun cardItems() = SectionCards.resistorsSelect
}

class CapacitorsMarkingSelectFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.capacitors
    override fun cardItems() = SectionCards.capacitorsSelect
}

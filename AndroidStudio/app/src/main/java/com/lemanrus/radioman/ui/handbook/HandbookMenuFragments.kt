package com.lemanrus.radioman.ui.handbook

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.PlaceholderFragment
import com.lemanrus.radioman.ui.common.SectionCards
import com.lemanrus.radioman.ui.common.SectionListFragment

class HandbookFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.tab_handbook
    override fun cardItems() = SectionCards.handbookRoot
}

class ChipsFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.chips
    override fun cardItems() = SectionCards.chipsRoot
}

class TheoryFragment : PlaceholderFragment() {
    override fun screenTitleRes() = R.string.theory
}

class SchematicsFragment : PlaceholderFragment() {
    override fun screenTitleRes() = R.string.schematics
}

class PinoutFragment : PlaceholderFragment() {
    override fun screenTitleRes() = R.string.pinout
}

class ConnectionsFragment : PlaceholderFragment() {
    override fun screenTitleRes() = R.string.connections
}

class LifehacksFragment : PlaceholderFragment() {
    override fun screenTitleRes() = R.string.lifehacks
}

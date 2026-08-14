package com.lemanrus.radioman.ui.help

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.SectionCards
import com.lemanrus.radioman.ui.common.SectionListFragment

class HelpFragment : SectionListFragment() {
    override fun screenTitleRes() = R.string.tab_help
    override fun cardItems() = SectionCards.helpRoot
}

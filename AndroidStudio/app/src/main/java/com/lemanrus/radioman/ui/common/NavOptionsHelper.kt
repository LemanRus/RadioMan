package com.lemanrus.radioman.ui.common

import androidx.navigation.NavOptions
import com.lemanrus.radioman.R

object NavOptionsHelper {
    fun forward(): NavOptions = NavOptions.Builder()
        .setEnterAnim(R.anim.slide_in_right)
        .setExitAnim(R.anim.slide_out_left)
        .setPopEnterAnim(R.anim.slide_in_left)
        .setPopExitAnim(R.anim.slide_out_right)
        .build()
}

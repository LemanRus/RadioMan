package com.lemanrus.radioman.ui.common

import android.content.Context
import android.util.AttributeSet
import android.widget.PopupMenu
import androidx.core.content.ContextCompat
import com.google.android.material.button.MaterialButton
import com.lemanrus.radioman.R

class ResistorBandView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : MaterialButton(context, attrs) {

    var bandIndex: Int = 0
    var bandCount: Int = 3
    var selectedColor: ResistorColor = ResistorColor.BLACK
        private set

    var onColorChanged: (() -> Unit)? = null

    init {
        setOnClickListener { showColorMenu() }
        applyColor(selectedColor)
    }

    fun configure(index: Int, count: Int, initial: ResistorColor = ResistorColor.BLACK) {
        bandIndex = index
        bandCount = count
        selectedColor = initial
        applyColor(initial)
    }

    private fun showColorMenu() {
        val popup = PopupMenu(context, this)
        val colors = ResistorColor.allowedColors(bandCount, bandIndex)
        colors.forEachIndexed { index, color ->
            popup.menu.add(0, index, index, color.displayName)
        }
        popup.setOnMenuItemClickListener { item ->
            val color = ResistorColor.allowedColors(bandCount, bandIndex)[item.itemId]
            selectedColor = color
            applyColor(color)
            onColorChanged?.invoke()
            true
        }
        popup.show()
    }

    private fun applyColor(color: ResistorColor) {
        setBackgroundColor(ContextCompat.getColor(context, color.colorRes))
        text = "▼"
        val textColor = if (color.darkText) R.color.black else R.color.white
        setTextColor(ContextCompat.getColor(context, textColor))
    }
}

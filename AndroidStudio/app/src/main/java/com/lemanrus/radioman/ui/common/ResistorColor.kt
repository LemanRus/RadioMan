package com.lemanrus.radioman.ui.common

import com.lemanrus.radioman.R

enum class ResistorColor(val displayName: String, val colorRes: Int, val darkText: Boolean) {
    GOLD("Золотой", R.color.resistor_gold, true),
    SILVER("Серебристый", R.color.resistor_silver, true),
    BLACK("Чёрный", R.color.resistor_black, false),
    BROWN("Коричневый", R.color.resistor_brown, false),
    RED("Красный", R.color.resistor_red, true),
    ORANGE("Оранжевый", R.color.resistor_orange, true),
    YELLOW("Жёлтый", R.color.resistor_yellow, true),
    GREEN("Зелёный", R.color.resistor_green, true),
    BLUE("Синий", R.color.resistor_blue, true),
    VIOLET("Фиолетовый", R.color.resistor_violet, true),
    GRAY("Серый", R.color.resistor_gray, true),
    WHITE("Белый", R.color.white, true);

    companion object {
        fun fromName(name: String): ResistorColor? =
            entries.firstOrNull { it.displayName == name }

        fun allowedColors(bandCount: Int, bandIndex: Int): List<ResistorColor> {
            val all = entries
            return when (bandCount) {
                3 -> when (bandIndex) {
                    0 -> all.drop(3).take(3)
                    1 -> all.drop(2)
                    2 -> all
                    else -> all
                }
                4 -> when (bandIndex) {
                    0 -> all.drop(3).take(3)
                    1 -> all.drop(2)
                    2 -> all.dropLast(1)
                    3 -> all.dropLast(1)
                    else -> all
                }
                5 -> when (bandIndex) {
                    0 -> all.drop(3).take(3)
                    1 -> all.drop(2)
                    2 -> all.drop(2)
                    3, 4 -> all.dropLast(1)
                    else -> all
                }
                6 -> when (bandIndex) {
                    0 -> all.drop(3).take(3)
                    1, 2 -> all.drop(2)
                    3, 4 -> all.dropLast(1)
                    5 -> listOf(BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, BLUE, GRAY, WHITE)
                    else -> all
                }
                else -> all
            }
        }
    }
}

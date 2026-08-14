package com.lemanrus.radioman.domain

import org.json.JSONObject

class ThResistorMarkingCalculator(markings: JSONObject) {
    private val nominal = markings.getJSONObject("nominal").toStringMap()
    private val multiplier = markings.getJSONObject("multiplier").toStringMap()
    private val tolerance = markings.getJSONObject("tolerance").toStringMap()
    private val thermal = markings.getJSONObject("thermal").toStringMap()

    fun calculate(bandColors: List<String>, bandCount: Int): String {
        val thermalSuffix: String
        var toleranceStr: String
        val resistance: Double

        when (bandCount) {
            3, 4 -> {
                val mult = multiplier[bandColors[2]]?.toDoubleOrNull() ?: return ValueFormatter.INVALID
                resistance = (
                    (nominal[bandColors[0]]?.toDoubleOrNull() ?: 0.0) * 10 +
                        (nominal[bandColors[1]]?.toDoubleOrNull() ?: 0.0)
                    ) * mult
                toleranceStr = if (bandCount == 4) {
                    tolerance[bandColors[3]] ?: "±20%"
                } else {
                    "±20%"
                }
                thermalSuffix = ""
            }
            5, 6 -> {
                val mult = multiplier[bandColors[3]]?.toDoubleOrNull() ?: return ValueFormatter.INVALID
                resistance = (
                    (nominal[bandColors[0]]?.toDoubleOrNull() ?: 0.0) * 100 +
                        (nominal[bandColors[1]]?.toDoubleOrNull() ?: 0.0) * 10 +
                        (nominal[bandColors[2]]?.toDoubleOrNull() ?: 0.0)
                    ) * mult
                toleranceStr = tolerance[bandColors[4]] ?: ""
                thermalSuffix = if (bandCount == 6) {
                    val t = thermal[bandColors[5]]
                    if (t != null) ", ТКС: $t" else ""
                } else ""
            }
            else -> return ValueFormatter.INVALID
        }

        val formatted = when {
            resistance < 1000 -> "${trim(resistance)} Ом"
            resistance < 1_000_000 -> "${trim(resistance / 1000)} кОм"
            else -> "${trim(resistance / 1_000_000)} МОм"
        }
        return "Результат: $formatted $toleranceStr$thermalSuffix"
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')

    private fun JSONObject.toStringMap(): Map<String, String> {
        val map = mutableMapOf<String, String>()
        keys().forEach { key -> map[key] = get(key).toString() }
        return map
    }
}

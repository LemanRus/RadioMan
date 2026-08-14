package com.lemanrus.radioman.domain

import org.json.JSONObject

class SmdResistorMarkingCalculator(markings: JSONObject) {
    private val eia96 = markings.getJSONObject("eia96").toStringDoubleMap()
    private val eia96Multiplier = markings.getJSONObject("eia96_multiplier").toStringDoubleMap()

    fun calculate(marking: String): String {
        return try {
            val m = marking.lowercase()
            var resistance: Double? = null
            var precision = false

            when {
                m in listOf("0", "00", "000", "0000") -> resistance = 0.0
                "r" in m -> {
                    if (m.length !in 3..4) return "Неверный ввод"
                    val parts = m.split("r")
                    resistance = "${parts[0]}.${parts[1]}".toDouble()
                    precision = m.length == 4
                }
                m.length == 3 -> {
                    if (m[2].isLetter() && m[2].toString().lowercase() in eia96Multiplier.keys) {
                        val mult = eia96Multiplier[m[2].toString()] ?: return "Неверный ввод"
                        resistance = (eia96[m.substring(0, 2)] ?: return "Неверный ввод") * mult
                        precision = true
                    } else {
                        resistance = m.substring(0, 2).toDouble() * Math.pow(10.0, m[2].toString().toDouble())
                    }
                }
                m.length == 4 -> {
                    resistance = m.substring(0, 3).toDouble() * Math.pow(10.0, m[3].toString().toDouble())
                    precision = true
                }
                else -> return "Неверный ввод"
            }

            formatResult(resistance!!, precision)
        } catch (_: Exception) {
            "Неверный ввод"
        }
    }

    private fun formatResult(resistance: Double, precision: Boolean): String {
        val base = when {
            resistance == 0.0 -> "0 Ом (перемычка)"
            resistance < 1000 -> "${trim(resistance)} Ом"
            resistance < 1_000_000 -> "${trim(resistance / 1000)} кОм"
            else -> "${trim(resistance / 1_000_000)} МОм"
        }
        val suffix = when {
            resistance == 0.0 -> ""
            precision -> " ±1%"
            else -> " ±5%"
        }
        return "Результат: $base$suffix"
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')

    private fun JSONObject.toStringDoubleMap(): Map<String, Double> {
        val map = mutableMapOf<String, Double>()
        keys().forEach { key -> map[key] = getDouble(key) }
        return map
    }
}

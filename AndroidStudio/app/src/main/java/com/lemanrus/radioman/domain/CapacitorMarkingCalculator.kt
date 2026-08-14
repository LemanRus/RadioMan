package com.lemanrus.radioman.domain

import org.json.JSONObject

class ThCapacitorMarkingCalculator(markings: JSONObject) {
    private val decimalPoint = markings.getJSONObject("decimal_point").toStringDoubleMap()

    fun calculate(value: String): String {
        var capacity: Double? = null
        when {
            value.all { it.isDigit() } -> {
                capacity = if (value.length <= 2) {
                    value.toDouble()
                } else {
                    value.dropLast(1).toInt() * Math.pow(10.0, value.last().digitToInt().toDouble())
                }
            }
            "r" in value.lowercase() -> {
                val parts = value.lowercase().split("r")
                capacity = "${parts[0]}.${parts[1]}".toDouble()
            }
            else -> {
                val intersection = decimalPoint.keys.firstOrNull { it in value }
                if (intersection != null) {
                    val parts = value.split(intersection)
                    capacity = "${parts[0]}.${parts[1]}".toDouble() * (decimalPoint[intersection] ?: 1.0)
                } else {
                    return "Неверный ввод"
                }
            }
        }
        return "Результат: ${ValueFormatter.formatCapacitorExtended(capacity ?: return "Неверный ввод")}"
    }

    private fun JSONObject.toStringDoubleMap(): Map<String, Double> {
        val map = mutableMapOf<String, Double>()
        keys().forEach { key -> map[key] = getDouble(key) }
        return map
    }
}

class SmdCapacitorMarkingCalculator(markings: JSONObject) {
    private val voltage = markings.getJSONObject("voltage").toStringMap()
    private val smdCapacity = markings.getJSONObject("smd_capacity").toStringDoubleMap()

    fun calculate(value: String): String {
        val values = value.toList().map { it.toString() }
        var capacity: Double? = null
        var voltageStr = "?"

        when (values.size) {
            2 -> {
                if (values[0] in smdCapacity) {
                    capacity = smdCapacity[values[0]]!! * Math.pow(10.0, values[1].toDouble())
                } else return "Неверный ввод"
            }
            3 -> {
                if (values[0] in voltage) voltageStr = voltage[values[0]]!!
                else return "Неверный ввод"
                if (values[1] in smdCapacity) {
                    capacity = smdCapacity[values[1]]!! * Math.pow(10.0, values[2].toDouble())
                } else return "Неверный ввод"
            }
            4 -> {
                if (values[0] in voltage) voltageStr = voltage[values[0]]!!
                else return "Неверный ввод"
                capacity = "${values[1]}${values[2]}".toInt() * Math.pow(10.0, values[3].toDouble())
            }
            else -> return "Неверный ввод"
        }

        return "Результат: ${ValueFormatter.formatCapacitorExtended(capacity!!)}, $voltageStr В"
    }

    private fun JSONObject.toStringMap(): Map<String, String> {
        val map = mutableMapOf<String, String>()
        keys().forEach { key -> map[key] = get(key).toString() }
        return map
    }

    private fun JSONObject.toStringDoubleMap(): Map<String, Double> {
        val map = mutableMapOf<String, Double>()
        keys().forEach { key -> map[key] = getDouble(key) }
        return map
    }
}

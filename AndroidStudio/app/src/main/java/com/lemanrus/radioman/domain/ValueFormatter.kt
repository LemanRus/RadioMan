package com.lemanrus.radioman.domain

object ValueFormatter {
    const val INVALID = "Неверный ввод"

    fun formatResistor(resistance: Double): String = when {
        resistance == 0.0 -> "0 Ом (перемычка)"
        resistance < 1000 -> "${trimDouble(resistance)} Ом"
        resistance < 1_000_000 -> "${trimDouble(resistance / 1000)} кОм"
        else -> "${trimDouble(resistance / 1_000_000)} МОм"
    }

    fun formatCapacitor(capacitance: Double): String = when {
        capacitance == 0.0 -> "0 пФ (перемычка)"
        capacitance < 1000 -> "${trimDouble(capacitance)} пФ"
        capacitance < 1_000_000 -> "${trimDouble(capacitance / 1000)} нФ"
        else -> "${trimDouble(capacitance / 1_000_000)} мкФ"
    }

    fun formatCapacitorExtended(capacity: Double): String {
        return when {
            capacity == 0.0 -> "0 мкФ (перемычка)"
            capacity < 1000 -> "${trimDouble(capacity)} пФ"
            capacity < 1_000_000 -> "${trimDouble(capacity / 1000)} нФ"
            capacity < 1_000_000_000 -> "${trimDouble(capacity / 1_000_000)} мкФ"
            else -> "${trimDouble(capacity / 1_000_000_000)} мФ"
        }
    }

    private fun trimDouble(value: Double): String {
        return if (value == value.toLong().toDouble()) value.toLong().toString()
        else value.toString().trimEnd('0').trimEnd('.')
    }
}

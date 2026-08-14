package com.lemanrus.radioman.domain

object ParallelResistorCalculator {
    fun calculate(values: List<String>): String {
        return try {
            val reciprocals = values.map { 1.0 / it.toDouble() }
            val resistance = 1.0 / reciprocals.sum()
            ValueFormatter.formatResistor(resistance)
        } catch (_: NumberFormatException) {
            ValueFormatter.INVALID
        } catch (_: ArithmeticException) {
            ValueFormatter.formatResistor(0.0)
        }
    }
}

object SerialCapacitorCalculator {
    fun calculate(values: List<String>): String {
        return try {
            val reciprocals = values.map { 1.0 / it.toDouble() }
            val capacitance = 1.0 / reciprocals.sum()
            ValueFormatter.formatCapacitor(capacitance)
        } catch (_: NumberFormatException) {
            ValueFormatter.INVALID
        } catch (_: ArithmeticException) {
            ValueFormatter.formatCapacitor(0.0)
        }
    }
}

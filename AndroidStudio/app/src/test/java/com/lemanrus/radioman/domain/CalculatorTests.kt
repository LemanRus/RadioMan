package com.lemanrus.radioman.domain

import org.junit.Assert.assertEquals
import org.junit.Test

class E24NominalsTest {
    @Test
    fun standardResistor_roundTrip() {
        val result = E24Nominals.calculateStandardResistor(4700.0, true)
        assertEquals(4700.0, result, 0.01)
    }
}

class UnitConverterTest {
    @Test
    fun sameUnit_returnsValue() {
        assertEquals("10", UnitConverter.convert("10", "см", "см"))
    }

    @Test
    fun cmToMm() {
        assertEquals("100", UnitConverter.convert("10", "см", "мм"))
    }
}

class LedCalculatorTest {
    @Test
    fun lowVoltage_returnsError() {
        val result = LedCalculator.calculate("3", "3", "20", "1")
        assert(result.resistance.contains("малое"))
    }
}

class ParallelResistorCalculatorTest {
    @Test
    fun twoEqualResistors() {
        assertEquals("5 Ом", ParallelResistorCalculator.calculate(listOf("10", "10")))
    }
}

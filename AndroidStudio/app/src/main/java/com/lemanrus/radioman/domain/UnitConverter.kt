package com.lemanrus.radioman.domain

object UnitConverter {
    private val fromTo = mapOf(
        "милдюйм" to 0.001, "дюйммил" to 1000.0, "дюймсм" to 2.54,
        "смдюйм" to 0.3937007874, "сммил" to 393.7007874016, "милсм" to 0.00254,
        "сммм" to 10.0, "ммсм" to 0.1, "дюйммм" to 25.4, "ммдюйм" to 0.0393700787,
        "милмм" to 0.0254, "мил²дюйм²" to 0.000001, "дюйм²мил²" to 1000000.0,
        "дюйм²см²" to 6.4516, "см²дюйм²" to 0.15500031,
        "см²мил²" to 155000.31000062, "мил²см²" to 0.0000064516, "см²мм²" to 100.0,
        "мм²см²" to 0.01, "дюйм²мм²" to 645.16, "мм²дюйм²" to 0.0015500031,
        "мил²мм²" to 0.00064516, "круг. милмил²" to 0.7853981634,
        "мил²круг. мил" to 1.2732395447, "круг. милсм²" to 0.000005067,
        "см²круг. мил" to 197352.5241389985, "круг. милмм²" to 0.00050670748,
        "мм²круг. мил" to 1973.52524138998,
        "дюйм²круг. мил" to 1273239.5447351627, "круг. милдюйм²" to 0.0000007854,
        "Ваттэрг/с" to 10000000.0, "эрг/сВатт" to 0.0000001,
        "нФпФ" to 1000.0, "пФнФ" to 0.001, "нФмкФ" to 0.001,
        "мкФнФ" to 1000.0, "пФмкФ" to 0.000001, "мкФпФ" to 1000000.0
    )

    val allUnits = listOf(
        "мил", "дюйм", "см", "мм", "мил²", "дюйм²", "см²", "мм²",
        "круг. мил", "пФ", "нФ", "мкФ", "Ватт", "эрг/с"
    )

    fun convert(value: String, fromUnit: String, toUnit: String): String {
        return try {
            if (fromUnit == toUnit) {
                trimDouble(value.toDouble())
            } else {
                val direction = fromUnit + toUnit
                val factor = fromTo[direction]
                    ?: return "Непереводимые величины"
                trimDouble(value.toDouble() * factor)
            }
        } catch (_: NumberFormatException) {
            ValueFormatter.INVALID
        }
    }

    private fun trimDouble(value: Double): String {
        return if (value == value.toLong().toDouble()) value.toLong().toString()
        else value.toString().trimEnd('0').trimEnd('.')
    }
}

package com.lemanrus.radioman.domain

data class LedResult(
    val resistance: String,
    val e24: String,
    val power: String,
    val current: String
)

object LedCalculator {
    fun calculate(vol: String, ledVol: String, ledCur: String, ledQuant: String): LedResult {
        return try {
            val v = vol.toDouble()
            val lv = ledVol.toDouble()
            val lc = ledCur.toDouble()
            val q = ledQuant.toDouble()
            val ledResistance = (v - lv * q) / (lc / 1000.0)
            if (ledResistance < 0) {
                LedResult(
                    resistance = "Слишком малое напряжение источника питания!",
                    e24 = "",
                    power = "",
                    current = ""
                )
            } else {
                val e24Result = E24Nominals.calculateStandardResistor(ledResistance, true)
                LedResult(
                    resistance = ValueFormatter.formatResistor(ledResistance),
                    e24 = ValueFormatter.formatResistor(e24Result),
                    power = "${trim((v - lv) * lc * q)} мВт",
                    current = "${trim(lc * q)} мА"
                )
            }
        } catch (_: NumberFormatException) {
            LedResult(ValueFormatter.INVALID, ValueFormatter.INVALID, ValueFormatter.INVALID, ValueFormatter.INVALID)
        }
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')
}

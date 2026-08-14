package com.lemanrus.radioman.domain

data class DividerVoltageResult(val vOut: String, val rate: String)

data class DividerResistanceResult(
    val r2: String,
    val rate: String,
    val r2E24: String,
    val vOutE24: String
)

object VoltageDividerCalculator {
    fun calculateVOut(vin: String, r1: String, r2: String): DividerVoltageResult {
        return try {
            val v = vin.toDouble()
            val rr1 = r1.toDouble()
            val rr2 = r2.toDouble()
            val vout = rr2 * v / (rr1 + rr2)
            val rate = v / vout
            DividerVoltageResult(trim(vout), trim(rate))
        } catch (_: Exception) {
            DividerVoltageResult(ValueFormatter.INVALID, "")
        }
    }

    fun calculateR(vin: String, vout: String, r1: String): DividerResistanceResult {
        return try {
            val v = vin.toDouble()
            val vo = vout.toDouble()
            val rr1 = r1.toDouble()
            if (v <= vo) {
                DividerResistanceResult("Проверьте напряжения!", "", "", "")
            } else {
                val r2 = rr1 * vo / (v - vo)
                val rate = v / vo
                val e24 = E24Nominals.calculateStandardResistor(r2, false)
                val voutCorrected = e24 * v / (rr1 + e24)
                DividerResistanceResult(
                    r2 = formatResistance(r2),
                    rate = trim(rate),
                    r2E24 = formatResistance(e24),
                    vOutE24 = "${trim(voutCorrected)} В"
                )
            }
        } catch (_: Exception) {
            DividerResistanceResult(ValueFormatter.INVALID, "", "", "")
        }
    }

    private fun formatResistance(r2: Double): String = when {
        r2 == 0.0 -> "0 Ом (перемычка)"
        r2 < 1000 -> "${trim(r2)} Ом"
        r2 < 1_000_000 -> "${trim(r2 / 1000)} кОм"
        else -> "${trim(r2 / 1_000_000)} МОм"
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')
}

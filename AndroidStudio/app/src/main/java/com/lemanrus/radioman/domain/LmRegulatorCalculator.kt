package com.lemanrus.radioman.domain

import kotlin.math.pow

data class LmVoltageResult(
    val r2: String,
    val r2Corrected: String,
    val vOut: String,
    val recommend: String,
    val power: String,
    val error: String? = null
)

data class LmCurrentResult(
    val r1: String,
    val r1Corrected: String,
    val r1Power: String,
    val r1PowerCorrected: String,
    val iOutCorrected: String,
    val recommend: String,
    val vin: String,
    val error: String? = null
)

object LmRegulatorCalculator {
    private const val HIGH_CURRENT = "Ток нагрузки должен быть меньше 5А!"

    fun calculateVoltage(vout: String, r1: String, iout: String, vin: String): LmVoltageResult {
        return try {
            val vo = vout.toDouble()
            val rr1 = r1.toDouble()
            val io = iout.toDouble()
            vin.toDouble()
            if (io > 5) {
                LmVoltageResult("", "", "", "", "", HIGH_CURRENT)
            } else {
                val r2 = rr1 * (vo / 1.25 - 1)
                val r2Corrected = E24Nominals.calculateStandardResistor(r2, false)
                val power = (vin.toDouble() - vo) * io
                val voutCorrected = 1.25 * (1 + r2Corrected / rr1)
                val recommend = when {
                    io > 3 -> "LM338"
                    io > 1.5 -> "LM350"
                    else -> "LM317"
                }
                LmVoltageResult(
                    r2 = ValueFormatter.formatResistor(r2),
                    r2Corrected = ValueFormatter.formatResistor(r2Corrected),
                    vOut = "${trim(voutCorrected)} В",
                    recommend = recommend,
                    power = "${trim(power)} Вт"
                )
            }
        } catch (_: Exception) {
            LmVoltageResult(
                ValueFormatter.INVALID, ValueFormatter.INVALID, ValueFormatter.INVALID,
                ValueFormatter.INVALID, ValueFormatter.INVALID
            )
        }
    }

    fun calculateCurrent(iout: String, vout: String?): LmCurrentResult {
        return try {
            val io = iout.toDouble()
            if (io > 5) {
                LmCurrentResult("", "", "", "", "", "", "", HIGH_CURRENT)
            } else {
                val r1 = 1.25 / io
                val r1Corrected = E24Nominals.calculateStandardResistor(r1, true)
                val recommend = when {
                    io > 3 -> "LM338"
                    io > 1.5 -> "LM350"
                    else -> "LM317"
                }
                val ioutCorrected = 1.25 / r1Corrected
                val powerR1 = io.pow(2) * r1
                val powerCorrected = ioutCorrected.pow(2) * r1Corrected
                val vinText = if (!vout.isNullOrBlank()) {
                    val vo = vout.toDouble()
                    if (vo !in 3.0..38.0) {
                        "Падение напряжения должно быть больше 2В и меньше 38В!"
                    } else {
                        "${trim(vo + 3.7)} В"
                    }
                } else ""
                LmCurrentResult(
                    r1 = ValueFormatter.formatResistor(r1),
                    r1Corrected = ValueFormatter.formatResistor(r1Corrected),
                    r1Power = "${trim(powerR1)} Вт",
                    r1PowerCorrected = "${trim(powerCorrected)} Вт",
                    iOutCorrected = "${trim(ioutCorrected * 1000)} мА",
                    recommend = recommend,
                    vin = vinText
                )
            }
        } catch (_: Exception) {
            LmCurrentResult(
                ValueFormatter.INVALID, ValueFormatter.INVALID, ValueFormatter.INVALID,
                ValueFormatter.INVALID, ValueFormatter.INVALID, ValueFormatter.INVALID,
                ValueFormatter.INVALID
            )
        }
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')
}

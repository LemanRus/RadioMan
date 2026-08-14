package com.lemanrus.radioman.domain

import kotlin.math.ln
import kotlin.math.pow
import kotlin.math.sqrt

object InductorCalculator {
    fun calculateHenrys(turns: String, diameter: String, length: String): String {
        return try {
            val t = turns.toDouble()
            val d = diameter.toDouble()
            val l = length.toDouble()
            val formFactor = l / d
            val induction = 0.0002 * Math.PI * d * t.pow(2) * (
                ln(1 + Math.PI / (2 * formFactor)) + 1 / (
                    2.3004 + 3.437 * formFactor + 1.7636 * formFactor.pow(2) -
                        0.47 / (0.755 + 1 / formFactor).pow(1.44)
                    )
                )
            return "${trim(induction)} мкГн"
        } catch (_: Exception) {
            ValueFormatter.INVALID
        }
    }

    data class SizeResult(
        val length: String,
        val lengthInt: String,
        val turns: String,
        val turnsInt: String
    )

    fun calculateTurns(henrys: String, diameter: String, oneTurn: String): SizeResult {
        return try {
            val h = henrys.toDouble()
            val d = diameter.toDouble() / 10.0
            val ot = oneTurn.toDouble() / 10.0
            val inductorLength = (
                50 * ot.pow(2) * h + sqrt(5.0) * sqrt(
                    500 * ot.pow(4) * h.pow(2) + 9 * ot.pow(2) * d.pow(3) * h
                )
                ) / d.pow(2)
            val inductorTurns = inductorLength / ot
            val inductorTurnsInt = kotlin.math.round(inductorTurns)
            val inductorLengthInt = inductorTurnsInt * ot * 10
            SizeResult(
                length = "${trim(inductorLength * 10)} мм",
                lengthInt = "${trim(inductorLengthInt)} мм",
                turns = "${trim(inductorTurns)} витка(ов)",
                turnsInt = "${trim(inductorTurnsInt)} витка(ов)"
            )
        } catch (_: Exception) {
            val err = ValueFormatter.INVALID
            SizeResult(err, err, err, err)
        }
    }

    private fun trim(v: Double): String =
        if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString().trimEnd('0').trimEnd('.')
}

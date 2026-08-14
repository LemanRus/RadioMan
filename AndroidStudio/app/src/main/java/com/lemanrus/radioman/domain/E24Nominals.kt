package com.lemanrus.radioman.domain

object E24Nominals {
    private val E24 = doubleArrayOf(
        1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3,
        3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    )

    fun calculateStandardResistor(resistance: Double, goUp: Boolean): Double {
        if (resistance >= 1) {
            var res = resistance
            while (res >= 10) res /= 10.0
            val listOfDiffs = E24.map { kotlin.math.abs(res - it) }
            var resultIndex = listOfDiffs.indexOf(listOfDiffs.minOrNull()!!)
            var interact = resistance / E24[resultIndex]
            var power = 0
            while (interact >= 9) {
                power++
                interact /= 10.0
            }
            var e24Result = E24[resultIndex] * Math.pow(10.0, power.toDouble())
            if (goUp && e24Result < resistance) {
                e24Result = if (resultIndex != E24.lastIndex) {
                    E24[resultIndex + 1] * Math.pow(10.0, power.toDouble())
                } else {
                    E24[0] * Math.pow(10.0, (power + 1).toDouble())
                }
            }
            return e24Result
        } else {
            var r = resistance
            var power = 0
            while (r < 1) {
                r *= 10.0
                power++
            }
            val listOfDiffs = E24.map { kotlin.math.abs(r - it) }
            val resultIndex = listOfDiffs.indexOf(listOfDiffs.minOrNull()!!)
            return E24[resultIndex] * Math.pow(10.0, -power.toDouble())
        }
    }
}

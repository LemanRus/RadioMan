package com.lemanrus.radioman.ui.calculations

import android.view.inputmethod.EditorInfo
import android.widget.LinearLayout
import android.widget.TextView
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.lemanrus.radioman.R
import com.lemanrus.radioman.domain.InductorCalculator
import com.lemanrus.radioman.domain.LedCalculator
import com.lemanrus.radioman.domain.LmRegulatorCalculator
import com.lemanrus.radioman.domain.ParallelResistorCalculator
import com.lemanrus.radioman.domain.SerialCapacitorCalculator
import com.lemanrus.radioman.domain.VoltageDividerCalculator
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

private fun android.view.View.fieldHint(hint: String): TextInputEditText {
    val layout = TextInputLayout(context).apply {
        this.hint = hint
        layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { bottomMargin = 16 }
    }
    val edit = TextInputEditText(context).apply {
        gravity = android.view.Gravity.CENTER
        inputType = android.text.InputType.TYPE_CLASS_NUMBER or
            android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL
        imeOptions = EditorInfo.IME_ACTION_DONE
    }
    layout.addView(edit)
    findViewById<LinearLayout>(R.id.calcContainer).addView(layout)
    return edit
}

private fun android.view.View.resultLabel(): TextView {
    return TextView(context).apply {
        layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        ).apply { topMargin = 16 }
        gravity = android.view.Gravity.CENTER
    }.also { findViewById<LinearLayout>(R.id.calcContainer).addView(it) }
}

private fun android.view.View.calcButton(onClick: () -> Unit): MaterialButton {
    return MaterialButton(context).apply {
        text = context.getString(R.string.calculate)
        setOnClickListener { onClick() }
    }.also { findViewById<LinearLayout>(R.id.calcContainer).addView(it) }
}

class LedResistorFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.led_title
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val vol = view.fieldHint("Напряжение источника, В")
        val ledVol = view.fieldHint("Напряжение LED, В")
        val ledCur = view.fieldHint("Ток LED, мА")
        val ledQuant = view.fieldHint("Количество LED")
        val r1 = view.resultLabel()
        val e24 = view.resultLabel()
        val power = view.resultLabel()
        val cur = view.resultLabel()
        view.calcButton {
            val res = LedCalculator.calculate(
                vol.text.toString(), ledVol.text.toString(),
                ledCur.text.toString(), ledQuant.text.toString()
            )
            r1.text = res.resistance
            e24.text = res.e24
            power.text = res.power
            cur.text = res.current
        }
    }
}

class InductorInductionFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.inductor_by_params
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val turns = view.fieldHint("Число витков")
        val diameter = view.fieldHint("Диаметр, мм")
        val length = view.fieldHint("Длина, мм")
        val result = view.resultLabel()
        view.calcButton {
            result.text = InductorCalculator.calculateHenrys(
                turns.text.toString(), diameter.text.toString(), length.text.toString()
            )
        }
    }
}

class InductorSizeFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.inductor_by_inductance
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val henrys = view.fieldHint("Индуктивность, мкГн")
        val diameter = view.fieldHint("Диаметр, мм")
        val oneTurn = view.fieldHint("Шаг намотки, мм")
        val l1 = view.resultLabel()
        val l2 = view.resultLabel()
        val t1 = view.resultLabel()
        val t2 = view.resultLabel()
        view.calcButton {
            val res = InductorCalculator.calculateTurns(
                henrys.text.toString(), diameter.text.toString(), oneTurn.text.toString()
            )
            l1.text = res.length
            l2.text = res.lengthInt
            t1.text = res.turns
            t2.text = res.turnsInt
        }
    }
}

class ParallelResistorFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    private val inputs = mutableListOf<TextInputEditText>()
    private lateinit var resultView: TextView
    private lateinit var fieldsContainer: LinearLayout

    override fun screenTitleRes() = R.string.parallel_resistor_title

    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        fieldsContainer = LinearLayout(requireContext()).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
        }
        val container = view.findViewById<LinearLayout>(R.id.calcContainer)
        container.addView(fieldsContainer)
        resultView = view.resultLabel()
        addResistorField("Резистор 1, Ом")
        addResistorField("Резистор 2, Ом")
        var counter = 2
        MaterialButton(requireContext()).apply {
            text = getString(R.string.add)
            setOnClickListener {
                counter++
                addResistorField("Резистор $counter, Ом")
            }
        }.also { container.addView(it, container.indexOfChild(resultView)) }
        view.calcButton {
            resultView.text = ParallelResistorCalculator.calculate(inputs.map { it.text.toString() })
        }
    }

    private fun addResistorField(label: String) {
        val layout = TextInputLayout(requireContext()).apply {
            hint = label
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply { bottomMargin = 16 }
        }
        val edit = TextInputEditText(requireContext()).apply {
            gravity = android.view.Gravity.CENTER
            inputType = android.text.InputType.TYPE_CLASS_NUMBER or
                android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL
        }
        layout.addView(edit)
        fieldsContainer.addView(layout)
        inputs.add(edit)
    }
}

class SerialCapacitorFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    private val inputs = mutableListOf<TextInputEditText>()
    override fun screenTitleRes() = R.string.serial_capacitor_title
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val result = view.resultLabel()
        fun addField(label: String) { inputs.add(view.fieldHint(label)) }
        addField("Конденсатор 1, пФ")
        addField("Конденсатор 2, пФ")
        view.calcButton {
            result.text = SerialCapacitorCalculator.calculate(inputs.map { it.text.toString() })
        }
    }
}

class VoltageDividerVoltageFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.divider_by_voltage
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val vin = view.fieldHint("Vin, В")
        val r1 = view.fieldHint("R1, Ом")
        val r2 = view.fieldHint("R2, Ом")
        val vout = view.resultLabel()
        val rate = view.resultLabel()
        view.calcButton {
            val res = VoltageDividerCalculator.calculateVOut(vin.text.toString(), r1.text.toString(), r2.text.toString())
            vout.text = "Vout: ${res.vOut}"
            rate.text = "K: ${res.rate}"
        }
    }
}

class VoltageDividerResistanceFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.divider_by_resistance
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val vin = view.fieldHint("Vin, В")
        val vout = view.fieldHint("Vout, В")
        val r1 = view.fieldHint("R1, Ом")
        val r2 = view.resultLabel()
        val rate = view.resultLabel()
        val e24 = view.resultLabel()
        val corrected = view.resultLabel()
        view.calcButton {
            val res = VoltageDividerCalculator.calculateR(vin.text.toString(), vout.text.toString(), r1.text.toString())
            r2.text = "R2: ${res.r2}"
            rate.text = "K: ${res.rate}"
            e24.text = "E24: ${res.r2E24}"
            corrected.text = "Vout E24: ${res.vOutE24}"
        }
    }
}

class LmRegulatorVoltageFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.lm_voltage
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val vout = view.fieldHint("Vout, В")
        val r1 = view.fieldHint("R1, Ом")
        val iout = view.fieldHint("Iout, А")
        val vin = view.fieldHint("Vin, В")
        val r2 = view.resultLabel()
        val r2c = view.resultLabel()
        val vo = view.resultLabel()
        val rec = view.resultLabel()
        val power = view.resultLabel()
        view.calcButton {
            val res = LmRegulatorCalculator.calculateVoltage(
                vout.text.toString(), r1.text.toString(), iout.text.toString(), vin.text.toString()
            )
            if (res.error != null) {
                r2.text = res.error
            } else {
                r2.text = "R2: ${res.r2}"
                r2c.text = "R2 E24: ${res.r2Corrected}"
                vo.text = res.vOut
                rec.text = res.recommend
                power.text = res.power
            }
        }
    }
}

class LmRegulatorCurrentFragment : ToolbarContentFragment(R.layout.fragment_calc_scroll) {
    override fun screenTitleRes() = R.string.lm_current
    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val iout = view.fieldHint("Iout, А")
        val vout = view.fieldHint("Vout, В (необязательно)")
        val r1 = view.resultLabel()
        val r1c = view.resultLabel()
        val p1 = view.resultLabel()
        val p1c = view.resultLabel()
        val ic = view.resultLabel()
        val rec = view.resultLabel()
        val vin = view.resultLabel()
        view.calcButton {
            val vo = vout.text?.toString()?.trim().orEmpty()
            val res = LmRegulatorCalculator.calculateCurrent(iout.text.toString(), vo.ifEmpty { null })
            if (res.error != null) {
                r1.text = res.error
            } else {
                r1.text = "R1: ${res.r1}"
                r1c.text = "R1 E24: ${res.r1Corrected}"
                p1.text = res.r1Power
                p1c.text = res.r1PowerCorrected
                ic.text = res.iOutCorrected
                rec.text = res.recommend
                vin.text = res.vin
            }
        }
    }
}

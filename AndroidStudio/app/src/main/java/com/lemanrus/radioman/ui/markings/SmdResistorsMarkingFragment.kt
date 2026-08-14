package com.lemanrus.radioman.ui.markings

import android.view.inputmethod.EditorInfo
import android.widget.TextView
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.lemanrus.radioman.R
import com.lemanrus.radioman.data.DataRepository
import com.lemanrus.radioman.domain.SmdResistorMarkingCalculator
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class SmdResistorsMarkingFragment : ToolbarContentFragment(R.layout.fragment_smd_marking) {

    private lateinit var calculator: SmdResistorMarkingCalculator

    override fun screenTitleRes() = R.string.smd_resistors

    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        calculator = SmdResistorMarkingCalculator(
            DataRepository.getInstance(requireContext()).loadSmdResistorMarkings()
        )
        val input = view.findViewById<TextInputEditText>(R.id.markingInput)
        val result = view.findViewById<TextView>(R.id.resultText)
        val calc = {
            result.text = calculator.calculate(input.text?.toString()?.trim().orEmpty())
        }
        view.findViewById<MaterialButton>(R.id.calculateButton).setOnClickListener { calc() }
        input.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { calc(); true } else false
        }
    }
}

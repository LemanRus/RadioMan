package com.lemanrus.radioman.ui.calculations

import android.text.Editable
import android.text.TextWatcher
import android.widget.ArrayAdapter
import android.widget.Spinner
import android.widget.TextView
import com.google.android.material.textfield.TextInputEditText
import com.lemanrus.radioman.R
import com.lemanrus.radioman.domain.UnitConverter
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class ConverterFragment : ToolbarContentFragment(R.layout.fragment_converter) {

    override fun screenTitleRes() = R.string.converter_title

    override fun onViewCreated(view: android.view.View, savedInstanceState: android.os.Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val units = UnitConverter.allUnits
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_dropdown_item, units)
        val from = view.findViewById<Spinner>(R.id.fromUnitSpinner)
        val to = view.findViewById<Spinner>(R.id.toUnitSpinner)
        from.adapter = adapter
        to.adapter = adapter
        val input = view.findViewById<TextInputEditText>(R.id.valueInput)
        val result = view.findViewById<TextView>(R.id.resultText)
        val calc = {
            result.text = UnitConverter.convert(
                input.text?.toString()?.trim().orEmpty(),
                from.selectedItem.toString(),
                to.selectedItem.toString()
            )
        }
        val watcher = object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) { calc() }
            override fun afterTextChanged(s: Editable?) {}
        }
        input.addTextChangedListener(watcher)
        from.onItemSelectedListener = simpleListener { calc() }
        to.onItemSelectedListener = simpleListener { calc() }
    }

    private fun simpleListener(block: () -> Unit) = object : android.widget.AdapterView.OnItemSelectedListener {
        override fun onItemSelected(parent: android.widget.AdapterView<*>?, v: android.view.View?, pos: Int, id: Long) = block()
        override fun onNothingSelected(parent: android.widget.AdapterView<*>?) {}
    }
}

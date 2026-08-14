package com.lemanrus.radioman.ui.markings

import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.LinearLayout
import android.widget.TextView
import com.lemanrus.radioman.R
import com.lemanrus.radioman.data.DataRepository
import com.lemanrus.radioman.domain.ThResistorMarkingCalculator
import com.lemanrus.radioman.ui.common.ResistorBandView
import com.lemanrus.radioman.ui.common.ResistorColor
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class ThResistorsMarkingFragment : ToolbarContentFragment(R.layout.fragment_th_resistors) {

    private lateinit var calculator: ThResistorMarkingCalculator
    private val bandViews = mutableListOf<ResistorBandView>()
    private var bandCount = 3

    override fun screenTitleRes() = R.string.th_resistors

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        calculator = ThResistorMarkingCalculator(
            DataRepository.getInstance(requireContext()).loadResistorMarkings()
        )
        val spinner = view.findViewById<android.widget.Spinner>(R.id.bandCountSpinner)
        spinner.adapter = ArrayAdapter(
            requireContext(),
            android.R.layout.simple_spinner_dropdown_item,
            listOf("3", "4", "5", "6")
        )
        spinner.setSelection(0)
        spinner.onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: android.widget.AdapterView<*>?, v: View?, pos: Int, id: Long) {
                bandCount = pos + 3
                rebuildBands(view)
            }
            override fun onNothingSelected(parent: android.widget.AdapterView<*>?) {}
        }
        rebuildBands(view)
    }

    private fun rebuildBands(view: View) {
        val container = view.findViewById<LinearLayout>(R.id.bandsContainer)
        container.removeAllViews()
        bandViews.clear()
        repeat(bandCount) { index ->
            val band = ResistorBandView(requireContext()).apply {
                layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.MATCH_PARENT, 1f).apply {
                    marginStart = 4
                    marginEnd = 4
                }
                configure(index, bandCount, ResistorColor.BLACK)
                onColorChanged = { calculate(view) }
            }
            bandViews.add(band)
            container.addView(band)
        }
        calculate(view)
    }

    private fun calculate(view: View) {
        val colors = bandViews.map { it.selectedColor.displayName }
        val result = calculator.calculate(colors, bandCount)
        view.findViewById<TextView>(R.id.resultText).text = result
    }
}

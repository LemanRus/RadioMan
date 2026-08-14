package com.lemanrus.radioman.ui.handbook

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.lemanrus.radioman.R
import com.lemanrus.radioman.data.DataRepository
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class ChipsAnalogsFragment : ToolbarContentFragment(R.layout.fragment_chips_analogs) {

    override fun screenTitleRes() = R.string.chips_analogs

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val seriesKey = arguments?.getString("seriesKey").orEmpty()
        val seriesTitle = arguments?.getString("seriesTitle").orEmpty()
        if (seriesTitle.isNotEmpty()) {
            (activity as? com.lemanrus.radioman.MainActivity)?.updateToolbarTitle(seriesTitle)
        }

        val overlay = view.findViewById<View>(R.id.loadingOverlay)
        val content = view.findViewById<View>(R.id.contentScroll)
        val recycler = view.findViewById<RecyclerView>(R.id.analogsRecycler)

        overlay.isVisible = true
        content.isVisible = false

        view.post {
            val chipsRoot = DataRepository.getInstance(requireContext()).loadChipsAnalogs()
            val seriesObj = chipsRoot.optJSONObject(seriesKey)
            val pairs = mutableListOf<Pair<String, String>>()
            seriesObj?.keys()?.forEach { key ->
                pairs.add(key to seriesObj.getString(key))
            }
            recycler.layoutManager = LinearLayoutManager(requireContext())
            recycler.adapter = AnalogAdapter(pairs)
            overlay.isVisible = false
            content.isVisible = true
        }
    }
}

private class AnalogAdapter(
    private val items: List<Pair<String, String>>
) : RecyclerView.Adapter<AnalogAdapter.Holder>() {

    class Holder(view: View) : RecyclerView.ViewHolder(view) {
        val domestic: TextView = view.findViewById(R.id.domesticName)
        val foreign: TextView = view.findViewById(R.id.foreignName)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_chip_analog, parent, false)
        return Holder(view)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val (domestic, foreign) = items[position]
        holder.domestic.text = domestic
        holder.foreign.text = foreign
    }

    override fun getItemCount(): Int = items.size
}

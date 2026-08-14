package com.lemanrus.radioman.ui.handbook

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.view.isVisible
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.lemanrus.radioman.R
import com.lemanrus.radioman.data.DataRepository
import com.lemanrus.radioman.data.SeriesNames
import com.lemanrus.radioman.databinding.ItemSectionCardBinding
import com.lemanrus.radioman.ui.common.NavOptionsHelper
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class ChipsAnalogsSelectFragment : ToolbarContentFragment(R.layout.fragment_chips_select) {

    override fun screenTitleRes() = R.string.chips_analogs

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val overlay = view.findViewById<View>(R.id.loadingOverlay)
        val content = view.findViewById<View>(R.id.contentScroll)
        val recycler = view.findViewById<RecyclerView>(R.id.seriesRecycler)

        overlay.isVisible = true
        content.isVisible = false

        view.post {
            val chipsData = DataRepository.getInstance(requireContext()).loadChipsAnalogs()
            val keys = SeriesNames.sortedKeys(chipsData.keys().asSequence().toSet())
            val titles = keys.map { SeriesNames.getDisplayName(it) }
            recycler.layoutManager = LinearLayoutManager(requireContext())
            recycler.adapter = SeriesListAdapter(keys, titles) { seriesKey, title ->
                findNavController().navigate(
                    R.id.chipsAnalogsFragment,
                    Bundle().apply {
                        putString("seriesKey", seriesKey)
                        putString("seriesTitle", title)
                    },
                    NavOptionsHelper.forward()
                )
            }
            overlay.isVisible = false
            content.isVisible = true
        }
    }
}

private class SeriesListAdapter(
    private val seriesKeys: List<String>,
    private val titles: List<String>,
    private val onClick: (String, String) -> Unit
) : RecyclerView.Adapter<SeriesListAdapter.Holder>() {

    class Holder(val binding: ItemSectionCardBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemSectionCardBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val key = seriesKeys[position]
        val resId = holder.itemView.resources.getIdentifier(
            key, "drawable", holder.itemView.context.packageName
        )
        holder.binding.cardIcon.setImageResource(
            if (resId != 0) resId else R.drawable.series_noname
        )
        holder.binding.cardTitle.text = titles[position]
        holder.binding.root.setOnClickListener {
            onClick(key, titles[position])
        }
    }

    override fun getItemCount(): Int = seriesKeys.size
}

package com.lemanrus.radioman.ui.common

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.lemanrus.radioman.databinding.ItemSectionCardBinding

class SectionCardAdapter(
    private val items: List<SectionCardItem>,
    private val onClick: (SectionCardItem) -> Unit
) : RecyclerView.Adapter<SectionCardAdapter.ViewHolder>() {

    class ViewHolder(val binding: ItemSectionCardBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemSectionCardBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = items[position]
        holder.binding.cardIcon.setImageResource(item.iconRes)
        holder.binding.cardTitle.text = item.title
        holder.binding.root.setOnClickListener { onClick(item) }
    }

    override fun getItemCount(): Int = items.size
}

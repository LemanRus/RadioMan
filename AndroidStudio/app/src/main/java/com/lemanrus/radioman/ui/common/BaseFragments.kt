package com.lemanrus.radioman.ui.common

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.annotation.LayoutRes
import androidx.annotation.StringRes
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.lemanrus.radioman.MainActivity

abstract class ToolbarContentFragment(@LayoutRes private val layoutRes: Int) : Fragment() {

    @StringRes
    abstract fun screenTitleRes(): Int

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View = inflater.inflate(layoutRes, container, false)

    override fun onResume() {
        super.onResume()
        (activity as? MainActivity)?.updateToolbar(screenTitleRes(), showBack = true)
    }
}

abstract class PlaceholderFragment : Fragment() {

    @StringRes
    abstract fun screenTitleRes(): Int

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(com.lemanrus.radioman.R.layout.fragment_placeholder, container, false)
    }

    override fun onResume() {
        super.onResume()
        (activity as? MainActivity)?.updateToolbar(screenTitleRes(), showBack = true)
    }
}

abstract class SectionListFragment : Fragment() {

    @StringRes
    abstract fun screenTitleRes(): Int

    abstract fun cardItems(): List<SectionCardItem>

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(com.lemanrus.radioman.R.layout.fragment_section_list, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val recycler = view.findViewById<androidx.recyclerview.widget.RecyclerView>(
            com.lemanrus.radioman.R.id.sectionRecycler
        )
        recycler.layoutManager = androidx.recyclerview.widget.LinearLayoutManager(requireContext())
        recycler.adapter = SectionCardAdapter(cardItems()) { item ->
            findNavController().navigate(item.destinationId, null, NavOptionsHelper.forward())
        }
    }

    override fun onResume() {
        super.onResume()
        (activity as? MainActivity)?.updateToolbar(
            screenTitleRes(),
            showBack = !isRootTab()
        )
    }

    private fun isRootTab(): Boolean {
        return this::class.simpleName in listOf(
            "MarkingsFragment", "CalculationsFragment", "HandbookFragment", "HelpFragment"
        )
    }
}

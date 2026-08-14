package com.lemanrus.radioman.ui.help

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.text.SpannableString
import android.text.Spanned
import android.text.TextPaint
import android.text.method.LinkMovementMethod
import android.text.style.ClickableSpan
import android.view.View
import android.widget.TextView
import androidx.core.content.ContextCompat
import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class AboutFragment : ToolbarContentFragment(R.layout.fragment_about) {

    override fun screenTitleRes() = R.string.about

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val linkColor = ContextCompat.getColor(requireContext(), R.color.lavender_primary)

        val about = view.findViewById<TextView>(R.id.aboutText)
        about.text = spannableWithLink(
            text = getString(R.string.about_text),
            link = getString(R.string.email),
            color = linkColor
        ) {
            startActivity(Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:electronics@hand-made-tlt.ru")))
        }
        about.movementMethod = LinkMovementMethod.getInstance()

        val git = view.findViewById<TextView>(R.id.gitLink)
        git.text = spannableWithLink(
            text = getString(R.string.source_code),
            link = getString(R.string.source_code),
            color = linkColor
        ) {
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://github.com/LemanRus/RadioMan")))
        }
        git.movementMethod = LinkMovementMethod.getInstance()

        val donation = view.findViewById<TextView>(R.id.donationText)
        donation.text = spannableWithLink(
            text = getString(R.string.about_donation),
            link = getString(R.string.support_author),
            color = linkColor
        ) {
            startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://yoomoney.ru/to/410011259431654")))
        }
        donation.movementMethod = LinkMovementMethod.getInstance()
    }

    private fun spannableWithLink(
        text: String,
        link: String,
        color: Int,
        onClick: () -> Unit
    ): SpannableString {
        val spannable = SpannableString(text)
        val start = text.indexOf(link)
        if (start < 0) return spannable
        val end = start + link.length
        spannable.setSpan(object : ClickableSpan() {
            override fun onClick(widget: View) = onClick()
            override fun updateDrawState(ds: TextPaint) {
                super.updateDrawState(ds)
                ds.color = color
                ds.isUnderlineText = true
            }
        }, start, end, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        return spannable
    }
}

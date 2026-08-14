package com.lemanrus.radioman

import android.app.Application
import com.lemanrus.radioman.data.DataRepository

class RadioManApp : Application() {
    override fun onCreate() {
        super.onCreate()
        DataRepository.getInstance(this)
    }
}

package com.lemanrus.radioman.data

import android.content.Context
import org.json.JSONObject

class DataRepository private constructor(context: Context) {

    private val assets = context.applicationContext.assets
    private val cache = mutableMapOf<String, JSONObject>()

    private fun loadJson(path: String): JSONObject {
        cache[path]?.let { return it }
        val json = assets.open(path).bufferedReader().use { it.readText() }
        return JSONObject(json).also { cache[path] = it }
    }

    fun loadChipsAnalogs(): JSONObject = loadJson("data/chips_analogs.json")

    fun loadResistorMarkings(): JSONObject = loadJson("data/resistor_markings.json")

    fun loadSmdResistorMarkings(): JSONObject = loadJson("data/smd_resistor_markings.json")

    fun loadCapacitorMarkings(): JSONObject = loadJson("data/capacitor_markings.json")

    fun clearCache() = cache.clear()

    companion object {
        @Volatile
        private var instance: DataRepository? = null

        fun getInstance(context: Context): DataRepository {
            return instance ?: synchronized(this) {
                instance ?: DataRepository(context).also { instance = it }
            }
        }
    }
}

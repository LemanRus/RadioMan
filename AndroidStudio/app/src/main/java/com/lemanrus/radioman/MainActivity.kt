package com.lemanrus.radioman

import android.os.Bundle
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.lemanrus.radioman.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var appBarConfiguration: AppBarConfiguration

    private val topLevelDestinations = setOf(
        R.id.markingsFragment,
        R.id.calculationsFragment,
        R.id.handbookFragment,
        R.id.helpFragment
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)

        val navHost = supportFragmentManager
            .findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        val navController = navHost.navController

        appBarConfiguration = AppBarConfiguration(topLevelDestinations)
        setupActionBarWithNavController(navController, appBarConfiguration)

        binding.bottomNavigation.setupWithNavController(navController)

        navController.addOnDestinationChangedListener { _, destination, _ ->
            val isTopLevel = destination.id in topLevelDestinations
            if (isTopLevel) {
                supportActionBar?.title = destination.label
                binding.toolbar.navigationIcon = null
            }
        }

        binding.toolbar.setNavigationOnClickListener {
            if (!navController.navigateUp(appBarConfiguration)) {
                onBackPressedDispatcher.onBackPressed()
            }
        }
    }

    fun updateToolbarTitle(title: String) {
        supportActionBar?.title = title
        binding.toolbar.navigationIcon = getDrawable(R.drawable.ic_arrow_back)
    }

    fun updateToolbar(@StringRes titleRes: Int, showBack: Boolean) {
        supportActionBar?.title = getString(titleRes)
        if (showBack) {
            binding.toolbar.navigationIcon = getDrawable(R.drawable.ic_arrow_back)
        } else {
            binding.toolbar.navigationIcon = null
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        val navHost = supportFragmentManager
            .findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        return navHost.navController.navigateUp(appBarConfiguration) || super.onSupportNavigateUp()
    }
}

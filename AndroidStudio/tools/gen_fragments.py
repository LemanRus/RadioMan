#!/usr/bin/env python3
"""Generate Android fragment Kotlin files and nav_graph.xml"""
from pathlib import Path

BASE = Path(r"c:\Users\Admin\Projects\RadioMan\AndroidStudio\app\src\main")

FRAGMENTS = [
    ("markings", "MarkingsFragment", "fragment_section_list", "tab_markings", False, []),
    ("markings", "ResistorsMarkingSelectFragment", "fragment_section_list", "resistors", True, []),
    ("markings", "ThResistorsMarkingFragment", "fragment_th_resistors", "th_resistors", True, []),
    ("markings", "SmdResistorsMarkingFragment", "fragment_smd_marking", "smd_resistors", True, []),
    ("markings", "CapacitorsMarkingSelectFragment", "fragment_section_list", "capacitors", True, []),
    ("markings", "ThCapacitorsMarkingFragment", "fragment_th_capacitors", "th_capacitors", True, []),
    ("markings", "SmdCapacitorsMarkingFragment", "fragment_smd_marking", "smd_capacitors", True, []),
    ("calculations", "CalculationsFragment", "fragment_section_list", "tab_calculations", False, []),
    ("calculations", "ConverterFragment", "fragment_converter", "converter_title", True, []),
    ("calculations", "LedResistorFragment", "fragment_led", "led_title", True, []),
    ("calculations", "InductorSelectFragment", "fragment_section_list", "inductor_select_title", True, []),
    ("calculations", "InductorInductionFragment", "fragment_inductor_induction", "inductor_by_params", True, []),
    ("calculations", "InductorSizeFragment", "fragment_inductor_size", "inductor_by_inductance", True, []),
    ("calculations", "ParallelResistorFragment", "fragment_parallel_resistor", "parallel_resistor_title", True, []),
    ("calculations", "SerialCapacitorFragment", "fragment_serial_capacitor", "serial_capacitor_title", True, []),
    ("calculations", "VoltageDividerSelectFragment", "fragment_section_list", "voltage_divider_title", True, []),
    ("calculations", "VoltageDividerVoltageFragment", "fragment_divider_voltage", "divider_by_voltage", True, []),
    ("calculations", "VoltageDividerResistanceFragment", "fragment_divider_resistance", "divider_by_resistance", True, []),
    ("calculations", "LmRegulatorSelectFragment", "fragment_section_list", "lm_regulator_title", True, []),
    ("calculations", "LmRegulatorVoltageFragment", "fragment_lm_voltage", "lm_voltage", True, []),
    ("calculations", "LmRegulatorCurrentFragment", "fragment_lm_current", "lm_current", True, []),
    ("handbook", "HandbookFragment", "fragment_section_list", "tab_handbook", False, []),
    ("handbook", "TheoryFragment", "fragment_placeholder", "theory", True, []),
    ("handbook", "SchematicsFragment", "fragment_placeholder", "schematics", True, []),
    ("handbook", "PinoutFragment", "fragment_placeholder", "pinout", True, []),
    ("handbook", "ConnectionsFragment", "fragment_placeholder", "connections", True, []),
    ("handbook", "ChipsFragment", "fragment_section_list", "chips", True, []),
    ("handbook", "ChipsAnalogsSelectFragment", "fragment_chips_select", "chips_analogs", True, []),
    ("handbook", "ChipsAnalogsFragment", "fragment_chips_analogs", "chips_analogs", True, []),
    ("handbook", "LifehacksFragment", "fragment_placeholder", "lifehacks", True, []),
    ("help", "HelpFragment", "fragment_section_list", "tab_help", False, []),
    ("help", "HowToFragment", "fragment_how_to", "how_to", True, []),
    ("help", "AboutFragment", "fragment_about", "about", True, []),
]

def camel_to_id(name):
    import re
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower().replace('_fragment', 'Fragment').replace('fragment', '')
    # MarkingsFragment -> markings_fragment

def frag_id(class_name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2[0].lower() + s2[1:] if s2 else s2

for pkg, cls, layout, title, _, _ in FRAGMENTS:
    fid = frag_id(cls)
    pkg_path = BASE / "java/com/lemanrus/radioman/ui" / pkg
    pkg_path.mkdir(parents=True, exist_ok=True)
    if cls in ("MarkingsFragment", "CalculationsFragment", "HandbookFragment", "HelpFragment",
               "ResistorsMarkingSelectFragment", "CapacitorsMarkingSelectFragment",
               "InductorSelectFragment", "VoltageDividerSelectFragment", "LmRegulatorSelectFragment",
               "ChipsFragment"):
        content = f'''package com.lemanrus.radioman.ui.{pkg}

import com.lemanrus.radioman.ui.common.SectionListFragment

class {cls} : SectionListFragment() {{
    override fun screenTitleRes() = com.lemanrus.radioman.R.string.{title}
    override fun cardItems() = {cls}Cards.items
}}
'''
    elif cls.endswith("Fragment") and "Placeholder" in layout or layout == "fragment_placeholder":
        content = f'''package com.lemanrus.radioman.ui.{pkg}

import com.lemanrus.radioman.ui.common.PlaceholderFragment

class {cls} : PlaceholderFragment() {{
    override fun screenTitleRes() = com.lemanrus.radioman.R.string.{title}
}}
'''
    elif layout == "fragment_placeholder":
        content = f'''package com.lemanrus.radioman.ui.{pkg}

import com.lemanrus.radioman.ui.common.PlaceholderFragment

class {cls} : PlaceholderFragment() {{
    override fun screenTitleRes() = com.lemanrus.radioman.R.string.{title}
}}
'''
    else:
        content = f'''package com.lemanrus.radioman.ui.{pkg}

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.ToolbarContentFragment

class {cls} : ToolbarContentFragment(R.layout.{layout}) {{
    override fun screenTitleRes() = R.string.{title}
}}
'''
    # Fix placeholder fragments
    if layout == "fragment_placeholder":
        content = f'''package com.lemanrus.radioman.ui.{pkg}

import com.lemanrus.radioman.R
import com.lemanrus.radioman.ui.common.PlaceholderFragment

class {cls} : PlaceholderFragment() {{
    override fun screenTitleRes() = R.string.{title}
}}
'''
    (pkg_path / f"{cls}.kt").write_text(content, encoding="utf-8")

# nav graph
lines = ['<?xml version="1.0" encoding="utf-8"?>', '<navigation xmlns:android="http://schemas.android.com/apk/res/android"',
         '    xmlns:app="http://schemas.android.com/apk/res-auto"',
         '    android:id="@+id/nav_graph"',
         '    app:startDestination="@id/markingsFragment">', '']

anim_action = '''
        app:enterAnim="@anim/slide_in_right"
        app:exitAnim="@anim/slide_out_left"
        app:popEnterAnim="@anim/slide_in_left"
        app:popExitAnim="@anim/slide_out_right"'''

for pkg, cls, layout, title, nested, _ in FRAGMENTS:
    fid = frag_id(cls)
    lines.append(f'    <fragment')
    lines.append(f'        android:id="@+id/{fid}"')
    lines.append(f'        android:name="com.lemanrus.radioman.ui.{pkg}.{cls}"')
    lines.append(f'        android:label="@string/{title}" />')
    lines.append('')

lines.append('</navigation>')
(BASE / "res/navigation/nav_graph.xml").write_text("\n".join(lines), encoding="utf-8")
print("Generated", len(FRAGMENTS), "fragments")

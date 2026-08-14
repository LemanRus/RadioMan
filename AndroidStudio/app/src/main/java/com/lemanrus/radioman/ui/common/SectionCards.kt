package com.lemanrus.radioman.ui.common

import com.lemanrus.radioman.R

object SectionCards {

    val markingsRoot = listOf(
        SectionCardItem("Резисторы", R.drawable.resistor, R.id.resistorsMarkingSelectFragment),
        SectionCardItem("Конденсаторы", R.drawable.capacitor, R.id.capacitorsMarkingSelectFragment)
    )

    val resistorsSelect = listOf(
        SectionCardItem("Резисторы сквозного монтажа", R.drawable.th_resistor, R.id.thResistorsMarkingFragment),
        SectionCardItem("SMD резисторы", R.drawable.smd_resistor, R.id.smdResistorsMarkingFragment)
    )

    val capacitorsSelect = listOf(
        SectionCardItem("Конденсаторы сквозного монтажа", R.drawable.th_capacitor, R.id.thCapacitorsMarkingFragment),
        SectionCardItem("SMD конденсаторы", R.drawable.smd_capacitor, R.id.smdCapacitorsMarkingFragment)
    )

    val calculationsRoot = listOf(
        SectionCardItem("Конвертер величин", R.drawable.converter, R.id.converterFragment),
        SectionCardItem("Расчёт резисторов для светодиодов", R.drawable.resistor_led, R.id.ledResistorFragment),
        SectionCardItem("Расчёт катушки индуктивности", R.drawable.inductor, R.id.inductorSelectFragment),
        SectionCardItem("Параллельное соединение резисторов", R.drawable.resistors_par, R.id.parallelResistorFragment),
        SectionCardItem("Последовательное соединение конденсаторов", R.drawable.capacitors_ser, R.id.serialCapacitorFragment),
        SectionCardItem("Делитель напряжения", R.drawable.divider, R.id.voltageDividerSelectFragment),
        SectionCardItem("LM317/LM350/LM338 калькулятор", R.drawable.transistor, R.id.lmRegulatorSelectFragment)
    )

    val inductorSelect = listOf(
        SectionCardItem("Расчёт индуктивности по параметрам", R.drawable.induction, R.id.inductorInductionFragment),
        SectionCardItem("Расчёт размеров по индуктивности", R.drawable.coil_size, R.id.inductorSizeFragment)
    )

    val voltageDividerSelect = listOf(
        SectionCardItem("Расчёт выходного напряжения", R.drawable.voltage, R.id.voltageDividerVoltageFragment),
        SectionCardItem("Расчёт сопротивлений", R.drawable.resistance, R.id.voltageDividerResistanceFragment)
    )

    val lmRegulatorSelect = listOf(
        SectionCardItem("Расчёт выходного напряжения", R.drawable.voltage_source, R.id.lmRegulatorVoltageFragment),
        SectionCardItem("Расчёт выходного тока", R.drawable.current_source, R.id.lmRegulatorCurrentFragment)
    )

    val handbookRoot = listOf(
        SectionCardItem("Теория", R.drawable.theory, R.id.theoryFragment),
        SectionCardItem("Обозначения на схемах", R.drawable.transistor_scheme, R.id.schematicsFragment),
        SectionCardItem("Распиновки", R.drawable.pinout, R.id.pinoutFragment),
        SectionCardItem("Типы соединений", R.drawable.connection, R.id.connectionsFragment),
        SectionCardItem("Микросхемы и компоненты", R.drawable.chip, R.id.chipsFragment),
        SectionCardItem("Лайфхаки", R.drawable.lifehack, R.id.lifehacksFragment)
    )

    val chipsRoot = listOf(
        SectionCardItem("Аналоги отечественных микросхем", R.drawable.chips_analogs, R.id.chipsAnalogsSelectFragment)
    )

    val helpRoot = listOf(
        SectionCardItem("Как пользоваться", R.drawable.help, R.id.howToFragment),
        SectionCardItem("О программе", R.drawable.info, R.id.aboutFragment)
    )
}

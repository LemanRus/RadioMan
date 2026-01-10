# -*- coding: utf-8 -*-
"""Экран расчета резистора для LED"""

from kivymd.uix.screen import MDScreen

from e24_nominals import E24Nominals as e24
from output_value_methods import format_output_resistor


class LEDResistorCalculationScreen(MDScreen):
    def led_calculate(self, vol, led_vol, led_cur, led_quant):
        try:
            led_resistance = (
                float(vol) - (float(led_vol) * float(led_quant))
                ) / (float(led_cur) / 1000)
            if led_resistance < 0:
                self.ids.led_result.text = "Слишком малое напряжение \
                                            источника питания!"
                self.ids.led_res_power.text = ''
                self.ids.led_cur.text = ''
                self.ids.led_e24.text = ''
            else:
                self.ids.led_result.text = format_output_resistor(
                    led_resistance
                    )
                e24_result = e24.calculate_standard_resistor(
                    led_resistance, True
                    )
                self.ids.led_e24.text = format_output_resistor(
                    e24_result
                    )

                self.ids.led_res_power.text = "{:g} мВт".format(
                        (float(vol) - float(led_vol)) *
                        float(led_cur) * float(led_quant)
                        )
                self.ids.led_cur.text = "{:g} мА".format(
                    float(led_cur) * float(led_quant)
                    )
        except ValueError:
            self.ids.led_e24.text = "Неверный ввод!"
            self.ids.led_result.text = "Неверный ввод!"
            self.ids.led_res_power.text = "Неверный ввод!"
            self.ids.led_cur.text = "Неверный ввод!"

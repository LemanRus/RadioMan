# -*- coding: utf-8 -*-
"""Экраны расчета индуктивности"""

import math

from kivymd.uix.screen import MDScreen


class InductorCalculationSelectScreen(MDScreen):
    pass


class InductorCalculateInductionScreen(MDScreen):
    def inductor_calculate_henrys(self, turns, diameter, length):
        try:

            turns = float(turns)
            diameter = float(diameter)
            length = float(length)

            formfactor = length / diameter

            induction = 0.0002 * math.pi * diameter * turns ** 2 * (
                math.log(
                    1 + math.pi / (2 * formfactor)
                    ) + 1 / (
                        2.3004 + 3.437 * formfactor + 1.7636 *
                        formfactor ** 2 -
                        0.47 / (0.755 + 1 / formfactor) ** 1.44
                        )
                )
            self.ids.induction.text = "{:g} мкГн".format(induction)
        except Exception:
            self.ids.induction.text = "Неверный ввод!"


class InductorCalculateSizeScreen(MDScreen):
    def inductor_calculate_turns(self, henrys, diameter, oneturn):
        try:
            henrys = float(henrys)
            diameter = float(diameter) / 10
            oneturn = float(oneturn) / 10
            inductor_length = (
                50 * oneturn ** 2 * henrys + math.sqrt(5) * math.sqrt(
                    500 * oneturn ** 4 * henrys ** 2 + 9 * oneturn ** 2
                    * diameter ** 3 * henrys
                    )
                ) / diameter ** 2

            inductor_turns = inductor_length / oneturn
            inductor_turns_int = round(inductor_turns, 0)
            inductor_length_int = inductor_turns_int * oneturn * 10

            self.ids.inductor_length.text = "{:g} мм".format(
                inductor_length * 10
                )
            self.ids.inductor_length_int.text = "{:g} мм".format(
                inductor_length_int
                )
            self.ids.inductor_turns.text = "{:g} витка(ов)".format(
                inductor_turns
                )
            self.ids.inductor_turns_int.text = "{:g} витка(ов)".format(
                inductor_turns_int
                )
        except Exception:
            self.ids.inductor_length.text = "Неверный ввод!"
            self.ids.inductor_length_int.text = "Неверный ввод!"
            self.ids.inductor_turns.text = "Неверный ввод!"
            self.ids.inductor_turns_int.text = "Неверный ввод!"

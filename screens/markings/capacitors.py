# -*- coding: utf-8 -*-
"""Экраны маркировок конденсаторов"""

from kivymd.uix.screen import MDScreen

from data_loader import load_capacitor_markings


class CapacitorsMarkingSelectScreen(MDScreen):
    pass


class THCapacitorsMarkingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        capacitor_data = load_capacitor_markings()
        self.decimal_point = capacitor_data['decimal_point']

    def calculate_capacitor(self, value):
        capacity = ""
        if value.isdigit():
            if len(value) <= 2:
                capacity = int(value)
            else:
                capacity = int(value[-2::-1][::-1]) * 10 ** int(value[-1])
        elif "r" in value.lower():
            capacity = float(
                "{}.{}".format(
                    value.lower().split("r")[0], value.lower().split("r")[1]
                        )
                    )
        elif any(ext in value for ext in self.decimal_point.keys()):
            intersection = "".join(
                [inter for inter in self.decimal_point.keys()
                 if (inter in value)]
                 )
            capacity = float(
                "{}.{}".format(
                    value.split(intersection)[0], value.split(intersection)[1]
                    )
                        ) * self.decimal_point[intersection]
        else:
            self.ids.th_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.th_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.th_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.th_capacitor_result.text += "{:g} пФ".format(
                        capacity
                        )
                elif capacity < 1000000:
                    self.ids.th_capacitor_result.text += "{:g} нФ".format(
                        capacity / 1000
                        )
                elif capacity < 1000000000:
                    self.ids.th_capacitor_result.text += "{:g} мкФ".format(
                        capacity / 1000000
                        )
                else:
                    self.ids.th_capacitor_result.text += "{:g} мФ".format(
                        capacity / 1000000000
                        )
            except ValueError:
                return "Неверный ввод!"


class SMDCapacitorsMarkingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Загружаем данные из JSON
        capacitor_data = load_capacitor_markings()
        self.voltage = capacitor_data['voltage']
        self.smd_capacity = capacitor_data['smd_capacity']

    def calculate_smd_capacitor(self, value):
        capacity = ""
        voltage = "?"
        values = list(value)
        if len(values) == 2:
            if values[0] in self.smd_capacity.keys():
                capacity = self.smd_capacity[values[0]] * 10 ** int(values[1])
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
        elif len(values) == 3:
            if values[0] in self.voltage.keys():
                voltage = self.voltage[values[0]]
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
            if values[1] in self.smd_capacity.keys():
                capacity = self.smd_capacity[values[1]] * 10 ** int(values[2])
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
        elif len(values) == 4:
            if values[0] in self.voltage.keys():
                voltage = self.voltage[values[0]]
            else:
                self.ids.smd_capacitor_result.text = "Неверный ввод"
            capacity = int(''.join((str(i) for i in values[1:3]))) * \
                10 ** int(values[3])
        else:
            self.ids.smd_capacitor_result.text = "Неверный ввод"

        if capacity != "":
            try:
                self.ids.smd_capacitor_result.text = "Результат: "
                capacity = float(capacity)
                if capacity == 0:
                    self.ids.smd_capacitor_result.text += "0 мкФ (перемычка)"
                elif capacity < 1000:
                    self.ids.smd_capacitor_result.text += "{:g} пФ".format(
                        capacity
                        )
                elif capacity < 1000000:
                    self.ids.smd_capacitor_result.text += "{:g} нФ".format(
                        capacity / 1000
                        )
                elif capacity < 1000000000:
                    self.ids.smd_capacitor_result.text += "{:g} мкФ".format(
                        capacity / 1000000
                        )
                else:
                    self.ids.smd_capacitor_result.text += "{:g} мФ".format(
                        capacity / 1000000000
                        )
            except ValueError:
                return "Неверный ввод!"
            self.ids.smd_capacitor_result.text += ", " + str(voltage) + " В"

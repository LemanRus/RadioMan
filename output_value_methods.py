def format_output_resistor(resistance: float):
    try:
        resistance = float(resistance)
        if resistance == 0:
            return "0 Ом (перемычка)"
        elif resistance < 1000:
            return "{:g} Ом".format(resistance)
        elif resistance < 1000000:
            return "{:g} кОм".format(resistance / 1000)
        else:
            return "{:g} МОм".format(resistance / 1000000)
    except ValueError:
        return "Неверный ввод"


def format_output_capacitor(capacitance: float):
    try:
        capacitance = float(capacitance)
        if capacitance == 0:
            return "0 пФ (перемычка)"
        elif capacitance < 1000:
            return "{:g} пФ".format(capacitance)
        elif capacitance < 1000000:
            return "{:g} нФ".format(capacitance / 1000)
        else:
            return "{:g} мкФ".format(capacitance / 1000000)
    except ValueError:
        return "Неверный ввод"

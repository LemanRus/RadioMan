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
class E24Nominals:
    E24 = (1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8,
           7.5, 8.2, 9.1)

    @staticmethod
    def calculate_standard_resistor(resistance, go_up: bool):
        res = resistance
        while res >= 10:
            res /= 10
        list_of_diffs = [abs(res - x) for x in E24Nominals.E24]
        result_index = list_of_diffs.index(min(list_of_diffs))
        interact = resistance / E24Nominals.E24[result_index]
        power = 0
        while True:
            if interact < 9:
                break
            power += 1
            interact /= 10
        e24_result = E24Nominals.E24[result_index] * 10 ** power
        if go_up:
            if e24_result < resistance:
                if result_index != len(E24Nominals.E24) - 1:
                    e24_result = E24Nominals.E24[result_index + 1] * 10 ** power
                else:
                    e24_result = E24Nominals.E24[0] * 10 ** (power + 1)
        return e24_result

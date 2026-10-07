from toolkit.errors import ConverterError

kf_length = {'mm':0.001, 'cm':0.01, 'm':1, 'km':1000}
kf_mass = {'g':1, 'kg':1000}

def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit in kf_length:
        if to_unit not in kf_length:
            raise ConverterError("Несовместимые единицы")

        value_in_meters = value * kf_length[from_unit]

        return float(value_in_meters / kf_length[to_unit])

    elif from_unit in kf_mass:
        if to_unit not in kf_mass:
            raise ConverterError("Несовместимые единицы")

        value_in_grams = value * kf_mass[from_unit]

        return float(value_in_grams / kf_mass[to_unit])

    elif from_unit in ('c', 'f', 'k'):
        if to_unit not in ('c', 'f', 'k'):
            raise ConverterError("Несовместимые единицы")

        if from_unit == 'c':
            celsius = value
        elif from_unit == 'k':
            celsius = value - 273.15
        else:
            celsius = (value - 32) * 5 / 9

        if celsius < -273.15:
            raise ConverterError("Температура ниже абсолютного нуля")

        if to_unit == 'c':
            return float(celsius)
        elif to_unit == 'k':
            return float(celsius + 273.15)
        else:
            return float((celsius * 9 / 5) + 32)

    else:
        raise ConverterError("Неизвестная единица")

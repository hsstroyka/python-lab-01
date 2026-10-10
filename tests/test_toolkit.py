import pytest

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import CalculatorError
from toolkit.errors import ConverterError

def test_calc_math():
    assert calculate("2 + 3 * 4") == 14
    assert calculate("10 / 2 - 1") == 4

def test_calc_space_float():
    assert calculate("  1.5  +    2.5    ") == 4

def test_calc_unary_minus_one():
    assert calculate("-5 + 10") == 5

def test_calc_unary_minus_middle():
    assert calculate("2 * -3") == -6

def test_calc_division_by_zero():
    with pytest.raises(CalculatorError, match = "Деление на ноль"):
        calculate("5 / 0")

def test_calc_two_operators():
    with pytest.raises(CalculatorError, match = "Два бинарных оператора подряд"):
        calculate("2 + * 3")

def test_calc_invalid_char():
    with pytest.raises(CalculatorError, match = "Недопустимый символ"):
        calculate("2 + $")

def test_convert_length():
    assert convert(1.5, "km", "m") == 1500
    assert convert(100, "cm", "m") == 1

def test_convert_mass():
    assert convert(100, "kg", "g") == 100000

def test_convert_temp():
    assert convert(0, "c", "k") == 273.15

def test_convert_reg():
    assert convert(1,"KG", "g") == 1000

def test_convert_different_units():
    with pytest.raises(ConverterError, match = "Несовместимые единицы"):
        convert(5, "kg", "m")

def test_convert_absolute_temperature():
    with pytest.raises(ConverterError, match = "Температура ниже абсолютного нуля"):
        convert(-300, "c", "k")

def test_convert_bred():
    with pytest.raises(ConverterError, match = "Неизвестная единица"):
        convert(10,"privet", "kg")

from toolkit.__main__ import main

def test_cli_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["toolkit", "--help"])
    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert "Консольный набор утилит" in captured.out

def test_cli_calc_error_stderr(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["toolkit", "calc", "5", "/", "0"])
    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ошибка: Деление на ноль" in captured.err

def test_cli_unknown_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["toolkit", "hello"])
    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ошибка: Недопустимый символ: hello" in captured.err



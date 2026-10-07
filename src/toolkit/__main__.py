import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def print_help():

    help_text = """Консольный набор утилит 'toolkit'

Использование:
  python -m toolkit calc "EXPRESSION" - Запуск калькулятора выражений
  python -m toolkit convert VALUE --from UNIT --to UNIT - Конвертер величин
  python -m toolkit --help - Показать эту справку"""
    print(help_text)

def main():

    args = sys.argv[1:]

    if not args or '--help' in args or '-h' in args:
        print_help()
        sys.exit(0)

    command = args[0]

    try:
        if command == 'calc':
            if len(args) < 2:
                raise ToolkitError("Пустое выражение")

            expression = "".join(args[1:])
            res = calculate(expression)
            print(f"{res:.6g}")
            sys.exit(0)

        elif command == 'convert':
            if len(args) < 6:
                raise ToolkitError("Неверное числовое значение")

            try:
                value = float(args[1])
            except ValueError:
                raise ToolkitError("Неверное числовое значение")

            if "--from" not in args or "--to" not in args:
                raise ToolkitError("Неизвестная единица")

            from_id = args.index("--from")
            to_id = args.index("--to")
            if from_id + 1 >= len(args) or to_id + 1 >= len(args):
                raise ToolkitError("Неизвестная единица")

            from_unit = args[from_id + 1]
            to_unit = args[to_id + 1]

            res = convert(value, from_unit, to_unit)

            print(f"{res:.6g} {to_unit}")
            sys.exit(0)

        else:
            raise ToolkitError(f"Недопустимый символ: {command}")

    except ToolkitError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()

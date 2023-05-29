import modules
from config import configs

import click
from PyInquirer import ValidationError, Validator, prompt, style_from_dict
from pyfiglet import figlet_format

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({})


def figletLog(string, color, font="slant"):
    if colored:
        print(colored(figlet_format(
            string, font=font), color))
    else:
        print(string)


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please input number only',
                cursor_position=len(document.text))


class ExcludedSeatValidator(Validator):
    def validate(self, seats):
        seats = seats.text
        seat_array = seats.strip().split()

        try:
            excluded_seats = [int(seat) for seat in seat_array]
        except ValueError:
            raise ValidationError(
                message='Please input numbers only')

        return excluded_seats



def askReorderOptions():
    questions = [
        {
            'type': 'list',
            'name': 'reorder_option',
            'message': 'Which seat option would you like to choose?',
            'choices': configs.REORDER_SEAT_OPTIONS
        },
        {
            'type': 'confirm',
            'name': 'include_absence',
            'message': 'Do you include those who are vacant?',
        },
        {
            'type': 'input',
            'name': 'excluded_seats',
            'message': 'Input seats to be excluded (space separated):',
            'validate': ExcludedSeatValidator,
            'filter': lambda val: [int(seat) for seat in val.split()] if val else [],
        },
    ]

    results = prompt(questions, style=style)
    return results


@click.command()
def main():
    figletLog("  Cloudforet  ", color="magenta")
    figletLog("Reorder Seats!!", color="light_blue")

    ask_results = askReorderOptions()
    result = modules.reorder_seats(ask_results)
    modules.print_seats(result)

if __name__ == '__main__':
    main()

from modules.reorder import reorder_seats
from modules.print import print_seats
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


def figlet_log(string, color, font="slant"):
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



def ask_reorder_options():
    questions = [
        {
            'type': 'list',
            'name': 'reorder_option',
            'message': 'Which seat option would you like to choose?',
            'choices': configs.REORDER_SEAT_OPTIONS
        },
        {
            'type': 'input',
            'name': 'excluded_seats',
            'message': 'Input seats to be excluded (space separated, 4 count required):',
            'validate': ExcludedSeatValidator,
            'filter': lambda val: [int(seat) for seat in val.split()] if val else [],
        },
    ]

    results = prompt(questions, style=style)
    return results


@click.command()
def main():
    figlet_log("  Cloudforet  ", color="magenta")
    figlet_log("Reorder Seats!!", color="light_blue")

    ask_results = ask_reorder_options()
    result = reorder_seats(ask_results)
    print_seats(result)

if __name__ == '__main__':
    main()

from enum import Enum
import random
import time
from typing import TypedDict, List
from rich import print
from rich.panel import Panel
from rich.progress import track

from member_info_manager import MemberInfoManager

member_data = 'config/members.json'


class ReorderSeatOptions(Enum):
    prevent_duplicate = 'prevent_duplicate'
    change_partner = 'change_partner'
    no_option = 'no_option'


class ReorderArgs(TypedDict):
    reorder_option: ReorderSeatOptions
    include_absence: bool
    excluded_seats: List['int']


def reorder_seats(options: ReorderArgs):
    reorder_option = options['reorder_option']
    include_absence = options['include_absence']
    excluded_seats = options['excluded_seats']

    manager = MemberInfoManager(member_data)
    manager.load_members_from_json()
    member_list = manager.members

    seat_indices = list(range(1, 25))
    for excluded_seat in excluded_seats:
        seat_indices.remove(excluded_seat)

    if reorder_option == ReorderSeatOptions.change_partner:
        seat_indices = rearrange_numbers(seat_indices)
    elif reorder_option == ReorderSeatOptions.prevent_duplicate:
        random.shuffle(seat_indices)
    else:
        random.shuffle(seat_indices)
        random.shuffle(seat_indices)

    for i, person in enumerate(member_list):
        if not include_absence and person['absence']:
            person['seat_index'] = -1
        else:
            person['seat_index'] = seat_indices[i]

    manager.update_members(member_list)
    manager.save_members_to_json()

    return member_list


def check_conditions(numbers):
    for i in range(len(numbers) - 1):
        num1 = numbers[i]
        num2 = numbers[i + 1]

        if i % 2 == 0 and num1 % 2 == 1 and num2 % 2 == 0:
            return False

        if num1 % 6 == 0 and num2 == num1 - 1:
            return False

    return True


def rearrange_numbers(numbers: List['int']):
    random.shuffle(numbers)

    while not check_conditions(numbers):
        random.shuffle(numbers)

    return numbers


class MemberInfo(TypedDict):
    name: str
    seat_index: int
    absence: bool


def print_seats(member_list: List['MemberInfo']):
    for i in track(range(100), description="Reordering...", show_speed=False):
        time.sleep(0.01)

    row_size = 4
    column_size = 2
    total_pictures = 3

    template = [[['빈자리'] * row_size for _ in range(column_size)] for _ in range(total_pictures)]

    for member in member_list:
        seat_number = member['seat_index']
        name = member['name'] if member['name'] else '빈자리'
        template_index, seat_index = divmod(seat_number - 1, row_size * column_size)
        column, row = divmod(seat_index, row_size)
        template[template_index][column][row] = name

    for row in template:
        panel_content = '\n'.join('\t'.join(col) for col in row)
        picture_panel = Panel(panel_content, title=None, width=43)
        print(picture_panel)

import time
from typing import TypedDict, List
from rich import print
from rich.panel import Panel
from rich.progress import track


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

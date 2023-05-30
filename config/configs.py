from enum import Enum
from typing import TypedDict

REORDER_SEAT_OPTIONS = [
    {
        'key': 'd',
        'name': 'Do you want to prevent duplicate existing seats?',
        'value': 'prevent_duplicate'
    },
    {
        'key': 'p',
        'name': 'Do you want to switch partners next to each other?',
        'value': 'change_partner'
    },
    {
        'key': 's',
        'name': 'Do you want the same parts to be placed close together?',
        'value': 'place_same_part_close'
    },
    {
        'key': 'r',
        'name': 'No Option (Just Random)',
        'value': 'no_option'
    }
]


class PartOptions(Enum):
    leader = 'leader'
    group_leader = 'group_leader'
    architect = 'architect'
    design = 'design'
    develop = 'develop'
    null = 'null'


class MemberInfo(TypedDict):
    name: str
    seat_index: int
    is_empty: bool
    part: PartOptions

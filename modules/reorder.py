from enum import Enum
from typing import List
import random

from modules.member_info_manager import MemberInfoManager
from config.configs import MemberInfo

member_data = 'config/members.json'


class ReorderSeatOptions(Enum):
    prevent_duplicate = 'prevent_duplicate'
    change_partner = 'change_partner'
    no_option = 'no_option'
    place_same_part_close = 'place_same_part_close'


def reorder_seats(options: dict):
    reorder_option = options['reorder_option']
    excluded_seats = options['excluded_seats']

    # Load member list from json
    manager = MemberInfoManager(member_data)
    manager.load_members_from_json()
    member_list = manager.members.copy()
    result = []

    # Get seat indices and exclude excluded seats
    allowed_seat_indices = list(range(1, 25))
    empty_list = [member for member in member_list if member['is_empty']]
    for i, excluded_seat in enumerate(excluded_seats):
        result.append({
            'seat_index': excluded_seat,
            'name': empty_list[i]['name'],
            'is_empty': True,
            'part': empty_list[i]['part'],
        })
        member_list.remove(empty_list[i])
        allowed_seat_indices.remove(excluded_seat)

    # Shuffle member list by close part
    if reorder_option == ReorderSeatOptions.place_same_part_close.value:
        parts = ['leader', 'group_leader', 'architect', 'design', 'develop']
        random.shuffle(parts)
        random.shuffle(member_list)
        member_list.sort(key=lambda x: parts.index(x['part']))
        result.extend({
            'seat_index': seat_index,
            'name': member['name'],
            'is_empty': member['is_empty'],
            'part': member['part']
        } for seat_index, member in zip(allowed_seat_indices, member_list))

    # Shuffle member list by another options
    else:

        if reorder_option == ReorderSeatOptions.change_partner.value:
            allowed_seat_indices = reorder_indices_by_change_partner(allowed_seat_indices)

        elif reorder_option == ReorderSeatOptions.prevent_duplicate.value:
            allowed_seat_indices = reorder_indices_by_prevent_duplicate(allowed_seat_indices)

        else:
            allowed_seat_indices = reorder_indices_by_no_option(allowed_seat_indices)

        result.extend({
            'seat_index': seat_index,
            'name': member_list[i]['name'],
            'is_empty': member_list[i]['is_empty'],
            'part': member_list[i]['part']
        } for i, seat_index in enumerate(allowed_seat_indices))


    # Sort member list by seat index
    result = sort_by_seat_index(result)

    # Save member list to json
    manager.update_members(result)
    manager.save_members_to_json()

    return result


# helper functions
def check_conditions(numbers):
    for i in range(len(numbers) - 1):
        num1 = numbers[i]
        num2 = numbers[i + 1]

        if i % 2 == 0 and num1 % 2 == 1 and num2 % 2 == 0:
            return False

        if num1 % 6 == 0 and num2 == num1 - 1:
            return False

    return True


def sort_by_seat_index(member_list: List['MemberInfo']):
    return sorted(member_list, key=lambda member: member["seat_index"])


# reorder functions
def reorder_indices_by_change_partner(indices: List['int']):
    result = indices.copy()
    random.shuffle(result)

    while not check_conditions(result):
        random.shuffle(result)

    return result


def reorder_indices_by_prevent_duplicate(indices: List['int']):
    result = indices.copy()
    random.shuffle(result)

    return result


def reorder_indices_by_no_option(indices: List['int']):
    result = indices.copy()
    random.shuffle(result)
    random.shuffle(result)

    return result


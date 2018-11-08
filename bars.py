import json
import sys
import os
from geopy import distance


def load_data_from_file(filepath):
    with open(filepath, 'r') as file:
        str_data = file.read()
    try:
        python_object = json.loads(str_data)
        return python_object
    except ValueError:
        return None


def get_seats_count(bar):
    return bar["properties"]["Attributes"]["SeatsCount"]


def get_bar_name(bar):
    return bar["properties"]["Attributes"]["Name"]


def get_bar_address(bar):
    return bar["properties"]["Attributes"]["Address"]


def get_biggest_bar(bars_list):
    biggest_bar = max(bars_list, key=get_seats_count)
    return biggest_bar


def get_smallest_bar(bars_list):
    smallest_bar = min(bars_list, key=get_seats_count)
    return smallest_bar


def convert_str_to_coodinates(str):
    strings = str.split(', ')
    if not len(strings) == 2:
        return None
    try:
        longitude = float(strings[0])
        latitude = float(strings[1])
        return longitude, latitude
    except ValueError:
        return None


def get_bar_coordinates(bar):
    return bar["geometry"]["coordinates"]


def get_closest_bar(bars_list, current_position):
    closest_bar = min(
        bars_list,
        key=lambda bar: distance.distance(
            get_bar_coordinates(bar),
            current_position
        ).m
    )
    return closest_bar


def print_bar_info(bar):
    print('    Name: {name}'.format(name=get_bar_name(bar)))
    print('    Seats count: {seats}'.format(seats=get_seats_count(bar)))
    print('    Address: {address}'.format(address=get_bar_address(bar)))
    print()

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        exit('No filepath received as argument')
    if not os.path.exists(sys.argv[1]):
        exit("File doesn't exist")
    data_dict = load_data_from_file(sys.argv[1])
    if data_dict is None:
        exit("Can't read data about bars")
    bars_list = data_dict["features"]
    biggest_bar = get_biggest_bar(bars_list)
    print('The biggest bar is')
    print_bar_info(biggest_bar)
    smallest_bar = get_smallest_bar(bars_list)
    print('The smallest bar is')
    print_bar_info(smallest_bar)
    input_str = input('Input your coordinates '
                      '(for example "36.234567, 45.345678"):\n')
    my_coordinates = convert_str_to_coodinates(input_str)
    if my_coordinates is None:
        exit("Can't find the closest bar! Input coordinates are incorrect.")
    closest_bar = get_closest_bar(bars_list, my_coordinates)
    print('The closest bar is')
    print_bar_info(closest_bar)

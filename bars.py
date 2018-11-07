import json
import sys
import os
from geopy import distance


def load_data_from_file(filepath):
    if not os.path.exists(filepath):
        return None
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


def get_bar_distance(bar):
    return bar["geometry"]["distance"]


def get_biggest_bar(bars_list):
    biggest_bar = max(bars_list, key=get_seats_count)
    return biggest_bar


def get_smallest_bar(data):
    smallest_bar = min(bars_list, key=get_seats_count)
    return smallest_bar


def convert_str_to_coodinates(str):
    strings = str.split(', ')
    if not len(strings) == 2:
        return None
    try:
        longitude = float(strings[0])
        latitude = float(strings[1])
        return [longitude, latitude]
    except:
        return None


def get_bar_coordinates(bar):
    return bar["geometry"]["coordinates"]


def get_closest_bar(data, current_position):
    for bar in bars_list:
        bar_distance = distance.distance(get_bar_coordinates(bar), current_position).m
        bar["geometry"]["distance"] = bar_distance
    closest_bar = min(bars_list, key=get_bar_distance)
    return closest_bar


def print_bar_info(bar):
    print('    Name: {name}'.format(name=get_bar_name(bar)))
    print('    Seats count: {seats}'.format(seats=get_seats_count(bar)))
    print('    Address: {address}'.format(address=get_bar_address(bar)))
    try:
        print('    Distance: {0:.2f} m'.format(get_bar_distance(bar)))
    except:
        pass

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        exit('No filepath received as argument')
    data_dict = load_data_from_file(sys.argv[1])
    if data_dict is None:
        exit("Can't read data from file")
    bars_list = data_dict["features"]
    biggest_bar = get_biggest_bar(bars_list)
    print('The biggest bar is')
    print_bar_info(biggest_bar)
    smallest_bar = get_smallest_bar(bars_list)
    print('The smallest bar is')
    print_bar_info(smallest_bar)
    input_str = input('Input your coordinates in format (for example "36.234567, 45.345678"):\n')
    my_coordinates = convert_str_to_coodinates(input_str)
    if my_coordinates is None:
        exit("Can't find the closest bar! Input coordinates are incorrect.")
    closest_bar = get_closest_bar(bars_list, my_coordinates)
    print('The closest bar is')
    print_bar_info(closest_bar)

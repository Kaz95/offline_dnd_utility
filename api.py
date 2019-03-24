import json
import requests
import re

# This module contains functions that interact with the API and those that rely on API sourced data
# "http://www.dnd5eapi.co/api/"


# TODO: Test this
# Creates and returns a simple session object.
def create_session():
    session = requests.Session()
    return session


# Calls (api) url and returns JSON text object. Tries to use a session object to persist underlying connection.
def call_api(url, session=None):
    if session is not None:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    else:
        response = requests.get(url)
        response.raise_for_status()
        return response.text


# Converts json data to python dictionary
def get_api_all(json_data):
    return json.loads(json_data)


# Concatenates an api url frame with a given variable
def construct_api_url(some_api_dict):
    return f'http://www.dnd5eapi.co/api/{some_api_dict}/'


# Slices a nested dictionary at a given top level key
def get_nested_api_dict(api_dump, dict_to_slice):
    return api_dump[dict_to_slice]


# some_dict = {'name': 'some_name', 'url': 'some_url'}
# TODO: Refactor: Name
# TODO: Might be a better way to write this.
def check_for_url(name, some_dict):
    if some_dict['name'] == name:
        new_call = some_dict['url']
        return new_call


# TODO: Might be a better way to write this
# Expects list of dictionaries
# similar to [{'name': 'some_name', 'url': 'some_url'}, {'name': 'some_name', 'url': 'some_url'}]
def get_api_info(name, list_of_dicts):
    for dic in list_of_dicts:   # For dict in list of dicts
        if dic['name'] == name:   # If dic['name'] == item searched for
            api_info = list([dic['name']] + [dic['url']])  # Double bracket to make sure string isn't slice by character
            return api_info


# TODO: Might be a better way to write this.
# Expects list of dictionaries
# similar to [{'name': 'some_name', 'url': 'some_url'}, {'name': 'some_name', 'url': 'some_url'}]
def get_item_url(name, list_of_dicts):
    for dic in list_of_dicts:  # For dictionary in list of dictionaries
        new_url = check_for_url(name, dic)
        if new_url is not None:
            return new_url


# TODO: Test this
# Retrieves the url associated with an item.
# Uses url to requests info from API
# Slices the cost dictionary from its parent
# Converts the sliced dictionary to base currency type and returns value
def get_item_value(item, some_dict, session):
    url = get_item_url(item, some_dict)
    item_info = get_api_all(call_api(url, session))
    item_cost = get_nested_api_dict(item_info, 'cost')
    item_value = convert_price_info(item_cost)
    return item_value


# Takes input as {'quantity': 'x', 'unit': 'y'}
# Converts to base currency type and returns value.
def convert_price_info(price_dict):
    if price_dict['unit'] == 'gp':
        converted_value = price_dict['quantity'] * 100  # Converts gp prices to universal cp unit used for back end math
        return converted_value
    elif price_dict['unit'] == 'sp':
        converted_value = price_dict['quantity'] * 10   # Converts sp prices to universal cp unit used for back end math
        return converted_value
    if price_dict['unit'] == 'cp':
        return price_dict['quantity']


# Slices index number from api url
def regex(url, api_category):
    reg = re.compile(r'(?<=' + re.escape(api_category) + r')\d{1,3}')
    temp_obj = reg.search(url)
    string = temp_obj.group()
    return string

import json
import requests
import re
# This module contains functions that interact with the API and those that rely on API sourced data
url = "http://www.dnd5eapi.co/api/equipment/"


def call_api(some_api):
    response = requests.get(some_api)
    response.raise_for_status()
    return response.text


def slice_dict_results(some_dict):
    return some_dict['results']


def get_api_all(api_url):
    return json.loads((call_api(api_url)))


def make_api_url(some_api_dict):
    return f'http://www.dnd5eapi.co/api/{some_api_dict}/'


def get_api_results(api_url):
    return get_api_all(api_url)['results']


def get_api_cost(item_info_dict):
    return item_info_dict['cost']


def url_call(name, i):
    if i['name'] == name:
        new_call = i['url']
        return new_call


def get_api_info(name, list_of_dicts):
    for dic in list_of_dicts:   # For dict in list of dicts
        if dic['name'] == name:   # If dic['name'] == item searched for
            api_info = list([dic['name']] + [dic['url']])  # Double bracket to make sure string isn't slice by character
            return api_info


def get_item_url(name, list_of_dicts):
    for i in list_of_dicts:  # For dictionary in list of dictionaries
        # if i['name'] == name:
        #     new = i['url']
        #     return new
        new_call = url_call(name, i)
        if new_call is not None:
            return new_call


# Takes input as {'quantity': 'x', 'unit': 'y'}
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
def regex(api):
    reg = re.compile(r'(?<=equipment/)\d{1,3}')
    temp_obj = reg.search(api)
    # print(temp_obj)
    string = temp_obj.group()
    return string


if __name__ == '__main__':
    # Examples of fake json objects
    a = '{"results": [{"name": 1, "url": 1},{"name": 2, "url": 2}]}'
    b = '{"results": 1}'
    # print(get_api_all(make_api_url('equipment')))
    # pprint.pprint(get_api_results(make_api_url('Equipment'), 'results'))
    print(get_api_cost(get_api_all(get_item_url('Club', get_api_results(make_api_url('Equipment'))))))
    # print(get_api_all(get_item_url('Acid Arrow', get_api_dictionary('spells'))))

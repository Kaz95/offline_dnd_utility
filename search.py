#!/usr/bin/python
import json
import requests
import re
# This module contains functions that interact with the API


# Search
def search(name):
    url = "http://www.dnd5eapi.co/api/equipment/"  # Storing API url as var
    response = requests.get(url)    # stores response from .get ping as response
    response.raise_for_status()     # Checks response for errors
    equipment = json.loads(response.text)   # json.load turns json data to a python dictionary
    list_of_dic = equipment['results']  # Dictionary containing Name/url: Values
    print('What are you looking for?')
    item = name  # Asks for item to search for
    for dic in list_of_dic:   # For dic in list of dics
        if dic['name'] == item:   # If dic[name] == item searched for
            api_info = list([dic['name']] + [dic['url']])  # Double bracket to make sure string isn't slice by character
            # print(api_info)
            return api_info


# Returns nested dictionary of all item information
def get_all_info(name):
    url = "http://www.dnd5eapi.co/api/equipment/"  # Storing API url as var
    response = requests.get(url)  # stores response from .get ping as response
    response.raise_for_status()  # Checks response for errors
    equipment = json.loads(response.text)  # json.load turns json data to a python dictionary
    list_of_dic = equipment['results']  # Dictionary containing Name/url: Values
    for i in list_of_dic:  # For dictionary in list of dictionaries
        if i['name'] == name:  # If dic[name] == item searched for
            url = i['url']  # Change API from general category to item specific url

    response = requests.get(url)  # stores response from .get ping as response
    response.raise_for_status()  # Checks response for errors
    item_info = json.loads(response.text)  # Assigns detailed item info to a var in form of nested dictionary.
    return item_info


# Returns {'quantity': 'x', 'unit': 'y'}
def get_price_info(name):
    url = "http://www.dnd5eapi.co/api/equipment/"  # Storing API url as var
    response = requests.get(url)  # stores response from .get ping as response
    response.raise_for_status()  # Checks response for errors
    equipment = json.loads(response.text)  # json.load turns json data to a python dictionary
    list_of_dic = equipment['results']  # Dictionary containing Name/url: Values
    for i in list_of_dic:  # For dictionary in list of dictionaries
        if i['name'] == name:  # If dic[name] == item searched for
            url = i['url']  # Change API from general category to item specific url

    response = requests.get(url)  # stores response from .get ping as response
    response.raise_for_status()  # Checks response for errors
    item_info = json.loads(response.text)  # Assigns detailed item info to a var in form of nested dictionary.
    price_info = item_info['cost']
    return price_info


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
    print(search('Club'))

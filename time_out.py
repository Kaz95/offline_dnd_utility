# Search
# # Searches for a given string value in a nested dictionary.
# # Dictionary is called from a static api address.
# # Returns [name, api]
# def get_api_info(name, api_call):
#     equipment = convert_json_slice_dict(api_call)
#     for dic in equipment:   # For dict in list of dicts
#         if dic['name'] == name:   # If dic['name'] == item searched for
#             api_info = list([dic['name']] + [dic['url']])  # Double bracket to make sure string isn't slice by character
#             return api_info
#
#
# # Passed an item name in form of string.
# # Returns nested dictionary of all item information.
# def get_detailed_info(name, api_call):
#     equipment = convert_json_slice_dict(api_call)
#     for i in equipment:  # For dictionary in list of dictionaries
#         if i['name'] == name:  # If dic[name] == item searched for
#             new_call = i['url']  # Change API from general category to item specific url
#             item_info = json.loads(call_api(new_call))
#             return item_info
#
#
# # Returns {'quantity': 'x', 'unit': 'y'}
# def get_price_info(name, api_call):
#     equipment = convert_json_slice_dict(api_call)
#     for i in equipment:  # For dictionary in list of dictionaries
#         if i['name'] == name:  # If dic[name] == item searched for
#             new_call = i['url']  # Change API from general category to item specific url
#             item_info = json.loads(call_api(new_call))
#             price_info = item_info['cost']
#             return price_info
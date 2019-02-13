import unittest
from unittest.mock import patch
from api import call_api, get_api_all, make_api_url, get_nested_api_dict, url_call, get_api_info, get_item_url
from api import convert_price_info, regex


class TestApi(unittest.TestCase):

    def test_call_api(self):
        with patch('api.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            response = call_api('http://www.dnd5eapi.co/api/equipment/')
            # mocked_get.assert_called_with('http://www.dnd5eapi.co/api/equipment/')
            self.assertEqual(response, 'Success')

    # def test_convert_json_slice_dict(self):
    #     api_call = '{"results": 1}'
    #     self.assertEqual(convert_json_slice_dict(api_call), 1)
    #
    # def test_search(self):
    #     list_of_dicts = '{"results": [{"name": 1, "url": 1},{"name": 2, "url": 2}]}'
    #     self.assertEqual(search(1, list_of_dicts), [1, 1])

    def test_get_api_all(self):
        some_api_call = '{"results": 1}'
        self.assertEqual(get_api_all(some_api_call), {"results": 1})

    def test_make_api_url(self):
        self.assertEqual(make_api_url('equipment'), 'http://www.dnd5eapi.co/api/equipment/')

    def test_get_api_results(self):
        some_dict_results = {'results': 1}
        some_dict_cost = {'cost': 2}
        self.assertEqual(get_nested_api_dict(some_dict_results, 'results'), 1)
        self.assertEqual(get_nested_api_dict(some_dict_cost, 'cost'), 2)

    def test_url_call(self):
        some_dict = {'name': 1, 'url': 2}
        self.assertEqual(url_call(1, some_dict), 2)

    def test_get_api_info(self):
        list_of_dicts = [{'name': 1, 'url': 1}, {'name': 2, 'url': 2}]
        self.assertEqual(get_api_info(1, list_of_dicts), [1, 1])
        self.assertEqual(get_api_info(2, list_of_dicts), [2, 2])

    def test_get_item_url(self):
        list_of_dicts = [{'name': 1, 'url': 1}, {'name': 2, 'url': 2}]
        self.assertEqual(get_item_url(1, list_of_dicts), 1)
        self.assertEqual(get_item_url(2, list_of_dicts), 2)

    def test_convert_price_info(self):
        s = {'quantity': 2, 'unit': 'sp'}
        g = {'quantity': 3, 'unit': 'gp'}
        c = {'quantity': 50, 'unit': 'cp'}
        self.assertEqual(convert_price_info(s), 20)
        self.assertEqual(convert_price_info(g), 300)
        self.assertEqual(convert_price_info(c), 50)

    def test_regex(self):
        equip = 'http://www.dnd5eapi.co/api/equipment/145'
        spells = 'http://www.dnd5eapi.co/api/spells/12'
        feat = 'http://www.dnd5eapi.co/api/features/312'
        classes = 'http://www.dnd5eapi.co/api/classes/5'
        self.assertEqual(regex(equip, 'equipment/'), '145')
        self.assertEqual(regex(spells, 'spells/'), '12')
        self.assertEqual(regex(feat, 'features/'), '312')
        self.assertEqual(regex(classes, 'classes/'), '5')


if __name__ == '__main__':
    unittest.main()


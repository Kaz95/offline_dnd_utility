import unittest
import api


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.list_of_dics = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('equipment'))),
                                                    'results')

    def test_main_dictionaries(self):
        equip_count = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('equipment'))), 'count')
        spells_count = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('spells'))), 'count')
        classes_count = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('classes'))), 'count')
        features_count = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('features'))), 'count')
        monsters_count = api.get_nested_api_dict(api.get_api_all(api.call_api(api.construct_api_url('monsters'))), 'count')
        self.assertEqual(equip_count, 256)
        self.assertEqual(spells_count, 319)
        self.assertEqual(classes_count, 12)
        self.assertEqual(features_count, 414)
        self.assertEqual(monsters_count, 325)

    def test_item_info(self):
        url = api.get_item_url('Club', self.list_of_dics)
        item_info = api.get_api_all(api.call_api(url))
        item_id = api.get_nested_api_dict(item_info, '_id')
        item_cost = api.get_nested_api_dict(item_info, 'cost')
        self.assertEqual(item_id, '5bce91275b7768e792017da3')
        self.assertEqual(item_cost['quantity'], 1)
        self.assertEqual(item_cost['unit'], 'sp')

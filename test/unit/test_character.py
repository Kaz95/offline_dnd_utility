import unittest
import mock
import character
import sql


class TestPlayer(unittest.TestCase):

    def setUp(self):
        print('----------setup-----------')
        self.player = character.Character(1, 'kaz', 5000, [])

    def tearDown(self):
        print('-------tear down--------\n')

# TODO: may need to make an integration test with DB being added to it

    # def test_add_currency(self):
    #     self.player.add_currency(100)
    #     self.assertEqual(self.player.currency, 5100)

    # def test_subtract_currency(self):
    #     self.player.subtract_currency(100)
    #     self.assertEqual(self.player.currency, 4900)


class TestPlayerClassIntegration(unittest.TestCase):

    def test_add_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            fake_player = character.Character(1, 'kaz', 5000, [])
            conn = mocksql.connect()
            fake_player.add_item(conn, 'Club', 1, 1)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_item_row(),
                                                                  (1, 1, 1, 'Club',
                                                                   'http://www.dnd5eapi.co/api/equipment/1', 1))

    def test_buy_sell_buy(self):
        fake_player = character.Character(1, 'kaz', 5000, [])
        fake_player.buy_sell('Club', 'buy')
        self.assertEqual(fake_player.currency, 4990)

    def test_buy_sell_sell(self):
        fake_player = character.Character(1, 'kaz', 5000, [])
        fake_player.buy_sell('Club', 'sell')
        self.assertEqual(fake_player.currency, 5010)

    def test_convert_currency(self):
        fake_player = character.Character(1, 'kaz', 4374, [])
        converted_cur = fake_player.convert_currency()
        self.assertEqual(converted_cur, {'gp': 43, 'sp': 7, 'cp': 4})

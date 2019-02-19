import unittest
import mock
import player
import sql

class TestPlayer(unittest.TestCase):

    def test_add_item(self):
        with mock.patch('database.sqlite3') as mocksql:
            fake_player = player.Player(1, 'kaz', 5000, [])
            conn = mocksql.connect()
            fake_player.add_item(conn, 'Club', 1, 1)
            mocksql.connect().cursor().execute.assert_called_with(sql.sql_add_item_row(),
                                                                  (1, 1, 1, 'Club',
                                                                   'http://www.dnd5eapi.co/api/equipment/1', 1))

    def test_buy_sell_buy(self):
        fake_player = player.Player(1, 'kaz', 5000, [])
        fake_player.buy_sell('Club', 'buy')
        self.assertEqual(fake_player.currency, 4990)

    def test_buy_sell_sell(self):
        fake_player = player.Player(1, 'kaz', 5000, [])
        fake_player.buy_sell('Club', 'sell')
        self.assertEqual(fake_player.currency, 5010)

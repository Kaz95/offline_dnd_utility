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
            mocksql.connect().cursor().fetchone.return_value = (0,)
            fake_player = character.Character(1, 'kaz', 5000, [])
            conn = mocksql.connect()
            fake_player.add_item_db(conn, 'Club', 1, 1)
            mocksql.connect().execute.assert_called_with(sql.add_item_row(),
                                                                  (1, 1, 1, 'Club',
                                                                   0, 0,  1))

    def test_buy_sell_buy(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            fake_player = character.Character(1, 'kaz', 5000, [])
            fake_player.buy_sell('Club', 'buy', conn)
            self.assertEqual(fake_player.currency, 4990)
            mocksql.connect().execute.assert_called_with(sql.update_currency(), (4990, 1))

    def test_buy_sell_sell(self):
        with mock.patch('database.sqlite3') as mocksql:
            conn = mocksql.connect()
            fake_player = character.Character(1, 'kaz', 5000, [])
            fake_player.buy_sell('Club', 'sell', conn)
            self.assertEqual(fake_player.currency, 5010)
            mocksql.connect().execute.assert_called_with(sql.update_currency(), (5010, 1))

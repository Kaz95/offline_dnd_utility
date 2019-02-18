import unittest
import player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        print('----------setup-----------')
        self.player = player.Player(1, 'kaz', 5000, [])

    def tearDown(self):
        print('-------tear down--------\n')

    def test_add_currency(self):
        self.player.add_currency(100)
        self.assertEqual(self.player.currency, 5100)

    def test_subtract_currency(self):
        self.player.subtract_currency(100)
        self.assertEqual(self.player.currency, 4900)

import unittest
import player


class TestPlayer(unittest.TestCase):

    def test_convert_currency(self):
        fake_player = player.Player(1, 'kaz', 4374, [])
        converted_cur = fake_player.convert_currency()
        self.assertEqual(converted_cur, {'gp': 43, 'sp': 7, 'cp': 4})

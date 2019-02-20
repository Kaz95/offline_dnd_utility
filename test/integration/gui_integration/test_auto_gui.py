import unittest
import auto_gui


class TestGUI(unittest.TestCase):

    def test_auto_gui(self):
        auto_gui.full_click('login')
        auto_gui.full_click('create')
        auto_gui.full_click('select')
        auto_gui.full_click('net')
        auto_gui.full_click('buy')
        auto_gui.full_click('greatclub')
        auto_gui.full_click('buy')
        auto_gui.full_click('donkey')
        auto_gui.full_click('buy')
        auto_gui.full_click('sailing_ship')
        auto_gui.full_click('buy')
        auto_gui.full_click('net')
        auto_gui.full_click('sell')
        auto_gui.full_click('greatclub')
        auto_gui.full_click('sell')
        auto_gui.full_click('donkey')
        auto_gui.full_click('sell')
        auto_gui.full_click('sailing_ship')
        auto_gui.full_click('sell')
        auto_gui.full_click('test')


import pyautogui
# pyautogui.PAUSE = 2
pyautogui.FAILSAFE = True


def button_path(some_button):
    button_string = 'C:\\Users\\Terrance\\Desktop\\button_screens\\{}.png'.format(some_button)
    return button_string


def locate_button(some_button):
    return pyautogui.locateOnScreen(some_button)


def center_mouse(some_button_location):
    return pyautogui.center(some_button_location)


def click_button(some_button_center):
    pyautogui.click(some_button_center)


def full_click(some_button):
    string_path = button_path(some_button)
    button_location = locate_button(string_path)
    button_center = center_mouse(button_location)
    click_button(button_center)


if __name__ == '__main__':
    full_click('login')
    full_click('create')
    full_click('select')
    full_click('net')
    full_click('buy')
    full_click('greatclub')
    full_click('buy')
    full_click('donkey')
    full_click('buy')
    full_click('sailing_ship')
    full_click('buy')
    full_click('net')
    full_click('sell')
    full_click('greatclub')
    full_click('sell')
    full_click('donkey')
    full_click('sell')
    full_click('sailing_ship')
    full_click('sell')
    full_click('tes')

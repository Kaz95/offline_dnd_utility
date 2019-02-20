from tkinter import *
from pages import login_page


def run():
    root = Tk()
    login_page(root)
    root.mainloop()


if __name__ == '__main__':
    run()

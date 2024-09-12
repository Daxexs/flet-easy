import flet as ft

import flet_easy as fs


class CounterC:
    def __init__(self):
        self.button_remove = fs.Ref[ft.IconButton]()
        self.button_add = fs.Ref[ft.IconButton]()
        self.txt_number = fs.Ref[ft.TextField]()

    def minus_click(self, e):
        self.txt_number.c.value = str(int(self.txt_number.c.value) - 1)
        self.txt_number.c.update()

    def plus_click(self, e):
        self.txt_number.c.value = str(int(self.txt_number.c.value) + 1)
        self.txt_number.c.update()

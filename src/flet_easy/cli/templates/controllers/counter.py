import flet as ft
from flet_easy import Ref


class CounterHook:
    def __init__(self):
        self.number = Ref[ft.TextButton]()
        self.input = Ref[ft.TextField]()
        self.alert = Ref[ft.SnackBar]()

    def get_input(self):
        return (
            int(self.input.c.value)
            if self.input.c.value is not None and self.input.c.value != ""
            else 1
        )

    def is_number(self):
        if not self.input.c.value.isdigit():
            self.alert.c.content = ft.Text("Enter number", text_align="center", color="#ffffff")
            self.alert.c.bgcolor = "#ef233c"
            self.alert.c.open = True
            self.alert.c.update()
            return False
        return True

    def add(self, e):
        if self.is_number():
            self.number.c.text = str(int(self.number.c.text) + self.get_input())
            self.number.c.update()

    def remove(self, e):
        if self.is_number():
            self.number.c.text = str(int(self.number.c.text) - self.get_input())
            self.number.c.update()

    def reload(self, e):
        self.number.c.text = "0"
        self.input.c.value = "1"
        self.input.c.update()
        self.number.c.update()

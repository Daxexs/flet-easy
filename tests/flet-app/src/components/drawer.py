import flet as ft


class Drawer(ft.FilledButton):
    def __init__(self, text: str, drawer: ft.NavigationDrawer, **kwargs):
        super().__init__(**kwargs)
        self.drawer = drawer
        self.text = text
        self.bgcolor = ft.Colors.RED_500
        self.color = ft.Colors.WHITE
        self.on_click = self.show_drawer

    def show_drawer(self, e):
        self.drawer.open = True
        self.page.update()

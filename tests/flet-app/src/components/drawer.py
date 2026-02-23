import flet as ft


class Drawer(ft.FilledButton):
    def __init__(self, text: str, drawer: ft.NavigationDrawer):
        super().__init__(text, on_click=self.show_drawer)
        self.drawer = drawer
        self.bgcolor = ft.Colors.RED_500
        self.color = ft.Colors.WHITE

    def show_drawer(self, e):
        self.drawer.open = True
        self.page.update()

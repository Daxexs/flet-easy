import flet as ft


class Drawer(ft.FilledButton):
    def __init__(self, text: str, drawer: ft.NavigationDrawer):
        super().__init__(text)
        self.drawer = drawer
        self.bgcolor = ft.Colors.RED_500
        self.color = ft.Colors.WHITE
        self.on_click = self.show_drawer

    async def show_drawer(self, e):
        if hasattr(self.drawer, "open"):
            self.drawer.open = True
            self.page.update()
        else:
            await self.page.show_drawer()

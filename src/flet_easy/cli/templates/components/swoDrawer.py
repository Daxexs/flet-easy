from flet import FilledButton, NavigationDrawer


class SwoDrawer(FilledButton):
    def __init__(
        self, text: str, drawer: NavigationDrawer, close: bool = False, **kwargs
    ) -> FilledButton:
        super().__init__(**kwargs)
        self.drawer = drawer
        self.close = close
        self.text = text
        self.on_click = self.go_url

    def go_url(self, e):
        if not self.close:
            self.drawer.open = True
        else:
            self.drawer.open = False

        self.page.update()

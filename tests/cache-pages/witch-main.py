import asyncio
import random

import flet as ft

import flet_easy as fs

app = fs.FletEasy()


# remove animation on route change
@app.config
def config(page: ft.Page):
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.NONE,
            android=ft.PageTransitionTheme.NONE,
            ios=ft.PageTransitionTheme.NONE,
            macos=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
        ),
    )


# use in 'data.view'
@app.view
def config_view(data: fs.Datasy):
    def change_color(e: ft.ControlEvent):
        colors = [ft.Colors.RED, ft.Colors.GREEN, ft.Colors.BLUE, ft.Colors.YELLOW]
        appbar.bgcolor = random.choice(colors)
        data.page.update()

    appbar = ft.AppBar(
        bgcolor=ft.Colors.BLACK45,
        actions=[
            ft.IconButton(
                icon=ft.Icons.RESTART_ALT_ROUNDED,
                icon_color=ft.Colors.WHITE,
                on_click=change_color,
            )
        ],
    )

    return ft.View(
        appbar=appbar,
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.CODE, label="counter 1"),
                ft.NavigationBarDestination(icon=ft.Icons.SYNC_DISABLED, label="counter 2"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.CODE,
                    label="counter 3",
                ),
            ],
            on_change=data.go_navigation_bar,
        ),
    )


# control custom
class Counter(ft.Container):
    def __init__(self, update, color: str):
        super().__init__()
        self.update = update

        self.number = ft.TextField(value="0", text_size=50, text_align="center")
        self.content = ft.Column(
            controls=[
                self.number,
                ft.FilledButton("start", on_click=self.start, height=50),
            ],
            horizontal_alignment="center",
        )
        self.width = 400
        self.bgcolor = color
        self.border_radius = 10
        self.padding = 20

    async def start(self, e):
        while True:
            self.number.value = str(int(self.number.value) + 1)
            self.update()
            await asyncio.sleep(1)


class Middleware(fs.MiddlewareRequest):
    def before_request(self):
        print("Middleware before_request:", self.data.page.views)

    def after_request(self):
        print("Middleware after_request:", self.data.page.views)


app.add_middleware(Middleware)


@app.page("/", title="Test 1", index=0, cache=True)
def index_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    def update_appbar_title(e: ft.AppBar):
        e.title = ft.Text("Test 1")
        page.update()

    data.dynamic_control(control=appbar, func_update=update_appbar_title)

    page.client_storage.set("counter", 5)

    return ft.View(
        controls=[
            ft.Text("Counter 1", size=50),
            Counter(page.update, ft.Colors.RED),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        horizontal_alignment="center",
        vertical_alignment="center",
    )


@app.page("/test2", title="Test 2", index=1)
def test_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    appbar.title = ft.Text("Test 2")
    counter = page.client_storage.get("counter")

    return ft.View(
        controls=[
            ft.Text("Disabled cache - Counter 2 ", size=50),
            ft.Text(f"client_storage: {counter}"),
            Counter(page.update, ft.Colors.BLUE),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# add cache to the page
@app.page("/test3", title="Test 3", index=2, cache=True)
async def test2_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    async def update_appbar_title(e: ft.AppBar):
        e.title = ft.Text("Test 3")
        page.update()

    data.dynamic_control(control=appbar, func_update=update_appbar_title)

    return ft.View(
        controls=[
            ft.Text("Counter 3", size=50),
            ft.Text(f"client_storage: {await page.client_storage.get_async('counter')}", size=50),
            Counter(page.update, ft.Colors.GREEN),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        horizontal_alignment="center",
        vertical_alignment="center",
    )


app.run()

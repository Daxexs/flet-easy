import asyncio
import random

import flet as ft

import flet_easy as fs

# compatible with flet >= 0.27.0

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
        print("Middleware before_request:", self.data.route)

    def after_request(self):
        print("Middleware after_request:", self.data.route)


app.add_middleware(Middleware)


# add page 1
@fs.page("/", title="Test 1", index=0)
def index_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    appbar.title = ft.Text("Test 1")

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


# add page 2
@fs.page("/test2", title="Test 2", index=1)
def test_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    appbar.title = ft.Text("Test 2")

    return ft.View(
        controls=[
            ft.Text("Disabled cache - Counter 2 ", size=50),
            Counter(page.update, ft.Colors.BLUE),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# add page 3
@fs.page("/test3", title="Test 3", index=2)
def test2_page(data: fs.Datasy):
    page = data.page
    appbar = data.view.appbar

    appbar.title = ft.Text("Test 3")

    return ft.View(
        controls=[
            ft.Text("Counter 3", size=50),
            Counter(page.update, ft.Colors.GREEN),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        horizontal_alignment="center",
        vertical_alignment="center",
    )


app.run()

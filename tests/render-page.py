import asyncio
from dataclasses import dataclass

import flet as ft

import flet_easy as fs

app = fs.FletEasy()


@dataclass
@ft.observable
class CounterState:
    count: int = 0

    def add(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def remove(self):
        self.count -= 1


# counter
@ft.component
def counter():
    state, _ = ft.use_state(CounterState())

    return ft.Column(
        controls=[
            ft.Text(value=f"{state.count}", size=30),
            ft.Row(
                controls=[
                    ft.Button("Add", on_click=state.add),
                    ft.Button("Remove", on_click=state.remove),
                    ft.Button("Reset", on_click=state.reset),
                ],
                alignment="center",
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )


class middleware_routes(fs.MiddlewareRequest):
    def before_request(self):
        print(f"route: {self.data.route} - before home")

    def after_request(self):
        print(f"route: {self.data.route} - after home")


# add middlewares to all routes
app.add_middleware(middleware_routes)


def middleware_home(data: fs.Datasy):
    data.page.show_dialog(ft.SnackBar(ft.Text(f"route: {data.route} - Hello from middleware!")))


# use component
@ft.component
@app.page(route="/", title="Home", middleware=middleware_home, cache=True)
def App(data: fs.Datasy):

    async def go_test():
        await ft.context.page.push_route("/test")

    return ft.View(
        controls=[
            counter(),
            ft.Button("go test", on_click=go_test),
            ft.Button("go progress-bar", on_click=data.go("/add-pagesy/progress-bar")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# use function
@app.page(route="/test", title="test")
def test(data: fs.Datasy):

    return ft.View(
        controls=[
            ft.Text("test"),
            ft.Button("go back", on_click=data.go("/")),
            ft.Button("go test3", on_click=data.go("/add-pagesy/progress-bar")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@dataclass
@ft.observable
class AppState:
    counter: float

    async def start_counter(self):
        self.counter = 0
        for _ in range(0, 10):
            self.counter += 0.1
            await asyncio.sleep(0.5)


# Test the import of the app the diferent file
app2 = fs.AddPagesy(
    route_prefix="/add-pagesy",
    middleware=middleware_home,
)


@ft.component
@app2.page(route="/progress-bar", title="progress-bar")
def progress_bar(data: fs.Datasy):
    state, _ = ft.use_state(AppState(counter=0))

    async def go_back():
        await ft.context.page.push_route("/")

    return ft.View(
        controls=[
            ft.ProgressBar(state.counter),
            ft.Button("Run!", on_click=state.start_counter),
            ft.Button("go back", on_click=go_back),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


app.add_pages([app2])

app.run()

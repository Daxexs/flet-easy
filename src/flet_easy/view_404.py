from flet import (
    ButtonStyle,
    Column,
    Container,
    FilledButton,
    Page,
    Text,
    View,
    colors,
)


class ViewError:
    def __init__(self, route_index: str) -> None:
        self.route = "/Flet-Easy-404"
        self.route_index = route_index

    def view(self, page: Page) -> View:
        page.title = "page 404"

        return View(
            self.route,
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Text("404", size=90),
                            Text("url not found!"),
                            FilledButton(
                                "go to Home",
                                width=200,
                                height=40,
                                on_click=lambda e: e.page.go(self.route_index),
                                style=ButtonStyle(
                                    bgcolor=colors.RED_500,
                                    color=colors.WHITE,
                                ),
                            ),
                        ],
                        alignment="center",
                        horizontal_alignment="center",
                    ),
                    bgcolor=colors.BLACK12,
                    padding=20,
                    border_radius=10,
                )
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )

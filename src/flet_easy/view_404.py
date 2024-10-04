from flet import (
    ButtonStyle,
    Column,
    Container,
    FilledButton,
    Text,
    View,
    colors,
)

from flet_easy.datasy import Datasy


def page_404_fs(data: Datasy) -> View:
    return View(
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
                            on_click=data.go(data.route_init),
                            style=ButtonStyle(
                                bgcolor=colors.RED_900,
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

from flet import (
    ButtonStyle,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    FilledButton,
    MainAxisAlignment,
    Text,
    View,
)

from flet_easy.core.data import Datasy


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
                                bgcolor=Colors.RED_900,
                                color=Colors.WHITE,
                            ),
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                bgcolor=Colors.BLACK12,
                padding=20,
                border_radius=10,
            )
        ],
        vertical_alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

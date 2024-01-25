from flet import (
    View,
    Page,
    Column,
    Container,
    Text,
    FilledButton,
    ButtonStyle,
    colors,
    MainAxisAlignment,
    CrossAxisAlignment,
)


class ViewError:
    def __init__(self) -> None:
        self.route = "/404-Routing-Flet"
        self.route_index = None

    def view(self, page: Page) -> View:
        page.title = "page 404"

        return View(
            self.route,
            controls=[
                Column(
                    [
                        Container(
                            content=Column(
                                controls=[
                                    Text("404", size=90),
                                    Text("url no encontrada:"),
                                    FilledButton(
                                        "ir a Home",
                                        width=200,
                                        height=40,
                                        on_click=lambda e: e.page.go(self.route_index),
                                        style=ButtonStyle(
                                            bgcolor=colors.AMBER_300,
                                            color=colors.WHITE70,
                                        ),
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=colors.LIGHT_BLUE_500,
                            padding=20,
                            border_radius=10,
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.CENTER,
                )
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

    async def view_async(self, page: Page) -> View:
        page.title = "page 404"

        async def go_index(e):
            await page.go_async(self.route_index)

        return View(
            self.route,
            controls=[
                Column(
                    [
                        Container(
                            content=Column(
                                controls=[
                                    Text("404", size=90),
                                    Text("url no encontrada:"),
                                    FilledButton(
                                        "ir a Home",
                                        width=200,
                                        height=40,
                                        on_click=go_index,
                                        style=ButtonStyle(
                                            bgcolor=colors.AMBER_300,
                                            color=colors.WHITE70,
                                        ),
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=colors.LIGHT_BLUE_500,
                            padding=20,
                            border_radius=10,
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    alignment=MainAxisAlignment.CENTER,
                )
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

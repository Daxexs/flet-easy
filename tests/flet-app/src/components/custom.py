import flet as ft


class Custom:
    def __init__():
        pass

    def custom_appbar(self):
        return ft.AppBar(
            title=ft.Text("App - Using a class as a view"),
            actions=[
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            "Go back",
                            on_click=self.data.go_back(),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_600,
                            ),
                        ),
                        ft.FilledButton(
                            "Page 2",
                            on_click=self.data.go("/counter/ts"),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.AMBER_500,
                            ),
                        ),
                    ]
                )
            ],
        )

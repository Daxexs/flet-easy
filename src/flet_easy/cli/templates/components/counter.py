import flet as ft
from controllers import CounterHook


class Counter(ft.UserControl):
    def __init__(
        self, page: ft.Page, id: str, width: int | float, height: int | float = None
    ) -> ft.Control:
        super().__init__()
        self.counter = CounterHook()
        self.id = id
        self.height = height
        self.width = width
        self.page = page
        self.page.snack_bar = ft.SnackBar(ref=self.counter.alert, content=ft.Text(""))

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.icons.REMOVE,
                                bgcolor=ft.colors.RED_900,
                                on_click=self.counter.remove,
                            ),
                            ft.TextButton(
                                ref=self.counter.number,
                                text=self.id,
                                style=ft.ButtonStyle(bgcolor=ft.colors.BLACK26),
                            ),
                            ft.IconButton(
                                ft.icons.ADD,
                                bgcolor=ft.colors.GREEN_900,
                                on_click=self.counter.add,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                ref=self.counter.input,
                                label="value",
                                value="1",
                                expand=True,
                            ),
                            ft.FilledButton("Reload", on_click=self.counter.reload, expand=True),
                        ]
                    ),
                ]
            ),
            bgcolor="#0353a4",
            blur=ft.Blur(10, 10, ft.BlurTileMode.REPEATED),
            padding=10,
            border_radius=10,
            border=ft.border.all(1),
            alignment=ft.alignment.center,
            height=self.height,
            width=self.width,
        )

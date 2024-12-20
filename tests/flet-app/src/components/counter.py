import flet as ft
from controllers import CounterC

import flet_easy as fs


class Counter(ft.Container):
    def __init__(self, resize: fs.Resizesy, id: int = None):
        super().__init__()
        self.counter = CounterC()
        self.id = id
        self.resize = resize
        self.padding = 20
        self.content = ft.ResponsiveRow(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ref=self.counter.button_remove,
                            icon=ft.Icons.REMOVE,
                            on_click=self.counter.minus_click,
                        ),
                        ft.TextField(
                            ref=self.counter.txt_number,
                            value=self.id,
                            text_align="center",
                            expand=True,
                        ),
                        ft.IconButton(
                            ref=self.counter.button_add,
                            icon=ft.Icons.ADD,
                            on_click=self.counter.plus_click,
                        ),
                    ],
                    col={"xs": 12, "sm": 10, "md": 8, "lg": 5, "xl": 4, "xxl": 3},
                    alignment="center",
                ),
            ],
            alignment="center",
        )

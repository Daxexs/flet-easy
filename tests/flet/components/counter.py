import flet as ft
import flet_easy as fs
from controllers import CounterC


class Counter(ft.Container):
    def __init__(self, resize: fs.Resizesy, id: int = None):
        super().__init__()
        self.counter = CounterC()
        self.id = id
        self.resize = resize
        self.padding = 20
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ref=self.counter.button_remove,
                            icon=ft.icons.REMOVE,
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
                            icon=ft.icons.ADD,
                            on_click=self.counter.plus_click,
                        ),
                    ],
                    alignment="center",
                ),
            ]
        )
        self.width = self.resize.widthX(50)

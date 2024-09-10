import flet as ft
from controllers import RegisterC

import flet_easy as fs


class Register(ft.Container):
    def __init__(self, data: fs.Datasy, redirect: str):
        super().__init__()
        self.register = RegisterC(data, redirect)
        self.content = ft.Column(
            controls=[
                ft.Text("Register", size=30),
                ft.TextField(
                    ref=self.register.username,
                    label="Username",
                ),
                ft.TextField(
                    ref=self.register.password,
                    label="Password",
                ),
                ft.FilledButton("Register", on_click=self.register.add),
                ft.TextButton("Login", on_click=data.go("/login")),
            ],
            horizontal_alignment="center",
        )

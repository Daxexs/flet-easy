import flet as ft
import flet_easy as fs
from controllers import LoginC


class Login(ft.Container):
    def __init__(self, data: fs.Datasy, redirect: str):
        super().__init__()
        self.login = LoginC(data, redirect)
        self.content = ft.Column(
            controls=[
                ft.Text("Login", size=30),
                ft.TextField(
                    ref=self.login.username,
                    label="Username",
                ),
                ft.TextField(
                    ref=self.login.password,
                    label="Password",
                ),
                ft.FilledButton("Login", on_click=self.login.check),
                ft.TextButton("Register", on_click=data.go("/register")),
            ],
            horizontal_alignment="center",
        )

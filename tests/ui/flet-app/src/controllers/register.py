from datetime import timedelta

import flet as ft
from models.methods import User, add_user

import flet_easy as fs


class RegisterC:
    def __init__(self, data: fs.Datasy, redirect: str) -> None:
        self.data = data
        self.redirect = redirect
        self.username = fs.Ref[ft.TextField]()
        self.password = fs.Ref[ft.TextField]()

    def show_snack_bar(self, text: str) -> None:
        if hasattr(self.data.page, "open"):
            self.data.page.open(ft.SnackBar(content=ft.Text(text)))
        else:
            self.data.page.show_dialog(ft.SnackBar(content=ft.Text(text)))

    async def add(self, e) -> None:
        username = self.username.c.value or ""
        password = self.password.c.value or ""

        if username and password:
            if not await add_user(User(username=username, password=password)):
                self.show_snack_bar("The user already exists")
            else:
                await self.data.login_async(
                    key="login",
                    value={"user": username},
                    time_expiry=timedelta(seconds=10),
                    next_route="/dashboard",
                )
        else:
            self.show_snack_bar("Enter the data")

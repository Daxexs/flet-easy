from datetime import timedelta

import flet as ft
from models.methods import User, check_user

import flet_easy as fs


class LoginC:
    def __init__(self, data: fs.Datasy, redirect: str):
        self.data = data
        self.redirect = redirect
        self.username = fs.Ref[ft.TextField]()
        self.password = fs.Ref[ft.TextField]()
        self.time_logout = fs.Ref[ft.TextField]()

    async def check(self, e):
        username = (
            self.username.c.value
            if self.username.c.value != "" and self.username.c.value
            else False
        )

        password = (
            self.password.c.value
            if self.password.c.value != "" and self.password.c.value
            else False
        )

        if username and password:
            if not await check_user(User(username=username, password=password)):
                self.data.page.snack_bar = ft.SnackBar(
                    content=ft.Text("User does not exist"), action="Alright!", open=True
                )
            else:
                await self.data.login_async(
                    key="login",
                    value={"user": username},
                    time_expiry=timedelta(seconds=int(self.time_logout.c.value)),
                    next_route="/dashboard",
                )
        else:
            self.data.page.snack_bar = ft.SnackBar(
                content=ft.Text("Enter the data"), action="Alright!", open=True
            )
        self.data.page.update()

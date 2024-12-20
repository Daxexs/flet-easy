from datetime import timedelta

import flet as ft
from models.methods import User, add_user

import flet_easy as fs


class RegisterC:
    def __init__(self, data: fs.Datasy, redirect: str):
        self.data = data
        self.redirect = redirect
        self.username = fs.Ref[ft.TextField]()
        self.password = fs.Ref[ft.TextField]()

    def add(self, e):
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
            if not e.page.run_task(add_user, User(username=username, password=password)).result():
                self.data.page.snack_bar = ft.SnackBar(
                    content=ft.Text("The user already exists"), action="Alright!", open=True
                )
            else:
                self.data.login(
                    key="login",
                    value={"user": username},
                    time_expiry=timedelta(seconds=10),
                    next_route="/dashboard",
                )
        else:
            self.data.page.snack_bar = ft.SnackBar(
                content=ft.Text("Enter the data"), action="Alright!", open=True
            )
        self.data.page.update()

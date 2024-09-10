import flet as ft
from components import Drawer, Login, Register

import flet_easy as fs

login = fs.AddPagesy()


def login_check(data: fs.Datasy):
    print("Loading the page Login!")


@login.page("/login", title="Login", middleware=[login_check])
async def login_request(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={
                            "xs": 10,
                            "sm": 5,
                            "md": 5,
                            "lg": 3,
                            "xl": 3,
                        },
                        controls=[
                            Drawer("Menu", data.view.drawer),
                            Login(data, "/dashboard"),
                        ],
                    ),
                ],
                vertical_alignment="center",
                alignment="center",
            )
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        drawer=data.view.drawer,
        appbar=data.view.appbar,
    )


@login.page("/register", title="Register")
def register_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        col={
                            "xs": 10,
                            "sm": 5,
                            "md": 5,
                            "lg": 3,
                            "xl": 3,
                        },
                        controls=[
                            Drawer("Menu", data.view.drawer),
                            Register(data, "/dashboard"),
                        ],
                    ),
                ],
                vertical_alignment="center",
                alignment="center",
            )
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        drawer=data.view.drawer,
        appbar=data.view.appbar,
    )

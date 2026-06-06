from time import sleep

import flet as ft

import flet_easy as fs

login = fs.AddPagesy(route_prefix="/login")


class Login(ft.UserControl):
    def __init__(self, page, data: fs.Datasy):
        super().__init__()
        self.page = page
        self.data: fs.Datasy = data
        self.username = ft.TextField(
            label="Username",
        )
        self.password = ft.TextField(
            label="Password",
        )
        self.menssage = ft.Column()

    def login(self, e):
        if self.username.value and self.password.value:
            # Registering in the client's storage the key and value in all browser sessions.
            self.data.login(
                "login", self.username.value, next_route=f"{self.data.route_prefix}/counter"
            )
        else:
            if len(self.menssage.controls) == 0:
                self.menssage.controls.append(ft.Text("Enter the fields"))
                self.update()
                sleep(3)
                self.menssage.controls.clear()
                self.update()

    def build(self):
        conteiner = ft.Container(
            col={"xs": 10, "sm": 10, "md": 2, "lg": 2, "xl": 3, "xxl": 3},
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=30),
                    self.username,
                    self.password,
                    self.menssage,
                    ft.Text("Test login require in page (protected route)"),
                    ft.ElevatedButton("Login", on_click=self.login),
                    ft.ElevatedButton(
                        "Go to Index",
                        on_click=self.data.go(self.data.route_init),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_500,
            padding=20,
            border_radius=10,
        )
        return ft.ResponsiveRow(controls=[conteiner], alignment=ft.MainAxisAlignment.CENTER)


@login.page("/user", title="Login")
async def login_page(data: fs.Datasy):
    page = data.page
    view = data.view

    view.appbar.title = ft.Text("Login")

    """ add controls personalization """
    conteiner_login = Login(page, data)

    return ft.View(
        controls=[
            conteiner_login,
            ft.FilledButton("go resize", on_click=data.go(f"{data.route_prefix}/resize")),
        ],
        appbar=view.appbar,
        vertical_alignment=view.vertical_alignment,
        horizontal_alignment=view.horizontal_alignment,
    )

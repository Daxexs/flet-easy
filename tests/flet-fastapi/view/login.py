import flet as ft
import flet_easy as fs
import asyncio

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

    async def login(self, e):
        if self.username.value and self.password.value:
            # Registering in the client's storage the key and value in all browser sessions.
            await self.data.update_login_async("login", self.username.value)
            await self.page.go_async(f"{self.data.route_prefix}/counter")
        else:
            if len(self.menssage.controls) == 0:
                self.menssage.controls.append(ft.Text("Enter the fields"))
                await self.update_async()
                await asyncio.sleep(3)
                self.menssage.controls.clear()
                await self.update_async()

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
                        key=self.data.route_init,
                        on_click=self.data.go_async,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.BLUE_500,
            padding=20,
            border_radius=10,
        )
        return ft.ResponsiveRow(
            controls=[conteiner], alignment=ft.MainAxisAlignment.CENTER
        )


@login.page("/user")
async def login_page(data: fs.Datasy):
    page = data.page
    view = data.view
    page.title = "login"

    view.appbar.title = ft.Text("Login")

    """ add controls personalization """
    conteiner_login = Login(page, data)

    return ft.View(
        route="/user",
        controls=[conteiner_login],
        appbar=view.appbar,
        vertical_alignment=view.vertical_alignment,
        horizontal_alignment=view.horizontal_alignment,
    )

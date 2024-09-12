import flet as ft

import flet_easy as fs


class ConfigApp:
    def __init__(self, app: fs.FletEasy):
        self.app = app
        self.start()

    def start(self):
        @self.app.login
        async def login_required(data: ft.Page):
            # Using Jwt to authenticate user, which has been previously configured with the `data.login()` method.
            return await fs.decode_async(key_login="login", data=data)

        @self.app.view
        async def view_config(data: fs.Datasy):
            return fs.Viewsy(
                appbar=ft.AppBar(title=ft.Text("Flet-Easy")),
                drawer=ft.NavigationDrawer(
                    controls=[
                        ft.Container(height=12),
                        ft.Column(
                            controls=[
                                ft.Text("Navigation", size=25),
                                ft.Divider(thickness=2),
                                ft.FilledButton(
                                    text="Home",
                                    on_click=data.go(data.route_init),
                                ),
                                ft.FilledButton(
                                    text="Counter",
                                    on_click=data.go("/counter/test/10"),
                                ),
                                ft.FilledButton(
                                    text="Share Data",
                                    on_click=data.go("/share/send-data"),
                                ),
                                ft.FilledButton(
                                    text="Login",
                                    on_click=data.go("/login"),
                                ),
                                ft.FilledButton(
                                    text="Dashboard",
                                    on_click=data.go("/dashboard"),
                                ),
                                ft.FilledButton("Go back", on_click=data.go_back()),
                                ft.FilledButton(
                                    text="Logout",
                                    on_click=data.logout("login"),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
            )

        @self.app.config
        def page_config(page: ft.Page):
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:  # Removing animation on route change.
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)
            page.theme = theme

        @self.app.config_event_handler
        async def event_handler(data: fs.Datasy):
            page = data.page

            async def on_disconnect(e):
                print("Disconnect test application")

            page.on_disconnect = on_disconnect

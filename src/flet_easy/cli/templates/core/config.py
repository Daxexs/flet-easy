import flet as ft
import flet_easy as fs


class ConfigApp:
    def __init__(self, app: fs.FletEasy):
        self.app = app
        self.start()

    def start(self):
        @self.app.view
        def view_config(data: fs.Datasy):
            return fs.Viewsy(
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
                                    on_click=data.go("/counter/test/0"),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                )
            )

        @self.app.config
        def page_config(page: ft.Page):
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:  # Removing animation on route change.
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)
            page.theme = theme

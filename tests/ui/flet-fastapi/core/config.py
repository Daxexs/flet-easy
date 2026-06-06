import flet as ft

import flet_easy as fs


class ConfigApp:
    def __init__(self, app: fs.FletEasy) -> None:
        self.app = app
        self.start()

    def start(self):
        """ " route protection configuration"""

        @self.app.login
        async def login_x(data: fs.Datasy):
            username = await data.page.client_storage.get_async("login")
            return username is not None

        """" general configuration of the charter page """

        @self.app.config
        async def config(page: ft.Page):
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:  # Removing animation on route change.
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)

            theme.text_theme = ft.TextTheme()
            page.theme = theme

        """" add universal controls to use on more than one page in an easy way """

        @self.app.view
        async def view(data: fs.Datasy):
            page = data.page

            def modify_theme():
                if page.theme_mode == ft.ThemeMode.DARK:
                    page.theme_mode = ft.ThemeMode.LIGHT
                else:
                    page.theme_mode = ft.ThemeMode.DARK

            async def theme(e):
                if page.theme_mode == ft.ThemeMode.SYSTEM:
                    modify_theme()

                modify_theme()
                await page.update_async()

            async def reload(e):
                await page.launch_url_async(
                    url=page.route,
                    web_window_name="_self",
                )

            return fs.Viewsy(
                appbar=ft.AppBar(
                    title=ft.Text("AppBar Example"),
                    center_title=False,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    actions=[
                        ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED, on_click=theme),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(text="🔥 Home", on_click=data.go(data.route_init)),
                                ft.PopupMenuItem(
                                    text="❌ Logaut",
                                    on_click=data.logout("login"),
                                ),
                                ft.PopupMenuItem(text="🔃 Reload", on_click=reload),
                            ]
                        ),
                    ],
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        """ Add a custom page, which will be activated when a page (path) is not found. """

        @self.app.page_404("/FletEasy-404", title="Error 404", page_clear=True)
        async def page404(data: fs.Datasy):
            view = data.view

            view.appbar.title = ft.Text("Error 404")

            return ft.View(
                route="/error404",
                controls=[
                    ft.Text("Error 404", size=30),
                    ft.ElevatedButton(
                        "Go to Home",
                        on_click=data.go(data.route_init),
                    ),
                ],
                appbar=view.appbar,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        @self.app.config_event_handler
        async def event_handler(data: fs.Datasy):
            page = data.page

            async def on_disconnect_async(e):
                print("Disconnect test application")

            page.on_disconnect = on_disconnect_async

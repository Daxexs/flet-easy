import flet as ft
import flet_easy as fs

ROUTE = "/tools"


class ConfigApp:
    def __init__(self, app: fs.FletEasy) -> None:
        self.app = app
        self.start()

    def start(self):
        """ " route protection configuration"""

        @self.app.login
        async def login_x(page: ft.Page):
            username = await page.client_storage.get_async("login")
            if username is None:
                return False
            return True

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

            async def go_home(e):
                await page.go_async(data.route_init)

            async def logauth(e):
                await data.logaut_async("login")

            async def reload(e):
                await page.launch_url_async(
                    url=page.route,
                    web_window_name="_self",
                )

            return fs.Viewsy(
                appbar=ft.AppBar(
                    title=ft.Text("AppBar Example"),
                    center_title=False,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[
                        ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=theme),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(text="🔥 Home", on_click=go_home),
                                ft.PopupMenuItem(text="❌ Logaut", on_click=logauth),
                                ft.PopupMenuItem(text="🔃 Reload", on_click=reload),
                            ]
                        ),
                    ],
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        """ Add a custom page, which will be activated when a page (path) is not found. """

        @self.app.page_404("/FletEasy-404", page_clear=True)
        async def page404(data: fs.Datasy):
            page = data.page
            view = data.view
            page.title = "Error 404"
            view.appbar.title = ft.Text("Error 404")

            async def index_go(e):
                await page.go_async(ROUTE + "/hi")

            return ft.View(
                route="/error404",
                controls=[
                    ft.Text("Error 404", size=30),
                    ft.ElevatedButton(
                        "ir a index",
                        on_click=index_go,
                    ),
                ],
                appbar=view.appbar,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        @self.app.config_event_handler
        async def event_handler(page: ft.Page):
            async def on_disconnect_async(e):
                print("Disconnect test application")

            page.on_disconnect = on_disconnect_async

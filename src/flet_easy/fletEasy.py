try:
    from flet import Page, app, AppView, WebRenderer
except ImportError:
    raise Exception(
        'Install "flet" the latest version available -> pip install flet --upgrade.'
    )

from flet_easy.inheritance import Pagesy, Viewsy, AddPagesy
from flet_easy.route import FletEasyX
from functools import wraps
from typing import Callable, Optional


class FletEasy:
    """we create the app object, in it you can configure:
    * The path that is different from '/'.
    * The initial path when initializing the app
    * The path that will be redirected when the app has path protection configured.

    Example:
    ```python
    import flet as ft
    import flet_easy as fs

    app = fs.FletEasy(
        route_prefix='/index',
        route_init='/index/hi',
    )

    @app.view()
    async def view(page: ft.Page):
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
            await page.go_async('/index/hi')
        return fs.Viewsy(
            appbar=ft.AppBar(
                title=ft.Text("AppBar Example"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.IconButton(ft.icons.WB_SUNNY_OUTLINED,
                                  on_click=theme
                                  ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="🔥 Home",
                                on_click=go_home
                            ),
                        ]
                    ),
                ],
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    @app.page('/hi', page_clear=True)
    async def index_page(data: fs.Datasy):
        page = data.page
        view = data.view
        page.title = 'Index - Home'

        view.appbar.title = ft.Text('Index - Home')

        async def go_test(e):
            await page.go_async(f'/index/test/10/user/junior')


        return ft.View(
            '/index/hi',
            controls=[

                ft.Text('Menú', size=40),
                ft.ElevatedButton(
                    'Go to Test', on_click=go_test,
                )

            ],
            appbar=view.appbar,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    @app.page('/test/{id:d}/user/{name:l}')
    async def test_page(data: fs.Datasy, id:int, name:str):
        page = data.page
        view = data.view

        page.title = 'Test'
        view.appbar.title = ft.Text('test')

        async def go_index(e):
            await page.go_async(f'/index/hi')

        return ft.View(
            '/index/test',
            controls=[

                ft.Text(f'Test {data.url_params}'),
                ft.Text(f'Test Id is: {id}'),
                ft.ElevatedButton(
                    'Go to Home', on_click=go_index),

            ],
            appbar=view.appbar,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # Execute the app (synchronous / asynchronous)
    app.run()

    ```
    """

    def __init__(
        self,
        route_prefix: str = None,
        route_init: str = "/",
        route_login: str = None,
        on_resize: bool = False,
        on_Keyboard: bool = False,
        secret_key: str = None,
        auto_logout: bool = False,
    ):
        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__on_resize = on_resize
        self.__on_Keyboard = on_Keyboard
        self.__secret_key = secret_key
        self.__auto_logout = auto_logout
        self.__config_login: Callable = None
        # ----
        self.__pages = set()
        self.__page_404: Pagesy = None
        self.__view_data: Viewsy = None
        self.__view_config: Callable = None
        self.__config_event: Callable = None

    # -------------------------------------------------------------------
    # -- initialize / Supports async

    def run(
        self,
        name="",
        host=None,
        port=0,
        view: Optional[AppView] = AppView.FLET_APP,
        assets_dir="assets",
        upload_dir=None,
        web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
        use_color_emoji=False,
        route_url_strategy="path",
        export_asgi_app: bool = False,
        fastapi: bool = False,
    ) -> Page:
        """* Execute the app. | Supports async and fastapi."""

        def main(page: Page):
            app = FletEasyX(
                page=page,
                route_prefix=self.__route_prefix,
                route_init=self.__route_init,
                route_login=self.__route_login,
                config_login=self.__config_login,
                pages=self.__pages,
                page_404=self.__page_404,
                view_data=self.__view_data,
                view_config=self.__view_config,
                config_event_handler=self.__config_event,
                on_resize=self.__on_resize,
                on_Keyboard=self.__on_Keyboard,
                secret_key=self.__secret_key,
                auto_logout=self.__auto_logout,
            )

            app.run()

        if fastapi:
            return main
        try:
            app(
                target=main,
                name=name,
                host=host,
                port=port,
                view=view,
                assets_dir=assets_dir,
                upload_dir=upload_dir,
                web_renderer=web_renderer,
                use_color_emoji=use_color_emoji,
                route_url_strategy=route_url_strategy,
                export_asgi_app=export_asgi_app,
            )
        except RuntimeError:
            Exception(
                "If you are using fastapi from flet, set the 'fastapi = True' parameter of the run() method."
            )

    # -- decorators --------------------------------

    def __decorator(self, value: str, data: dict = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(data, *args, **kwargs):
                return func(data, *args, **kwargs)

            if data:
                if self.__route_prefix and data.get("route"):
                    route = (
                        self.__route_prefix
                        if data.get("route") == "/"
                        else self.__route_prefix + data.get("route")
                    )
                else:
                    route = data.get("route")

            if value == "page_404":
                self.__page_404 = Pagesy(route, func, data.get("title"), data.get("page_clear"))
            elif value == "page":
                self.__pages.add(
                    Pagesy(
                        route=route,
                        view=func,
                        title=data.get("title"),
                        clear=data.get("page_clear"),
                        share_data=data.get("share_data"),
                        protected_route=data.get("protected_route"),
                        custom_params=data.get("custom_params"),
                    )
                )
            return wrapper

        return decorator

    def add_pages(self, group_pages: list[AddPagesy]):
        """Add pages from other archives
        * In the list you enter objects of class `AddPagesy` from other .py files.

        Example:
        ```python
        app.add_pages([index, test, contador, login, task])
        ```
        """
        try:
            for page in group_pages:
                if self.__route_prefix:
                    self.__pages.update(page._add_pages(self.__route_prefix))
                else:
                    self.__pages.update(page._add_pages())
        except Exception as e:
            raise e

    def page(
        self,
        route: str,
        title: str = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: dict = None,
    ):
        """Decorator to add a new page to the app, you need the following parameters:
        * route: text string of the url, for example(`'/FletEasy'`).
        * `title` : Define the title of the page. (optional).
        * clear: Removes the pages from the `page.views` list of flet. (optional)
        * protected_route: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
        * custom_params: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.

        -> The decorated function must receive a parameter, for example `data:fs.Datasy`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy(
            route_prefix='/FletEasy',
            route_init='/FletEasy',
        )

        @app.page('/', title='FletEasy')
        async def index_page(data: fs.Datasy):
            return ft.View(
                route='/FletEasy',
                controls=[
                    ft.Text('FletEasy')
                ],
                vertical_alignment=view.vertical_alignment,
                horizontal_alignment=view.horizontal_alignment
            )
        ```
        """

        data = {
            "route": route,
            "title": title,
            "page_clear": page_clear,
            "share_data": share_data,
            "protected_route": protected_route,
            "custom_params": custom_params,
        }
        return self.__decorator("page", data)

    def page_404(
        self,
        route: str = None,
        title: str = None,
        page_clear: bool = False,
    ):
        """Decorator to add a new custom page when not finding a route in the app, you need the following parameters :
        * route: text string of the url, for example (`'/FletEasy-404'`). (optional).
        * `title` : Define the title of the page. (optional).
        * clear: remove the pages from the `page.views` list of flet. (optional)

        -> The decorated function must receive a mandatory parameter, for example: `data:fs.Datasy`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy(
            route_prefix='/FletEasy',
            route_init='/FletEasy',
        )

        @app.page_404('/FletEasy-404', title='Error 404', page_clear=True)
        async def page404(data: fs.Datasy):

            return ft.View(
                route='/error404',
                controls=[
                    ft.Text(f'Error 404', size=30),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ```
        """
        data = {"route": route, "title": title, "page_clear": page_clear}
        return self.__decorator("page_404", data)

    def view(self, func):
        """
        Decorator to add custom controls to the application, the decorator function will return the `Viewsy` class of `FletEasy`. Which will be obtained in functions with `data:fs.Datasy` parameter and can be added to the page view decorated with `data.view` of `FletEasy` class.

        * The decorator function must receive a mandatory parameter, for example: `data:ft.Datasy`.
        * Add universal controls to use on more than one page in an easy way.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy(
            route_prefix='/FletEasy',
            route_init='/FletEasy',
        )

        @app.view
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
                await page.go_async('/FletEasy')

            return fs.Viewsy(
                appbar=ft.AppBar(
                    title=ft.Text("AppBar Example"),
                    center_title=False,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[
                        ft.IconButton(ft.icons.WB_SUNNY_OUTLINED,
                                      on_click=theme
                                      ),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(
                                    text="🔥 Home",
                                    on_click=go_home
                                ),
                            ]
                        ),
                    ],
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ```
        """
        self.__view_data = func

    def config(self, func):
        """Decorator to add a custom configuration to the app:

        * The decorator function must receive a mandatory parameter, for example: `page:ft.Page`. Which can be used to make universal app configurations.
        * The decorator function does not return anything.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy()

        @app.config
        async def config(page: ft.Page):
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:  # Removing animation on route change.
                setattr(theme.page_transitions, platform,
                        ft.PageTransitionTheme.NONE)

            theme.text_theme = ft.TextTheme()
            page.theme = theme

        ```
        """
        self.__view_config = func

    def login(self, func):
        """Decorator to add a login configuration to the app (protected_route):

        * The decorator function must receive a mandatory parameter, for example: `page:ft.Page`. Which can be used to get information and perform universal settings of the app.
        * The decorator function must `return a boolean`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy()

        # Basic demo example for login test
        @app.login
        async def login_x(page: ft.Page):
            v = [False, True, False, False, True]
            value = v[random.randint(0, 4)]
            return value
        ```
        """
        self.__config_login = func

    def config_event_handler(self, func):
        """Decorator to add charter event settings -> https://flet.dev/docs/controls/page#events

        Example:
        ```python
        @app.config_event_handler
        async def event_handler(page: ft.Page):

            async def on_disconnect_async(e):
                print("Disconnect test application")

            page.on_disconnect = on_disconnect_async
        ```
        """

        self.__config_event = func

    def add_routes(self, add_views: list[Pagesy]):
        """-> Add routes without the use of decorators.

        Example:
        ```python
        app.add_routes(add_views=[
            fs.Pagesy('/hi', index_page, True),
            fs.Pagesy('/test/{id:d}/user/{name:l}', test_page, protected_route=True),
            fs.Pagesy('/counter', counter_page),
            fs.Pagesy('/task', task_page),
            fs.Pagesy('/login/user', login_page),
        ])
        ```
        """

        assert len(add_views) != 0, "add view (add_view) in 'add_routes'."
        for page in add_views:
            if self.__route_prefix:
                page.route = self.__route_prefix + page.route

            self.__pages.add(page)

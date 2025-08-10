import logging
from ctypes import Union

from flet_easy.exceptions import AddPagesError, FletEasyError, MidlewareError

try:
    from flet import AppView, Page, WebRenderer, app
except ImportError:
    raise FletEasyError(
        'Install "flet" the latest version available -> pip install flet[all] --upgrade.'
    )

from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from warnings import warn

from flet_easy.auto_route import automatic_routing
from flet_easy.datasy import Datasy
from flet_easy.extrasJwt import SecretKey
from flet_easy.inheritance import Viewsy
from flet_easy.logger import LoggingFletEasy, get_logger
from flet_easy.middleware import MiddlewareHandler, MiddlewareRequest
from flet_easy.pagesy import AddPagesy, Pagesy
from flet_easy.route import FletEasyX


class FletEasy(FletEasyX):
    """
    we create the app object, in it you can configure:

    * `route_prefix` : The route that is different from ` /`.
    * `route_init` : The initial route to initialize the app, by default is `/`.
    * `route_login` : The route that will be redirected when the app has route protectionconfigured.
    * `on_Keyboard` : Enables the on_Keyboard event, by default it is disabled (False).
    * `on_resize` : Triggers the on_resize event, by default it is disabled (False).
    * `secret_key` : Used with `SecretKey` class of Flet easy, to configure JWT or client storage.
    * `auto_logout` : If you use JWT, you can configure it.
    * `path_views` : Configuration of the folder where are the .py files of the pages, you use the `Path` class to configure it.
    * `logger` : Activates the logger, by default it is disabled (False).

    Example:
    ```python
    import flet as ft
    import flet_easy as fs

    app = fs.FletEasy(
        route_prefix="/FletEasy",
        route_init="/FletEasy/home",
    )


    @app.view
    async def view(data: fs.Datasy):
        return fs.Viewsy(
            appbar=ft.AppBar(
                title=ft.Text("AppBar Example"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="🔥 Home", on_click=data.go(data.route_init)
                            ),
                        ]
                    )
                ],
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


    @app.page("/home", title="Index - Home", page_clear=True)
    async def index_page(data: fs.Datasy):
        view = data.view
        view.appbar.title = ft.Text("Index - Home")
        return ft.View(
            data.route_init,
            controls=[
                ft.Text("Menú", size=40),
                ft.ElevatedButton(
                    "Go to Test",
                    on_click=data.go(f"{data.route_prefix}/test/10/user/dxs"),
                ),
            ],
            appbar=view.appbar,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


    @app.page("/test/{id:d}/user/{name:l}", title="Test")
    def test_page(data: fs.Datasy, id: int, name: str):
        view = data.view
        view.appbar.title = ft.Text("test")
        return ft.View(
            "/index/test",
            controls=[
                ft.Text(f"Test {id} | {name}"),
                ft.Text(f"Test Id is: {id}"),
                ft.ElevatedButton("Go to Home", on_click=data.go(data.route_init)),
            ],
            appbar=view.appbar,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


    # Execute the app (synchronous / asynchronous)
    app.run()
    ```
    """

    __self = None

    def __init__(
        self,
        route_prefix: str = None,
        route_init: str = "/",
        route_login: str = None,
        on_resize: bool = False,
        on_Keyboard: bool = False,
        secret_key: SecretKey = None,
        auto_logout: bool = False,
        path_views: Path = None,
        logger: bool = False,
    ):
        if logger:
            LoggingFletEasy.enable(logging.DEBUG)
        self.logger = get_logger("FletEasy")

        self.__route_prefix = route_prefix
        self.__path_views = path_views
        FletEasy.__self = self

        super().__init__(
            route_prefix=self.__route_prefix,
            route_init=route_init,
            route_login=route_login,
            on_resize=on_resize,
            on_Keyboard=on_Keyboard,
            secret_key=secret_key,
            auto_logout=auto_logout,
        )

        # add data to middleware request
        MiddlewareRequest._data = self._data

        self.__pagesys = automatic_routing(self.__path_views) if self.__path_views else None

    # -------------------------------------------------------------------
    def __pre_config(self, page: Page):
        """config before run"""
        self._add_configuration_start(page)

        if self.__pagesys:
            self.add_pages(self.__pagesys)

        self._run()

    def start(self, page: Page):
        """Start the app in the main function"""
        self.logger.debug("enabling connection with flet app")
        self.__pre_config(page)

    def get_app(self):
        """Return the app function main"""

        def main(page: Page):
            self.__pre_config(page)

        self.logger.debug("getting app from fletEasy to export")
        return main

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
        """* Execute the app. | Soporta async, fastapi y export_asgi_app."""

        def main(page: Page):
            self.__pre_config(page)

        if fastapi:
            warn(
                "Avoid using the 'fastapi' parameter in the 'run()' method, instead it is better to use the 'get_app()' method.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return main
        try:
            self.logger.debug("running app from fletEasy with flet")
            return app(
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
            raise FletEasyError(
                "Ifs you are using fastapi from flet, set the 'fastapi = True' parameter of the run() method."
            )

    # -- decorators --------------------------------

    def __decorator(self, value: str, data: Dict[str, Any] = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(data, *args, **kwargs):
                return func(data, *args, **kwargs)

            route = data.get("route")

            route = (
                (self.__route_prefix if route == "/" else self.__route_prefix + route)
                if self.__route_prefix and route
                else route
            )

            if value == "page_404":
                self._page_404 = Pagesy(route, func, data.get("title"), data.get("page_clear"))
                self.logger.debug(f"Adding page 404: {self._page_404}")

            elif value == "page":
                self._pages.append(
                    Pagesy(
                        route=route,
                        view=func,
                        title=data.get("title"),
                        index=data.get("index"),
                        clear=data.get("page_clear"),
                        share_data=data.get("share_data"),
                        protected_route=data.get("protected_route"),
                        custom_params=data.get("custom_params"),
                        middleware=data.get("middleware"),
                        cache=data.get("cache"),
                    )
                )
                self.logger.debug(f"Adding page: {self._pages[-1]}")

            return wrapper

        return decorator

    def add_pages(self, group_pages: List[AddPagesy]):
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
                    self._pages.extend(page._add_pages(self.__route_prefix))
                else:
                    self._pages.extend(page._add_pages())

                self.logger.debug(f"Adding group of pages: {len(group_pages)}: {page}\n")
        except Exception as e:
            raise AddPagesError("Add pages error in route: ", e)

    @classmethod
    def page(
        cls,
        route: str,
        title: str = None,
        index: Optional[int] = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Dict[str, Any] = None,
        middleware: Optional[
            Union[List[Union[MiddlewareHandler, MiddlewareRequest]], MiddlewareHandler, MiddlewareRequest]
        ] = None,
        cache: bool = False,
    ) -> Callable:
        """Decorator to add a new page to the app, you need the following parameters:
        * route: text string of the url, for example(`'/FletEasy'`).
        * `title` : Define the title of the page. (optional).
        * `index` : Define the index of the page, use in controls like `ft.CupertinoNavigationBar` or `ft.NavigationBar`. (optional)
        * clear: Removes the pages from the `page.views` list of flet. (optional)
        * `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way. (optional)
        * protected_route: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
        * custom_params: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.
        * `middleware` : It acts as an intermediary between different software components, intercepting and processing requests and responses. They allow adding functionalities to an application in a flexible and modular way. (optional)
        * `cache`: Boolean that preserves page state when navigating. Controls retain their values instead of resetting. (Optional)

        -> The decorated function must receive a parameter, for example `data:fs.Datasy`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy(
            route_prefix="/FletEasy",
            route_init="/FletEasy",
        )


        @app.page("/", title="FletEasy")
        async def index_page(data: fs.Datasy):
            return ft.View(
                route="/FletEasy",
                controls=[ft.Text("FletEasy")],
                vertical_alignment=view.vertical_alignment,
                horizontal_alignment=view.horizontal_alignment,
            )
        ```
        """

        data = {
            "route": route,
            "title": title,
            "index": index,
            "page_clear": page_clear,
            "share_data": share_data,
            "protected_route": protected_route,
            "custom_params": custom_params,
            "middleware": middleware,
            "cache": cache,
        }
        return cls.__decorator(cls.__self, "page", data)

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
            route_prefix="/FletEasy",
            route_init="/FletEasy",
        )


        @app.page_404("/FletEasy-404", title="Error 404", page_clear=True)
        async def page404(data: fs.Datasy):
            return ft.View(
                route="/error404",
                controls=[
                    ft.Text(f"Error 404", size=30),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ```
        """
        data = {
            "route": route,
            "title": "Flet-Easy 404" if title is None else title,
            "page_clear": page_clear,
        }
        return self.__decorator("page_404", data)

    def view(self, func: Callable[[Datasy], Viewsy]):
        """
        Decorator to add custom controls to the application, the decorator function will return the `Viewsy` class of `FletEasy`. Which will be obtained in functions with `data:fs.Datasy` parameter and can be added to the page view decorated with `data.view` of `FletEasy` class.

        * The decorator function must receive a mandatory parameter, for example: `data:ft.Datasy`.
        * Add universal controls to use on more than one page in an easy way.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        app = fs.FletEasy(
            route_prefix="/FletEasy",
            route_init="/FletEasy",
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
                await page.go_async("/FletEasy")

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
                            ]
                        ),
                    ],
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ```
        """
        self._view_data = func
        self.logger.debug(f"Adding view: {self._view_data}")

    def config(self, func: Callable[[Datasy], None]):
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
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)

            theme.text_theme = ft.TextTheme()
            page.theme = theme
        ```
        """
        self._view_config = func
        self.logger.debug(f"Adding config: {self._view_config}")

    def login(self, func: Callable[[Datasy], bool]):
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
        self._config_login = func
        self.logger.debug(f"Adding login: {self._config_login}")

    def config_event_handler(self, func: Callable[[Datasy], None]):
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

        self._config_event = func
        self.logger.debug(f"Adding config event: {self._config_event}")

    def add_routes(self, add_views: List[Pagesy]):
        """-> Add routes without the use of decorators.

        Example:
        ```python
        app.add_routes(
            add_views=[
                fs.Pagesy("/hi", index_page, True),
                fs.Pagesy(
                    "/test/{id:d}/user/{name:l}", test_page, protected_route=True
                ),
                fs.Pagesy("/counter", counter_page),
                fs.Pagesy("/task", task_page),
                fs.Pagesy("/login/user", login_page),
            ]
        )
        ```
        """

        assert len(add_views) != 0, "add view (add_view) in 'add_routes'."
        for page in add_views:
            if self.__route_prefix:
                page.route = self.__route_prefix + page.route

            self._pages.append(page)
            self.logger.debug(f"Add routes: {page}")

    def add_middleware(
        self,
        *middleware: Optional[
            Union[Tuple[Union[MiddlewareHandler, MiddlewareRequest]], MiddlewareHandler, MiddlewareRequest]
        ],
    ):
        """
        You can add a list of elements as classes inherited from `fs.MiddlewareRequest` or functions that receive `data:fs.Datasy` as a parameter. Or you can add them individually.

        **More info:** https://daxexs.github.io/flet-easy/latest/middleware/#general-application
        """
        try:
            middleware = middleware[0] if isinstance(middleware[0], list) else middleware
            self._middlewares_after = []
            self._middlewares = []

            for m in middleware:
                if isinstance(m, type):
                    if issubclass(m, MiddlewareRequest):
                        middleware_instance = m()
                        self._middlewares.append(middleware_instance)
                        self._middlewares_after.append(middleware_instance)
                    else:
                        raise TypeError(
                            f"Class '{m.__name__}' must inherit from MiddlewareRequest class",
                        )
                else:
                    self._middlewares.append(m)

            self.logger.debug(f"Add middlewares in method 'add_middleware': {middleware}")
        except Exception as e:
            raise MidlewareError(
                "You are not adding any midleware but you are using the 'add_middleware' method:",
                e,
            )

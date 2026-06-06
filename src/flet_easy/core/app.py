from collections import deque
from pathlib import Path
from typing import Any, Callable, Optional, Union, cast
from warnings import warn

from flet_easy.exceptions import (
    AddPagesError,
    ConfigurationError,
    FletEasyError,
    MiddlewareError,
)
from flet_easy.utils import normalize_route

try:
    from flet import AppView, Page, WebRenderer
except ImportError:
    raise FletEasyError(
        'Install "flet" the latest version available -> pip install flet[all] --upgrade.'
    )

try:
    from flet import RouteUrlStrategy
except ImportError:
    from enum import Enum

    class RouteUrlStrategy(str, Enum):
        PATH = "path"
        HASH = "hash"


try:
    # support for flet < 0.80.0 deprecated in flet 0.80.0
    from flet import run as app
except ImportError:
    from flet import app

from flet_easy.core.auto_route import automatic_routing
from flet_easy.core.data import Datasy
from flet_easy.core.middleware import (
    Middleware,
    MiddlewareItem,
    MiddlewareRequest,
)
from flet_easy.core.pages import AddPagesy, Pagesy
from flet_easy.core.router import FletEasyX
from flet_easy.logger import LoggingFletEasy, get_logger
from flet_easy.security.config import SecretKey
from flet_easy.ui.controls import Viewsy


class FletEasy:
    """Main application class for Flet-Easy.

    Configure the app with:

    * `route_prefix` : Route prefix different from `/`.
    * `route_init` : Initial route, default is `/`.
    * `route_login` : Route for redirect when using protected routes.
    * `on_keyboard` : Enable on_keyboard event (default: False).
    * `on_resize` : Enable on_resize event (default: False).
    * `secret_key` : Configure JWT or client storage with `SecretKey`.
    * `auto_logout` : Auto-logout with JWT expiry (default: False).
    * `path_views` : Folder path for auto-discovered page files.
    * `logger` : Enable logger (default: False).

    Example:
    ```python
    import flet as ft
    import flet_easy as fs

    app = fs.FletEasy(
        route_prefix="/FletEasy",
        route_init="/FletEasy/home",
    )


    @app.page("/home", title="Home", page_clear=True)
    async def index_page(data: fs.Datasy):
        return ft.View(
            data.route_init,
            controls=[ft.Text("Home", size=40)],
        )


    app.run()
    ```
    """

    __self: Optional["FletEasy"] = None

    # ─── Initialization ───────────────────────────────────────────────

    def __init__(
        self,
        route_prefix: Optional[str] = None,
        route_init: str = "/",
        route_login: Optional[str] = None,
        on_resize: bool = False,
        on_keyboard: bool = False,
        secret_key: Optional[SecretKey] = None,
        auto_logout: bool = False,
        path_views: Optional[Path] = None,
        logger: bool = False,
        use_error_boundary: bool = True,
    ) -> None:
        if logger:
            import logging

            LoggingFletEasy.enable(logging.DEBUG)
        self._logger = get_logger("FletEasy")

        self.__route_prefix: str = route_prefix or ""
        self.__route_init: str = route_init
        self.__route_login: Optional[str] = route_login
        self.__path_views: Optional[Union[str, Path]] = path_views
        self.__on_resize: bool = on_resize
        self.__on_keyboard: bool = on_keyboard
        self.__secret_key: Optional[SecretKey] = secret_key
        self.__auto_logout: bool = auto_logout
        self.__use_error_boundary: bool = use_error_boundary

        self.__page_404: Optional[Pagesy] = None
        self.__middlewares: Optional[deque[MiddlewareItem]] = None
        self.__middlewares_after: Optional[deque[MiddlewareItem]] = None

        self.__pages: deque[Pagesy] = deque()
        self.__view_data: Optional[Callable[[Datasy], Viewsy]] = None
        self.__config_login: Optional[Callable[[Datasy], bool]] = None
        self.__view_config: Optional[Callable[[Page], None]] = None
        self.__config_event: Optional[Callable[[Datasy], None]] = None

        FletEasy.__self = self
        self.__fsx: Optional[FletEasyX] = None
        self.__pagesys = automatic_routing(str(self.__path_views)) if self.__path_views else None

    # ─── App Lifecycle ────────────────────────────────────────────────

    def __pre_config(self, page: Page) -> None:
        """Configure and start the routing engine."""

        # Add automatic routing pages before initializing FletEasyX
        # so they are included in the exact_routes_map
        if self.__pagesys:
            self.add_pages(self.__pagesys)
            self.__pagesys = None

        fsx = FletEasyX(
            page=page,
            route_prefix=self.__route_prefix,
            route_init=self.__route_init,
            route_login=self.__route_login,
            page_404=self.__page_404,
            pages=self.__pages,
            view_data=self.__view_data,
            config_login=self.__config_login,
            view_config=self.__view_config,
            config_event=self.__config_event,
            middlewares=self.__middlewares,
            middlewares_after=self.__middlewares_after,
            on_resize=self.__on_resize,
            on_keyboard=self.__on_keyboard,
            secret_key=self.__secret_key,
            auto_logout=self.__auto_logout,
            use_error_boundary=self.__use_error_boundary,
        )

        self.__fsx = fsx

        fsx.run()

    def start(self, page: Page) -> None:
        """Start the app in the main function."""
        self._logger.debug("enabling connection with flet app")
        self.__pre_config(page)

    def get_app(self) -> Callable[[Page], None]:
        """Return the app function main."""
        self._logger.debug("getting app from fletEasy to export")

        def main(page: Page) -> None:
            self.__pre_config(page)

        return main

    def run(
        self,
        name: str = "",
        host: Optional[str] = None,
        port: int = 0,
        view: Optional[AppView] = AppView.FLET_APP,
        assets_dir: str = "assets",
        upload_dir: Optional[str] = None,
        web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
        route_url_strategy: Union[RouteUrlStrategy, str] = RouteUrlStrategy.PATH,
        export_asgi_app: bool = False,
        fastapi: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Execute the app. Supports async, fastapi, and export_asgi_app."""
        main = self.get_app()

        if fastapi:
            warn(
                "Avoid using the 'fastapi' parameter in the 'run()' method, "
                "instead use the 'get_app()' method.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return main

        try:
            self._logger.debug("running app from fletEasy with flet")
            app_kwargs: dict[str, Any] = {
                "name": name,
                "host": host,
                "port": port,
                "view": view,
                "assets_dir": assets_dir,
                "upload_dir": upload_dir,
                "web_renderer": web_renderer,
                "export_asgi_app": export_asgi_app,
                **kwargs,
            }
            if route_url_strategy is not None:
                app_kwargs["route_url_strategy"] = route_url_strategy

            return app(
                main,
                **app_kwargs,
            )
        except RuntimeError:
            raise FletEasyError(
                "If you are using fastapi from flet, set the 'fastapi = True' "
                "parameter of the run() method."
            )

    # ─── Route Registration ───────────────────────────────────────────

    @classmethod
    def page(
        cls,
        route: str,
        title: Optional[str] = None,
        index: Optional[int] = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Optional[dict[str, Any]] = None,
        middleware: Middleware = None,
        cache: bool = False,
    ) -> Callable:
        """Decorator to add a new page to the app.

        Args:
            route: URL path, e.g. `'/home'`.
            title: Page title (optional).
            index: Page index for NavigationBar (optional).
            page_clear: Remove previous views (optional).
            share_data: Share data between pages (optional).
            protected_route: Protect with login (optional).
            custom_params: Custom URL parameter validators (optional).
            middleware: Page-level middleware (optional).
            cache: Preserve page state when navigating (optional).
        """
        self = cls.__self
        if self is None:
            raise ConfigurationError("FletEasy instance not initialized.")

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            pagesy = Pagesy(
                route=normalize_route(self.__route_prefix, route),
                view=func,
                title=title,
                index=index,
                clear=page_clear,
                share_data=share_data,
                protected_route=protected_route,
                custom_params=custom_params,
                middleware=middleware,
                cache=cache,
            )
            self.__pages.append(pagesy)

            # Back-reference for reverse decorator order (@ft.component on top)
            setattr(func, "__flet_easy_pagesy__", pagesy)  # noqa: B010

            self._logger.debug("Adding page: %s", self.__pages[-1])
            return func

        return decorator

    def page_404(
        self,
        route: Optional[str] = None,
        title: Optional[str] = None,
        page_clear: bool = False,
    ) -> Callable:
        """Decorator to add a custom 404 page.

        Args:
            route: URL path for the 404 page (optional).
            title: Page title (default: 'Flet-Easy 404').
            page_clear: Remove previous views (optional).
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.__page_404 = Pagesy(
                normalize_route(self.__route_prefix, route or ""),
                func,
                title or "Flet-Easy 404",
                clear=page_clear,
            )
            self._logger.debug("Adding page 404: %s", self.__page_404)
            return func

        return decorator

    def add_pages(self, group_pages: Union[list[AddPagesy], AddPagesy]) -> None:
        """Add pages from other files.

        Example:
        ```python
        app.add_pages([index, test, contador, login, task])
        ```
        """
        group_pages = group_pages if isinstance(group_pages, list) else [group_pages]

        try:
            for page in group_pages:
                if self.__route_prefix:
                    self.__pages.extend(page._add_pages(self.__route_prefix))
                else:
                    self.__pages.extend(page._add_pages())

                self._logger.debug("Adding group of pages: %d: %s", len(group_pages), page)
        except Exception as e:
            raise AddPagesError("Add pages error in route: ", e)

    def add_routes(self, add_views: list[Pagesy]) -> None:
        """Add routes without the use of decorators.

        Example:
        ```python
        app.add_routes(
            add_views=[
                fs.Pagesy("/hi", index_page, True),
                fs.Pagesy("/counter", counter_page),
            ]
        )
        ```
        """
        if not add_views:
            raise ConfigurationError("add view (add_view) in 'add_routes'.")

        for page in add_views:
            if self.__route_prefix:
                page.route = normalize_route(self.__route_prefix, page.route)

            self.__pages.append(page)
            self._logger.debug("Add routes: %s", page)

    # ─── Configuration Decorators ─────────────────────────────────────

    def view(self, func: Callable[[Datasy], Viewsy]) -> Callable[[Datasy], Viewsy]:
        """Decorator to add custom view controls (appbar, navigation, etc).

        The decorated function receives `data:fs.Datasy` and returns `fs.Viewsy`.
        """
        self.__view_data = func
        self._logger.debug("Adding view: %s", self.__view_data)
        return func

    def config(self, func: Callable[[Page], None]) -> Callable[[Page], None]:
        """Decorator to add custom page configuration (theme, etc).

        The decorated function receives `page:ft.Page` and returns nothing.
        """
        self.__view_config = func
        self._logger.debug("Adding config: %s", self.__view_config)
        return func

    def login(self, func: Callable[[Datasy], bool]) -> Callable[[Datasy], bool]:
        """Decorator to add login configuration for protected routes.

        The decorated function receives `data:fs.Datasy` and must return a boolean.
        """
        self.__config_login = func
        self._logger.debug("Adding login: %s", self.__config_login)
        return func

    def config_event_handler(self, func: Callable[[Datasy], None]) -> Callable[[Datasy], None]:
        """Decorator to add page event handler settings."""
        self.__config_event = func
        self._logger.debug("Adding config event: %s", self.__config_event)
        return func

    # ─── Middleware ────────────────────────────────────────────────────

    def add_middleware(
        self,
        *middleware: MiddlewareItem,
    ) -> None:
        """Add global middleware.

        Accepts classes inheriting from `fs.MiddlewareRequest` or functions
        that receive `data:fs.Datasy`. Can be added individually or as a list.

        **More info:** https://daxexs.github.io/flet-easy/latest/middleware/#general-application
        """
        if not middleware:
            raise MiddlewareError(
                "No middleware provided to 'add_middleware'. "
                "Pass at least one middleware function or MiddlewareRequest class."
            )

        items = middleware[0] if isinstance(middleware[0], list) else list(middleware)

        self.__middlewares = deque()
        self.__middlewares_after = deque()

        for m in items:
            if isinstance(m, type) and issubclass(m, MiddlewareRequest):
                self.__middlewares.append(m)
                self.__middlewares_after.append(m)
            elif callable(m):
                self.__middlewares.append(cast(MiddlewareItem, m))
            else:
                raise MiddlewareError(
                    f"Middleware '{m}' must be a class inheriting from "
                    f"MiddlewareRequest or a callable function."
                )

        self._logger.debug("Add middlewares in method 'add_middleware': %s", items)

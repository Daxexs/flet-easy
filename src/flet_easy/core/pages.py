from collections import deque
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Union

from flet_easy.core.middleware import (
    Middleware,
    MiddlewareHandler,
    MiddlewareRequest,
    ViewHandler,
)


class Pagesy:
    """To add pages, it requires the following parameters:
    * `route`: text string of the url, for example(`'/task'`).
    * `view`: Stores the page function.
    * `title` : Define the title of the page.
    * `index` : Define the index of the page, use in controls like `ft.NavigationBar` and `ft.CupertinoNavigationBar`.
    * `clear`: Removes the pages from the `page.views` list of flet. (optional)
    * `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way. (optional)
    * `protected_route`: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
    * `custom_params`: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.
    * `middleware` : It acts as an intermediary between different software components, intercepting and processing requests and responses. They allow adding functionalities to an application in a flexible and modular way. (optional)
    * `cache`: Boolean that preserves page state when navigating. Controls retain their values instead of resetting. (Optional)

    Example:
    ```python
    Pagesy("/test/{id:d}/user/{name:l}", test_page, protected_route=True)
    ```
    """

    __slots__ = (
        "route",
        "view",
        "title",
        "index",
        "clear",
        "share_data",
        "protected_route",
        "custom_params",
        "middleware",
        "cache",
        "_is_component",
        "_middlewares_request",
    )

    def __init__(
        self,
        route: str,
        view: ViewHandler,
        title: Optional[str] = None,
        index: Optional[int] = None,
        clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Optional[Dict[str, Callable[[], bool]]] = None,
        middleware: Optional[
            Union[
                List[Union[MiddlewareHandler, MiddlewareRequest]],
                MiddlewareHandler,
                MiddlewareRequest,
            ]
        ] = None,
        cache: bool = False,
    ):
        self.route = route
        self.view = view
        self.title = title
        self.index = index
        self.clear = clear
        self.share_data = share_data
        self.protected_route = protected_route
        self.custom_params = custom_params
        self.middleware = middleware
        self.cache: bool = cache
        self._is_component: bool = getattr(view, "__is_component__", False)
        self._middlewares_request: deque[MiddlewareRequest] = deque()

    def _valid_middlewares_request(self) -> bool:
        return bool(self._middlewares_request)

    def _process_middleware(self, middleware: Union[MiddlewareRequest, MiddlewareHandler]) -> None:
        """Process and validate middleware handlers."""

        if isinstance(middleware, FunctionType):
            self.middleware.append(middleware)
        elif isinstance(middleware, MiddlewareRequest) or (
            isinstance(middleware, type) and issubclass(middleware, MiddlewareRequest)
        ):
            self._middlewares_request.append(middleware)
            self.middleware.append(middleware)
        else:
            raise TypeError(
                f"Class '{getattr(middleware, '__name__', type(middleware).__name__)}' must inherit from MiddlewareRequest class or be a function",
            )

    def _check_middleware(self, middleware: Middleware) -> None:
        if middleware is None and self.middleware is None:
            return

        # Collect page-level items first, then global ones
        page_items = []
        if self.middleware is not None:
            if isinstance(self.middleware, (list, tuple, set, deque)):
                page_items.extend(self.middleware)
            else:
                page_items.append(self.middleware)

        global_items = []
        if middleware is not None:
            if isinstance(middleware, (list, tuple, set, deque)):
                global_items.extend(middleware)
            else:
                global_items.append(middleware)

        self.middleware = deque()
        self._middlewares_request = deque()

        for m in page_items + global_items:
            try:
                self._process_middleware(m)
            except (TypeError, AssertionError) as e:
                from flet_easy.exceptions import ConfigurationError

                raise ConfigurationError(f"Invalid middleware configuration: {str(e)}")

    def __repr__(self):
        return f"Pagesy(route={self.route}, view={self.view}, title={self.title}, index={self.index}, clear={self.clear}, share_data={self.share_data}, protected_route={self.protected_route}, custom_params={self.custom_params}, middleware={self.middleware}, cache={self.cache})"


class AddPagesy:
    """This class allows you to add pages from other files to the main `Flet-Easy` class.

    Requiere los parámetros:
    - **route_prefix:** cadena de texto que se unira a la url del decorator `page`, ejemplo(`/users`) esto englobara todas las urls de esta clase. (opcional)
    - **middleware:** lista de middlewares que se agregaran a la página. (opcional)

    **Ejemplo:**
    ```python
    users = fs.AddPagesy(route_prefix="/user")


    @users.page("/task")
    async def task_page(data: fs.Datasy):
        page = data.page
        page.title = "Task"
        return ft.View(
            route="/users/task",
            controls=[ft.Text("Task")],
        )
    ```
    """

    __slots__ = ("route_prefix", "middleware", "__pages")

    def __init__(
        self,
        route_prefix: Optional[str] = None,
        middleware: Optional[
            Union[
                List[Union[MiddlewareHandler, MiddlewareRequest]],
                MiddlewareHandler,
                MiddlewareRequest,
            ]
        ] = None,
    ):
        self.route_prefix = route_prefix.rstrip("/") if route_prefix else None
        self.middleware = middleware
        self.__pages: deque[Pagesy] = deque()

    def __build_route(self, route: str) -> str:
        """Build complete route with prefix."""
        if not self.route_prefix:
            return route
        if route == "/":
            return self.route_prefix
        return self.route_prefix + route

    def page(
        self,
        route: str,
        title: Optional[str] = None,
        index: Optional[int] = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Optional[Dict[str, Any]] = None,
        middleware: Optional[
            Union[
                List[Union[MiddlewareHandler, MiddlewareRequest]],
                MiddlewareHandler,
                MiddlewareRequest,
            ]
        ] = None,
        cache: bool = False,
    ) -> Callable:
        """Decorator for adding pages with configuration."""

        def decorator(func: Callable) -> Callable:
            pagesy = Pagesy(
                route=self.__build_route(route),
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
            func.__flet_easy_pagesy__ = pagesy

            return func

        return decorator

    def _add_pages(self, route: Optional[str] = None) -> deque[Pagesy]:
        """Add pages with optional route prefix override."""

        for page in self.__pages:
            page._check_middleware(self.middleware)

            if route:
                page.route = route if page.route == "/" else route + page.route

        return self.__pages

    def __repr__(self) -> str:
        return f"AddPagesy(route_prefix={self.route_prefix}, middleware={self.middleware}, number_pages={len(self.__pages)}, pages={self.__pages})"

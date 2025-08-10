from collections import deque
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from flet_easy.middleware import (
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
            List[MiddlewareHandler | MiddlewareRequest] | MiddlewareHandler | MiddlewareRequest
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
        self._middlewares_request: deque[MiddlewareRequest] = deque()

    def _valid_middlewares_request(self) -> bool:
        if len(self._middlewares_request) != 0:
            return True

    def _process_middleware(self, middleware: Union[MiddlewareRequest, MiddlewareHandler]) -> None:
        """Process and validate middleware handlers."""

        if isinstance(middleware, type):
            if issubclass(middleware, MiddlewareRequest):
                middleware_instance = middleware()

                self._middlewares_request.append(middleware_instance)
                self.middleware.append(middleware_instance)
            else:
                raise TypeError(
                    f"Class '{middleware.__name__}' must inherit from MiddlewareRequest class",
                )
        else:
            self.middleware.append(middleware)

    def _check_middleware(self, middleware: Middleware) -> None:
        if middleware is None and self.middleware is None:
            return

        if middleware:
            _middleware = deque()

            if self.middleware is not None:
                if isinstance(self.middleware, list):
                    _middleware.extend(self.middleware)
                    self.middleware.clear()
                else:
                    _middleware.append(self.middleware)
                    self.middleware = deque()

            else:
                self.middleware = deque()

            _middleware.extend(middleware if isinstance(middleware, list) else [middleware])

            for m in _middleware:
                try:
                    self._process_middleware(m)

                except (TypeError, AssertionError) as e:
                    raise ValueError(f"Invalid middleware configuration: {str(e)}")
        else:
            if not isinstance(self.middleware, list):
                self.middleware = [self.middleware]

    def __repr__(self):
        return f"Pagesy(route={self.route}, view={self.view}, title={self.title}, index={self.index}, clear={self.clear}, share_data={self.share_data}, protected_route={self.protected_route}, custom_params={self.custom_params}, middleware={self.middleware}, cache={self.cache})"


class AddPagesy:
    """
    Creates an object to then add to the list of the `add_routes` method of the `FletEasy` class.
    -> Requires the parameter:
    - **route_prefix:** text string that will bind to the url of the `page` decorator, example(`/users`) this will encompass all urls of this class. (optional)
    - **middleware:** list of middlewares to be added to the page. (optional)

    **Example:**

    ```python
    users = fs.AddPagesy(route_prefix="/user")

    # -> Urls to be created:
    # * '/user/task'
    # * '/user/information'


    @users.page("/task")
    async def task_page(data: fs.Datasy):
        page = data.page

        page.title = "Task"

        return ft.View(
            route="/users/task",
            controls=[
                ft.Text("Task"),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment,
        )


    @users.page("/information")
    async def information_page(data: fs.Datasy):
        page = data.page

        page.title = "Information"

        return ft.View(
            route="/users/information",
            controls=[
                ft.Text("Information"),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment,
        )
    ```

    """

    def __init__(
        self,
        route_prefix: Optional[str] = None,
        middleware: Optional[
            List[MiddlewareHandler | MiddlewareRequest] | MiddlewareHandler | MiddlewareRequest
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
            List[MiddlewareHandler | MiddlewareRequest] | MiddlewareHandler | MiddlewareRequest
        ] = None,
        cache: bool = False,
    ) -> Callable:
        """Decorator for adding pages with configuration."""

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            self.__pages.append(
                Pagesy(
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
            )
            return wrapper

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

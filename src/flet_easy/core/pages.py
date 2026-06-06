from collections import deque
from collections.abc import Iterable
from inspect import signature
from itertools import chain
from typing import Any, Callable, Optional, cast

from flet_easy.core.middleware import (
    Middleware,
    MiddlewareItem,
    MiddlewareRequest,
    ViewHandler,
)
from flet_easy.exceptions import ConfigurationError
from flet_easy.utils import normalize_route


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
        # Cached signature flags — computed once on first render, reused every navigation
        "_view_has_params",
        "_build_has_params",
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
        custom_params: Optional[dict[str, Callable[..., bool]]] = None,
        middleware: Middleware = None,
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
        self.middleware: Middleware = middleware
        self.cache: bool = cache
        self._is_component: bool = getattr(view, "__is_component__", False) or (
            isinstance(view, type)
            and getattr(getattr(view, "build", None), "__is_component__", False)
        )
        self._middlewares_request: deque[MiddlewareRequest] = deque()
        # None = not yet computed, True/False = cached result
        self._view_has_params: Optional[bool] = None
        self._build_has_params: Optional[bool] = None

    def _get_view_has_params(self) -> bool:
        """Cached check: does the view function/class __init__ accept parameters?"""
        if self._view_has_params is None:
            try:
                self._view_has_params = bool(signature(self.view).parameters)
            except (ValueError, TypeError):
                self._view_has_params = False
        return self._view_has_params

    def _get_build_has_params(self, build_fn: Any) -> bool:
        """Cached check: does the build() method accept parameters beyond self?

        Caching per Pagesy is safe because all instances of the same class share the
        same build() signature (we only check declared params, not self/instance state).
        """
        if self._build_has_params is None:
            try:
                self._build_has_params = bool(signature(build_fn).parameters)
            except (ValueError, TypeError):
                self._build_has_params = False
        return self._build_has_params

    def _valid_middlewares_request(self) -> bool:
        return bool(self._middlewares_request)

    def _process_middleware(self, item: MiddlewareItem) -> None:
        """Process and validate middleware handlers."""

        if not isinstance(self.middleware, deque):
            if self.middleware is None:
                self.middleware = deque[MiddlewareItem]()
            elif isinstance(self.middleware, (list, tuple, set)):
                self.middleware = deque[MiddlewareItem](
                    cast(Iterable[MiddlewareItem], self.middleware)
                )
            else:
                self.middleware = deque[MiddlewareItem]([self.middleware])

        middleware_deque = cast(deque[MiddlewareItem], self.middleware)

        if isinstance(item, MiddlewareRequest) or (
            isinstance(item, type) and issubclass(item, MiddlewareRequest)
        ):
            # Store as-is (class or instance) — instantiation happens lazily in the router
            # because MiddlewareRequest._data is only set after FletEasyX.__init__
            self._middlewares_request.append(cast(MiddlewareRequest, item))
            middleware_deque.append(item)
        elif callable(item):
            middleware_deque.append(item)
        else:
            raise TypeError(
                f"Class '{getattr(item, '__name__', type(item).__name__)}' must inherit from MiddlewareRequest class or be a function",
            )

    def _check_middleware(self, middleware: Middleware) -> None:
        if middleware is None and self.middleware is None:
            return

        # Capture original page-level middleware before resetting
        original_page_middleware = self.middleware

        def _to_iter(m: Middleware) -> Iterable[MiddlewareItem]:
            if m is None:
                return ()
            if isinstance(m, (list, tuple, set, deque)):
                return cast(Iterable[MiddlewareItem], m)
            return (m,)

        # Reset so _process_middleware starts fresh
        self.middleware = deque[MiddlewareItem]()
        self._middlewares_request = deque()

        # Chain original page middleware first, then group-level middleware
        for m in chain(_to_iter(original_page_middleware), _to_iter(middleware)):
            try:
                self._process_middleware(m)
            except (TypeError, AssertionError) as e:
                raise ConfigurationError(f"Invalid middleware configuration: {str(e)}")

    def __repr__(self) -> str:
        return f"Pagesy(route={self.route}, view={self.view}, title={self.title}, index={self.index}, clear={self.clear}, share_data={self.share_data}, protected_route={self.protected_route}, custom_params={self.custom_params}, middleware={self.middleware}, cache={self.cache})"


class AddPagesy:
    """This class allows you to add pages from other files to the main `Flet-Easy` class.

    Requires the following parameters:
    - **route_prefix:** A text string that will be joined to the URL of the `page` decorator, for example (`'/users'`). This will encompass all URLs in this class. (Optional)
    - **middleware:** A list of middlewares to be added to the page. (Optional)

    **Example:**
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

    __slots__ = ("route_prefix", "middleware", "__pages", "_finalized")

    def __init__(
        self,
        route_prefix: Optional[str] = None,
        middleware: Middleware = None,
    ):
        self.route_prefix = route_prefix.rstrip("/") if route_prefix else None
        self.middleware = middleware
        self.__pages: deque[Pagesy] = deque()
        self._finalized: bool = False

    def page(
        self,
        route: str,
        title: Optional[str] = None,
        index: Optional[int] = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Optional[dict[str, Any]] = None,
        middleware: Middleware = None,
        cache: bool = False,
    ) -> Callable[..., Any]:
        """Decorator for adding pages with configuration."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            pagesy = Pagesy(
                route=normalize_route(self.route_prefix, route),
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

            return func

        return decorator

    def _add_pages(self, route: Optional[str] = None) -> deque[Pagesy]:
        """Add pages with optional route prefix override.

        Idempotent: safe to call multiple times — subsequent calls are no-ops
        to prevent route prefixes from being compounded.
        """
        if self._finalized:
            return self.__pages

        for page in self.__pages:
            page._check_middleware(self.middleware)

            if route:
                page.route = normalize_route(route, page.route)

        self._finalized = True
        return self.__pages

    def __repr__(self) -> str:
        return f"AddPagesy(route_prefix={self.route_prefix}, middleware={self.middleware}, number_pages={len(self.__pages)}, pages={self.__pages})"

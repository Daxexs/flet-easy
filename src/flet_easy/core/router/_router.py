"""FletEasyX — main router class, assembled from mixins.

Contains only __slots__, __init__, and run().
All logic lives in specialized mixins.
"""

import asyncio
from collections import deque
from typing import Any, Callable, Optional, Union, cast

from flet import Page, View

from flet_easy.core.context import current_data
from flet_easy.core.data import Datasy
from flet_easy.core.middleware import MiddlewareItem, MiddlewareRequest
from flet_easy.core.models import RouteState
from flet_easy.core.pages import Pagesy
from flet_easy.logger import LoggingFletEasy, get_logger
from flet_easy.security.config import SecretKey
from flet_easy.ui.controls import Keyboardsy, Resizesy, Viewsy
from flet_easy.ui.view_404 import page_404_fs

from ._builder import ViewBuilderMixin
from ._compat import _DECLARATIVE_API_AVAILABLE
from ._declarative import DeclarativeMixin
from ._events import EventsMixin
from ._middleware import MiddlewareMixin
from ._navigation import NavigationMixin
from ._url import UrlMixin


class FletEasyX(
    DeclarativeMixin,
    ViewBuilderMixin,
    NavigationMixin,
    MiddlewareMixin,
    EventsMixin,
    UrlMixin,
):
    """flet-easy router — manages routes, views, and navigation.

    The logic is distributed in mixins by responsibility:
    - DeclarativeMixin  → declarative mode (app(), @ft.component)
    - ViewBuilderMixin  → imperative view construction
    - NavigationMixin   → routing engine (_go, _navigate, _view_append)
    - MiddlewareMixin   → middleware pipeline
    - EventsMixin       → Flet event handlers (imperative)
    - UrlMixin          → URL matching with dynamic parameters
    """

    __slots__ = (
        "_page_on_keyboard",
        "_route_prefix",
        "_route_init",
        "_route_login",
        "_on_resize",
        "_on_keyboard",
        "_pages",
        "_history_pages",
        "_view_404",
        "_automatically_imply_leading",
        "_can_pop_supported",
        "_page",
        "_page_404",
        "_config_login",
        "_middlewares_after",
        "_pagesy",
        "_middlewares",
        "_auto_logout",
        "_secret_key",
        "_page_on_resize",
        "_data",
        "_view_data_func",
        "_view_config_func",
        "_config_event_func",
        "_logger",
        "_exact_routes_map",
        "_is_web",
        "_declarative_mode",
        "_resolved_views",
        "_declarative_set_route_state",
        "_use_error_boundary",
    )

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: Optional[str],
        page_404: Optional[Pagesy],
        pages: deque[Pagesy],
        view_data: Optional[Callable[[Datasy], Viewsy]],
        config_login: Optional[Callable[[Datasy], bool]],
        view_config: Optional[Callable[[Page], None]],
        config_event: Optional[Callable[[Datasy], None]],
        middlewares: Optional[Union[list[MiddlewareItem], deque[MiddlewareItem]]],
        middlewares_after: Optional[Union[list[MiddlewareItem], deque[MiddlewareItem]]],
        on_resize: bool,
        on_keyboard: bool,
        secret_key: Optional[SecretKey],
        auto_logout: bool,
        use_error_boundary: bool,
    ) -> None:
        self._page_on_keyboard = Keyboardsy()

        self._route_prefix = route_prefix
        self._route_init = route_init
        self._route_login = route_login
        self._on_resize = on_resize
        self._on_keyboard = on_keyboard

        self._pages = pages
        self._history_pages: dict[str, Union[View, Callable[..., Any]]] = {}
        self._view_404 = page_404_fs
        self._automatically_imply_leading = False
        self._can_pop_supported = hasattr(View, "can_pop")

        self._page: Page = page
        setattr(self._page, "_flet_easy_router", self)  # noqa: B010
        self._is_web: bool = page.web
        self._page_404: Optional[Pagesy] = page_404
        self._config_login = config_login

        self._middlewares_after = middlewares_after
        self._pagesy: Optional[Pagesy] = None
        self._middlewares = middlewares

        self._auto_logout = auto_logout
        self._secret_key = secret_key
        self._use_error_boundary = use_error_boundary

        self._page_on_resize = Resizesy(self._page)
        self._data: Datasy = Datasy(
            page=self._page,
            route_prefix=self._route_prefix,
            route_init=self._route_init,
            route_login=self._route_login,
            secret_key=self._secret_key,
            auto_logout=self._auto_logout,
            page_on_keyboard=self._page_on_keyboard,
            page_on_resize=self._page_on_resize,
            go=self._go,
        )

        current_data.set(self._data)
        MiddlewareRequest._data = self._data

        # O(1) lookup for routes without parameters
        self._exact_routes_map: dict[str, Pagesy] = {}
        for p in self._pages:
            if "{" not in p.route:
                self._exact_routes_map[p.route] = p
            p._check_middleware(middlewares)

        if self._route_login is not None:
            self._data._create_login()

        self._view_data_func = view_data
        self._view_config_func = view_config
        self._config_event_func = config_event

        self._logger = get_logger("FletEasyX")
        self._declarative_mode: bool = False
        self._resolved_views: dict[str, Any] = {}
        self._declarative_set_route_state: Optional[Callable[[RouteState], Any]] = None

    def run(self, declarative: bool = False) -> None:
        """Configures and starts the router."""
        self._resolve_components()

        if self._route_init != "/" and self._page.route == "/":
            self._page.route = self._route_init

        # Synchronizes the initial Data route to avoid the race condition where
        # app() pre-launches _resolve_and_set() asynchronously competing with _init_and_go()
        self._data.route = self._page.route

        any_components = any(p._is_component for p in self._pages)
        is_mock_page = "unittest.mock" in type(self._page).__module__
        self._declarative_mode = bool(
            _DECLARATIVE_API_AVAILABLE and (declarative or (any_components and not is_mock_page))
        )

        # In imperative mode, events are configured externally.
        # In declarative mode, on_route_change is managed within app().
        if not self._declarative_mode:
            self._page.on_route_change = self._route_change
            self._page.on_view_pop = self._view_pop

        if LoggingFletEasy._logger_activated:
            self._page.on_error = lambda e: self._logger.error("Page error: %s", e)

        self._page.on_disconnect = self._disconnect

        if self._on_resize:
            self._page.on_resize = cast(Any, self._page_resize)
        if self._on_keyboard:
            self._page.on_keyboard_event = self._on_keyboard_event

        async def _init_and_go() -> None:
            try:
                view_result, _, _ = await asyncio.gather(
                    self._await_func(self._view_data_func, self._data),
                    self._await_func(self._view_config_func, self._page),
                    self._await_func(self._config_event_func, self._data),
                )
                self._data.view = view_result
                await self._go(self._page.route, use_route_change=True)
            except Exception as e:
                self._logger.exception("Error during _init_and_go startup: %s", e)
                # Ensure the error is visible if we are in declarative mode
                if self._declarative_mode and self._declarative_set_route_state is not None:
                    # We can't easily show the detailed error here
                    # because we don't have the factory, but at least we can trigger a re-render
                    # or the error might have already been caught in _go -> _view_append
                    pass

        if self._declarative_mode:
            _render = getattr(self._page, "render_views", None) or getattr(
                self._page, "render", None
            )
            if _render is None:
                # render_views not available: fallback to imperative mode
                self._declarative_mode = False
                self._page.on_route_change = self._route_change
                self._page.on_view_pop = self._view_pop
                self._page.run_task(_init_and_go)
                return

            _render(self.app)
            self._page.run_task(_init_and_go)
            return

        self._page.run_task(_init_and_go)

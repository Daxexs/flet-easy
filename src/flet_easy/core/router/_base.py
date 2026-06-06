"""Base interface class for FletEasyX mixins.

Under TYPE_CHECKING, it declares:
- Instance attributes (FletEasyX slots)
- Cross-mixin methods (for visibility in mixins by the type checker)

No runtime logic or state.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from collections import deque

    from flet import Page

    from flet_easy.core.data import Datasy
    from flet_easy.core.models import RouteState
    from flet_easy.core.pages import Pagesy
    from flet_easy.security.config import SecretKey
    from flet_easy.ui.controls import Keyboardsy, Resizesy


class _RouterBase:
    """Base with type annotations for FletEasyX mixins.

    Only active under TYPE_CHECKING — zero runtime cost.
    """

    __slots__ = ()

    if TYPE_CHECKING:
        # ---- Page infrastructure ----
        _page: Page
        _is_web: bool
        _page_on_keyboard: Keyboardsy
        _page_on_resize: Resizesy

        # ---- Routes ----
        _route_prefix: str
        _route_init: str
        _route_login: str | None
        _on_resize: bool
        _on_keyboard: bool

        # ---- Registered pages ----
        _pages: deque[Pagesy]
        _exact_routes_map: dict[str, Pagesy]
        _page_404: Pagesy | None
        _view_404: Any

        # ---- View cache ----
        _history_pages: dict[str, Any]
        _can_pop_supported: bool
        _automatically_imply_leading: bool

        # ---- Session state ----
        _data: Datasy
        _pagesy: Pagesy | None
        _config_login: Callable[[Datasy], bool] | None
        _middlewares: Any
        _middlewares_after: Any
        _auto_logout: bool
        _secret_key: SecretKey | None

        # ---- Configuration callbacks ----
        _view_data_func: Any
        _view_config_func: Any
        _config_event_func: Any

        # ---- Declarative mode ----
        _declarative_mode: bool
        _resolved_views: dict[str, Any]
        _declarative_set_route_state: Callable[[RouteState], Any] | None

        # ---- Logging and Error Handling ----
        _logger: Any
        _use_error_boundary: bool

        # ---- Cross-mixin method stubs ----
        # Declared here for visibility in any mixin by the type checker.

        async def _go(
            self,
            route: str | int,
            use_route_change: bool = ...,
            page_reload: bool = ...,
        ) -> None: ...

        async def _await_func(
            self, func: Callable[..., Any] | None, *args: Any, **kwargs: Any
        ) -> Any: ...

        def _check_async(
            self,
            func: Callable[..., Any] | None,
            *args: Any,
            result: bool = ...,
            **kwargs: Any,
        ) -> Any: ...

        async def _view_append(self, route: str, pagesy: Pagesy) -> None: ...

        async def _navigate(
            self,
            route: str,
            pagesy: Pagesy,
            use_route_change: bool,
            page_reload: bool = ...,
        ) -> None: ...

        async def _reload_datasy(
            self,
            pagesy: Pagesy,
            url_params: dict[str, Any] | None = ...,
        ) -> None: ...

        async def _run_middlewares_optimized(
            self,
            route: str,
            route_match: dict[str, Any],
            pagesy: Pagesy,
            use_route_change: bool,
            page_reload: bool = ...,
        ) -> None: ...

        async def _run_after_request_middlewares(self, pagesy: Pagesy) -> None: ...

        async def _build_view_only(self, route: str, pagesy: Pagesy) -> Any: ...

        async def _construct_raw_view(self, pagesy: Pagesy) -> Any: ...

        async def _build_component_view_only(self, route: str, pagesy: Pagesy) -> Any: ...

        async def _render_imperative_view(self, route: str, pagesy: Pagesy) -> None: ...

        async def _render_imperative_component(self, route: str, pagesy: Pagesy) -> None: ...

        def _verify_url(
            self,
            url_pattern: str,
            url: str,
            custom_types: dict[str, Callable[[str], Any]] | None = ...,
        ) -> dict[str, Any] | None: ...

        def _wrap_view(self, view: Any) -> Any: ...

        def _prepare_view(
            self, view: Any, route: str, pagesy: Pagesy, use_cache: bool = ...
        ) -> Any: ...

        def _manage_dynamic_appbar(
            self,
            route: str,
            appbar: Any,
            drawer: Any,
            can_pop: bool = ...,
            clear: bool = ...,
        ) -> None: ...

        def _manage_dynamic_navigation_bar(
            self,
            navigation_bar: Any,
            index: int | None,
        ) -> None: ...

        async def _handle_404_case(self, route: str, use_route_change: bool) -> None: ...

        async def _page_reload(self, route: str, pagesy: Pagesy) -> None: ...

"""Declarative mode mixin for FletEasyX (Flet >= 0.80).

Contains:
- _build_component_view_only: creates an @ft.component factory for each route.
- routing_declarative: resolves routes for context consumers.
- app(): root component mounted with page.render_views().
"""

import traceback
from typing import Any, cast

from flet_easy import Redirect
from flet_easy.core.context import current_data
from flet_easy.core.models import RouteState, RoutingContextValue
from flet_easy.core.pages import Pagesy
from flet_easy.ui.view_error import page_error_fs

from ._base import _RouterBase
from ._builder import _HISTORY_CACHE_MAXSIZE
from ._compat import _DECLARATIVE_API_AVAILABLE, Routingctx, ft_component, use_state


class DeclarativeMixin(_RouterBase):
    """Mixin for Flet's declarative rendering mode."""

    __slots__ = ()

    # ------------------------------------------------------------------
    # Component factory construction for a route
    # ------------------------------------------------------------------

    async def _build_component_view_only(self, route: str, pagesy: Pagesy) -> Any:
        """Builds an @ft.component factory for the given route.

        The factory:
        1. Executes the page function in a component context (hooks work).
        2. Wraps any result (Row, Text, etc.) in ft.View.
        3. It is reusable: if cache=True, it is stored in _history_pages.
        """
        render_node = self._history_pages.get(route) if pagesy.cache else None

        if render_node is None:
            self._logger.debug("Building declarative factory for route: %s", route)
            pv = pagesy.view

            if isinstance(pv, type):
                try:
                    _has_class_params = pagesy._get_view_has_params()
                except ValueError:
                    _has_class_params = False

                view_instance = (
                    pv(self._data, **self._data.url_params) if _has_class_params else pv()
                )
                if not hasattr(view_instance, "data"):
                    view_instance.data = self._data
                component_fn = view_instance.build
                _has_params = pagesy._get_build_has_params(component_fn)
            else:
                component_fn = pv
                _has_params = pagesy._get_view_has_params()

            # Local references to avoid capturing `self` in the component closure
            data = self._data
            url_params = self._data.url_params or {}
            logger = self._logger

            @ft_component
            def _page_component() -> Any:
                current_data.set(data)
                logger.debug("Evaluating _page_component declarative function for route: %s", route)

                try:
                    c_func = cast(Any, component_fn)
                    raw_func = getattr(c_func, "__wrapped__", c_func)

                    # Correctly unwrap class methods
                    result = (
                        (
                            raw_func(c_func.__self__, data, **url_params)
                            if _has_params
                            else raw_func(c_func.__self__)
                        )
                        if hasattr(c_func, "__self__")
                        else raw_func(data, **url_params)
                        if _has_params
                        else raw_func()
                    )

                    # If the result is a component, its execution is deferred.
                    # Wrap its build method to catch exceptions within the Error Boundary.
                    if hasattr(result, "build") and callable(result.build):
                        original_build = result.build

                        def safe_build():
                            try:
                                return original_build()
                            except Exception as e:
                                logger.exception(
                                    "Error in component build for route '%s': %s", route, e
                                )
                                return page_error_fs(
                                    route,
                                    traceback.format_exc() if self._use_error_boundary else None,
                                )

                        object.__setattr__(result, "build", safe_build)

                    # Handle Redirect returns (triggers async navigation and renders nothing)
                    if isinstance(result, Redirect):
                        self._page.run_task(self._go, result.route)
                        return

                    return self._prepare_view(result, route, pagesy, use_cache=False)

                except Exception as e:
                    logger.exception("Error in page component for route '%s': %s", route, e)
                    return page_error_fs(
                        route, traceback.format_exc() if self._use_error_boundary else None
                    )

            render_node = _page_component

            if pagesy.cache:
                if len(self._history_pages) >= _HISTORY_CACHE_MAXSIZE:
                    self._history_pages.pop(next(iter(self._history_pages)))
                self._history_pages[route] = render_node

        return render_node

    # ------------------------------------------------------------------
    # Public API of the declarative mode
    # ------------------------------------------------------------------

    def routing_declarative(self, route: str) -> Any:
        """Resolves a route for Routingctx consumers (ft.use_context).

        Launches asynchronous resolution as a side-effect and returns the
        cached view synchronously (or a "Loading..." placeholder if it's not ready yet).
        """
        current_data.set(self._data)
        self._page.run_task(self._resolve_and_set, route)
        resolved = self._resolved_views.get(route)
        if resolved is None:
            return
        return resolved() if callable(resolved) else resolved

    async def _resolve_and_set(self, route: str) -> None:
        """Asynchronous side-effect: resolves the route and triggers re-render."""
        self._logger.debug("Task _resolve_and_set executing for route: %s", route)
        await self._go(route, use_route_change=True)

    # ------------------------------------------------------------------
    # Declarative root component
    # ------------------------------------------------------------------

    @ft_component
    def app(self) -> Any:
        current_data.set(self._data)
        if not _DECLARATIVE_API_AVAILABLE or use_state is None:
            from flet_easy.exceptions import ViewError

            raise ViewError(
                "Declarative mode is not available in this Flet version. "
                "Please upgrade Flet to >= 0.80 to use @ft.component routing."
            )

        page = self._page
        route_state, set_route_state = use_state(RouteState(page.route))

        self._declarative_set_route_state = set_route_state

        page.on_route_change = route_state.on_route_change
        page.on_view_pop = route_state.view_popped

        route = route_state.route
        resolved = self._resolved_views.get(route)

        self._logger.debug("app() rendered | RouteState: %s | Resolved: %s", route, bool(resolved))

        if resolved is None and self._data.route != route:
            self._logger.debug(
                "app() initiating _resolve_and_set task for unresolved route: %s", route
            )
            page.run_task(self._resolve_and_set, route)
        elif resolved is None:
            # If route matches data but resolved is None, it's the startup state
            # We must ensure _init_and_go is running or start it.
            self._logger.debug("app() startup state for route: %s", route)

        def _render_node() -> Any:
            self._logger.debug("_render_node() requested for route: %s", route)
            if resolved is None:
                return
            return resolved() if callable(resolved) else resolved

        if Routingctx is None:
            self._logger.debug("Flet-easy using direct _render_node() (Routingctx unavailable)")
            return _render_node()

        return Routingctx(
            value=RoutingContextValue(views=self.routing_declarative),
            callback=_render_node,
        )

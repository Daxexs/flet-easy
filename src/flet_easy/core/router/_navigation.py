"""Central navigation and routing mixin for FletEasyX.

Contains the routing engine: route resolution, view dispatch,
AppBar/NavigationBar management, data reloading, and 404 handling.
"""

import asyncio
import sys
from functools import lru_cache
from inspect import iscoroutinefunction
from typing import Any, Callable, Optional, Union

from flet import AppBar, IconButton, Icons, NavigationBar, NavigationDrawer, View

from flet_easy.core.context import current_data
from flet_easy.core.models import Redirect, RouteState
from flet_easy.core.pages import Pagesy
from flet_easy.exceptions import ConfigurationError, LoginRequiredError, RouteError
from flet_easy.migration import go_page

from ._base import _RouterBase

# Cached coroutine checker — avoids calling iscoroutinefunction() on every navigation.
_is_coroutine = lru_cache(maxsize=None)(iscoroutinefunction)


class NavigationMixin(_RouterBase):
    """Mixin with the core of the routing and navigation engine."""

    __slots__ = ()

    # ------------------------------------------------------------------
    # Sync/async dispatch
    # ------------------------------------------------------------------

    def _check_async(
        self, func: Optional[Callable[..., Any]], *args: Any, result: bool = False, **kwargs: Any
    ) -> Any:
        """Dispatches a sync or async function, optionally returning a result."""
        if func is None:
            return None

        if _is_coroutine(func):
            if result:
                try:
                    current_loop = asyncio.get_running_loop()
                except RuntimeError:
                    current_loop = None

                if current_loop and current_loop is self._page.loop:
                    return func(*args, **kwargs)
                else:
                    future = asyncio.run_coroutine_threadsafe(
                        func(*args, **kwargs), self._page.loop
                    )
                    return future.result()
            else:
                self._page.run_task(func, *args, **kwargs)
                return None
        else:
            return func(*args, **kwargs)

    async def _await_func(
        self, func: Optional[Callable[..., Any]], *args: Any, **kwargs: Any
    ) -> Any:
        """Awaits async functions; executes sync ones in a thread pool for web."""
        if func is None:
            return None

        if _is_coroutine(func):
            return await func(*args, **kwargs)

        # Web: multiple sessions share the same event loop — avoid blocking.
        if self._is_web:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

        return func(*args, **kwargs)

    # ------------------------------------------------------------------
    # @ft.component pages resolution
    # ------------------------------------------------------------------

    def _resolve_components(self) -> None:
        """Detects pages decorated with @ft.component after @app.page."""
        for p in self._pages:
            if p._is_component:
                continue

            if not hasattr(p.view, "__flet_easy_pagesy__"):
                continue

            try:
                module_name = getattr(p.view, "__module__", None)
                module = sys.modules.get(module_name) if module_name else None
            except Exception:
                module = None

            if not module:
                continue

            func_name = getattr(p.view, "__name__", "")
            current_func = getattr(module, func_name, None)

            if (
                callable(current_func)
                and getattr(current_func, "__is_component__", False)
                and getattr(current_func, "__wrapped__", None) is p.view
            ):
                p.view = current_func
                p._is_component = True

    # ------------------------------------------------------------------
    # Per-page data state
    # ------------------------------------------------------------------

    async def _reload_datasy(
        self,
        pagesy: Pagesy,
        url_params: Optional[dict[str, Any]] = None,
    ) -> None:
        """Updates the Datasy state when navigating between pages."""
        current_data.set(self._data)
        self._logger.debug(
            "Datasy reload | Route: %s | Title: %s | Cache: %s | Share_data: %s",
            pagesy.route,
            pagesy.title,
            pagesy.cache,
            pagesy.share_data,
        )
        self._page.title = pagesy.title or "Flet-easy"

        if not pagesy.share_data and self._data.history_routes and self._data.share:
            self._logger.debug("Clearing Datasy shared data across pages")
            await self._await_func(self._data.share.clear)

        if self._on_keyboard:
            self._data.on_keyboard_event.current_route = pagesy.route
            if not pagesy.cache:
                self._data.on_keyboard_event.clear()

        self._data.url_params = url_params or {}
        self._data.route = pagesy.route

    # ------------------------------------------------------------------
    # Dynamic UI: AppBar and NavigationBar
    # ------------------------------------------------------------------

    def _manage_dynamic_navigation_bar(
        self,
        navigation_bar: Optional[Union[NavigationBar, Any]],
        index: Optional[int],
    ) -> None:
        """Updates the selected index of the navigation bar."""
        if navigation_bar is None or index is None:
            return
        navigation_bar.selected_index = index

    def _manage_dynamic_appbar(
        self,
        route: str,
        appbar: Optional[Union[AppBar, Any]],
        drawer: Optional[NavigationDrawer],
        can_pop: bool = False,
        clear: bool = False,
    ) -> None:
        """Manages the leading button of the AppBar based on navigation history."""
        if appbar is None or clear:
            return

        if route == self._route_init:
            if can_pop:
                appbar.leading = None
            elif appbar.automatically_imply_leading:
                appbar.automatically_imply_leading = False
                self._automatically_imply_leading = True
            return

        if (
            can_pop
            and appbar.automatically_imply_leading
            and len(self._data.history_routes) != 0
            and appbar.leading is None
            and drawer is None
        ):
            appbar.leading = IconButton(Icons.ARROW_BACK, on_click=self._data.go_back)
        elif not appbar.automatically_imply_leading and self._automatically_imply_leading:
            appbar.automatically_imply_leading = True

    # ------------------------------------------------------------------
    # View append (imperative + declarative entry point)
    # ------------------------------------------------------------------

    async def _view_append(self, route: str, pagesy: Pagesy) -> None:
        """Builds and renders (or caches for declarative) a page view."""
        self._logger.debug("Building view: %s", route)

        if self._declarative_mode:
            # Declarative: resolve view, cache it, trigger re-render via state.
            # Never uses page.views.append() — Routingctx delivers the view to Flet.
            built = await self._build_view_only(route, pagesy)

            if isinstance(built, Redirect):
                if built.route is not None:
                    print("xRedirecting to: ", built.route)
                    await self._go(built.route)
                return

            if isinstance(built, View):
                self._manage_dynamic_appbar(
                    route, built.appbar, built.drawer, self._can_pop_supported, pagesy.clear
                )
                self._manage_dynamic_navigation_bar(built.navigation_bar, pagesy.index)

            self._resolved_views[route] = built
            self._data.history_routes.append((route, pagesy.index))
            await self._run_after_request_middlewares(pagesy)

            # Update page.route (browser URL) — without calling go_page to avoid
            # premature re-render of app() before the view is resolved.
            if self._page.route != route:
                self._page.route = route

            if self._declarative_set_route_state is not None:
                self._declarative_set_route_state(RouteState(route))
            return

        # Imperative
        if pagesy._is_component:
            await self._render_imperative_component(route, pagesy)
        else:
            await self._render_imperative_view(route, pagesy)

    # ------------------------------------------------------------------
    # Routing core: _go, _navigate, 404, reload
    # ------------------------------------------------------------------

    async def _go(
        self,
        route: Union[str, int],
        use_route_change: bool = False,
        page_reload: bool = False,
    ) -> None:
        """Main dispatcher: resolves the route and navigates."""
        # 1. Integer index routes
        if isinstance(route, int):
            for p in self._pages:
                if p.index == route:
                    route = p.route
                    break
            else:
                await self._handle_404_case(str(route), use_route_change)
                return

        route_str: str = str(route)

        # 2. Fast lookup for exact routes (no parameters)
        page = self._exact_routes_map.get(route_str)
        if page:
            route_match: dict[str, Any] = {}
            try:
                if page.protected_route:
                    if not await self._check_protected_route_optimized(
                        page, route_str, route_match, use_route_change
                    ):
                        return
                    return

                await self._run_middlewares_optimized(
                    route_str, route_match, page, use_route_change, page_reload
                )
            except Exception as e:
                raise RouteError(
                    detail=f"Error processing route '{route_str}' (page: {page.route}): {e}"
                )
            return

        # 3. Fallback: regex matching for dynamic routes
        for p in self._pages:
            if "{" not in p.route:
                continue

            route_match_opt = self._verify_url(p.route, route_str, p.custom_params)
            if route_match_opt is None:
                continue

            try:
                if p.protected_route:
                    if not await self._check_protected_route_optimized(
                        p, route_str, route_match_opt, use_route_change
                    ):
                        return
                    return

                await self._run_middlewares_optimized(
                    route_str, route_match_opt, p, use_route_change, page_reload
                )
            except Exception as e:
                raise RouteError(
                    detail=f"Error processing route '{route_str}' (page: {p.route}): {e}"
                ) from e
            return

        # 4. Route not found
        await self._handle_404_case(route_str, use_route_change)

    async def _check_protected_route_optimized(
        self,
        pagesy: Pagesy,
        route: str,
        route_match: dict[str, Any],
        use_route_change: bool,
    ) -> bool:
        """Verifies authentication for protected routes."""
        route_login = self._route_login
        if self._config_login is None or route_login is None:
            raise ConfigurationError(
                "Cannot check protected route: 'route_login' is not set in FletEasy(). "
                "Add route_login='/your-login-route' to the FletEasy constructor."
            )

        try:
            auth = await self._await_func(self._config_login, self._data)
            if not auth:
                await self._go(route_login)
                return False

            await self._reload_datasy(pagesy, route_match)
            await self._navigate(route, pagesy, use_route_change)
            return True
        except Exception as e:
            raise LoginRequiredError(
                f"Protected route '{route}' authentication check failed. "
                f"Ensure the 'login' config function is async and returns bool.",
                detail=e,
            ) from e

    async def _navigate(
        self,
        route: str,
        pagesy: Pagesy,
        use_route_change: bool,
        page_reload: bool = False,
    ) -> None:
        """Dispatches to _view_append (declarative / route_change) or go_page (imperative)."""
        if use_route_change or self._declarative_mode:
            # Declarative: always resolve directly.
            # NEVER call go_page — it would change page.route and trigger an
            # app() re-render BEFORE the view is resolved, causing a blank frame.
            await self._view_append(route, pagesy)
        else:
            if page_reload:
                await self._page_reload(route, pagesy)
                return

            if self._page.route != route:
                self._pagesy = pagesy
                self._logger.debug("Navigating to: %s", route)
                await go_page(self._page, route)
            else:
                await self._view_append(route, pagesy)

    async def _handle_404_case(self, route: str, use_route_change: bool) -> None:
        """Renders the 404 page for routes not found."""
        page = self._page_404 or Pagesy(route, self._view_404, "Flet-Easy 404")
        if page.route is None:
            page.route = route

        await self._reload_datasy(page)
        await self._navigate(page.route, page, use_route_change)

    async def _page_reload(self, route: str, pagesy: Pagesy) -> None:
        """Reloads a page — evicts the cache if enabled."""
        if pagesy.cache:
            try:
                self._data.history_routes.pop()
                self._history_pages.pop(route)
            except (IndexError, KeyError):
                self._logger.warning(
                    "Page reload for '%s': cache entry not found, rebuilding.", route
                )

        await self._view_append(route, pagesy)

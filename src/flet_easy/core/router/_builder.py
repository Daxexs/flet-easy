"""View construction mixin for FletEasyX (imperative mode).

Builds views without mutating them directly in page.views —
writing to the page occurs in _navigation.py (_view_append).

Also defines _HISTORY_CACHE_MAXSIZE, imported by _declarative.py.
"""

import traceback
from typing import Any, Optional, Union

from flet import PagePlatform, Text, View

from flet_easy.core.models import Redirect
from flet_easy.core.pages import Pagesy
from flet_easy.exceptions import ViewError
from flet_easy.migration import Control
from flet_easy.ui.view_error import page_error_fs

from ._base import _RouterBase

# Maximum number of cached views/factories in _history_pages (FIFO policy).
_HISTORY_CACHE_MAXSIZE = 100


class ViewBuilderMixin(_RouterBase):
    """Mixin to build imperative views without rendering them directly."""

    __slots__ = ()

    # ------------------------------------------------------------------
    # Shared utilities
    # ------------------------------------------------------------------

    def _wrap_view(self, view: Any) -> View:
        """Wraps the return value in ft.View if it is not already."""
        if isinstance(view, (View, Redirect)):
            return view
        elif isinstance(view, list):
            return View(controls=view)
        elif isinstance(view, str):
            return View(controls=[Text(view)])
        elif isinstance(view, Control) or (hasattr(view, "build") and callable(view.build)):
            return View(controls=[view])
        else:
            raise ValueError(f"FletEasy: Unsupported page return type '{type(view).__name__}'")

    def _prepare_view(self, view: Any, route: str, pagesy: Pagesy, use_cache: bool = True) -> View:
        """Prepares a View for navigation (settings route, can_pop, etc.)."""
        # If caching is enabled, check for a cached View instance.
        if use_cache:
            cached = self._history_pages.get(route)
            if isinstance(cached, View):
                return cached

        wrapped = self._wrap_view(view)

        if not isinstance(wrapped, Redirect):
            if not wrapped.route or (wrapped.route == "/" and route != "/"):
                wrapped.route = route

            if (
                self._can_pop_supported
                and route != self._route_init
                and wrapped.on_confirm_pop is None
            ):
                wrapped.can_pop = False
                wrapped.on_confirm_pop = lambda e: self._data.confirm_pop(e)

            if use_cache and pagesy.cache:
                if len(self._history_pages) >= _HISTORY_CACHE_MAXSIZE:
                    self._history_pages.pop(next(iter(self._history_pages)))
                self._history_pages[route] = wrapped

        return wrapped

    def _pop_supported(self, route: str) -> Optional[Union[View, Any]]:
        """Returns the cached view for the route, if cache is supported."""
        cached = None
        if self._can_pop_supported:
            cached = self._history_pages.get(route)
        else:
            # Old versions of Flet (< v0.28.0): no cache on Android/iOS.
            plat = self._page.platform
            if plat not in (PagePlatform.ANDROID, PagePlatform.IOS):
                cached = self._history_pages.get(route)

        if cached is not None:
            self._logger.debug("Cache hit -> View recovered for route: '%s'", route)
        return cached

    def _clean_page_views(self, route: str) -> None:
        """Safely clears page.views before adding the new view."""
        if route == self._route_init:
            self._data.history_routes.clear()

        # render_views() can replace page.views with a Component — reset to list.
        if not hasattr(self._page.views, "append"):
            self._page.views = []
            return

        if self._can_pop_supported:
            self._page.views.clear()
        else:
            plat = self._page.platform
            if plat in (PagePlatform.ANDROID, PagePlatform.IOS) and route == self._route_init:
                self._page.views.clear()

            try:
                if len(self._page.views) > 1:
                    self._page.views.pop()
            except TypeError:
                self._page.views = []

    # ------------------------------------------------------------------
    # Shared raw view construction

    async def _construct_raw_view(self, pagesy: Pagesy) -> Any:
        """Constructs the raw view result from a callable or class-based page.

        Shared by _build_imperative_view_only and _render_imperative_view to
        eliminate ~50 lines of duplicated callable/class dispatch logic.
        """
        pv = pagesy.view

        if callable(pv) and not isinstance(pv, type):
            self._logger.debug(
                "(build) view: %s | params: %s",
                getattr(pv, "__name__", "unknown"),
                self._data.url_params,
            )
            return (
                await self._await_func(pv, self._data, **self._data.url_params)
                if pagesy._get_view_has_params()
                else await self._await_func(pv)
            )

        elif isinstance(pv, type):
            self._logger.debug(
                "(build) class: %s | params: %s",
                pv.__name__,
                self._data.url_params,
            )
            view_instance = (
                pv(self._data, **self._data.url_params) if pagesy._get_view_has_params() else pv()
            )
            if not hasattr(view_instance, "data"):
                view_instance.data = self._data
            return (
                await self._await_func(view_instance.build, self._data, **self._data.url_params)
                if pagesy._get_build_has_params(view_instance.build)
                else await self._await_func(view_instance.build)
            )

        else:
            raise ViewError(
                f"Page view for route '{pagesy.route}' must be a function or a class with build(), "
                f"got {type(pv).__name__}: {pv}"
            )

    # ------------------------------------------------------------------
    # Construction without rendering (imperative)
    # ------------------------------------------------------------------

    async def _build_imperative_view_only(
        self, route: str, pagesy: Pagesy
    ) -> Union[View, Redirect]:
        """Builds an imperative view without writing it to page.views."""
        cached = self._pop_supported(route)
        if isinstance(cached, View):
            return cached

        view = await self._construct_raw_view(pagesy)
        return self._prepare_view(view, route, pagesy)

    async def _build_view_only(self, route: str, pagesy: Pagesy) -> Any:
        """Dispatcher: builds the correct view based on the page type."""
        if pagesy._is_component:
            return await self._build_component_view_only(route, pagesy)
        return await self._build_imperative_view_only(route, pagesy)

    # ------------------------------------------------------------------
    # Imperative render (writes to page.views)
    # ------------------------------------------------------------------

    async def _render_imperative_view(self, route: str, pagesy: Pagesy) -> None:
        """Renders a standard imperative view in page.views."""
        page = self._page
        view = self._pop_supported(route)

        if view is None:
            try:
                view = await self._construct_raw_view(pagesy)
                view = self._prepare_view(view, route, pagesy)
            except Exception as e:
                self._logger.exception(
                    "(render_imperative_view) Failed to build view for '%s': %s", route, e
                )
                view = page_error_fs(
                    route, traceback.format_exc() if self._use_error_boundary else None
                )

        if isinstance(view, Redirect):
            if view.route is not None:
                await self._go(view.route)
            return

        self._clean_page_views(route)

        # Execute dynamic controls registered for this route
        dyn = self._data._dynamic_control.get(route)
        if dyn:
            for control, func_update in dyn:
                await self._await_func(func_update, control)

        if isinstance(view, View):
            self._manage_dynamic_appbar(
                route, view.appbar, view.drawer, self._can_pop_supported, pagesy.clear
            )
            self._manage_dynamic_navigation_bar(view.navigation_bar, pagesy.index)
            if not hasattr(page.views, "append"):
                page.views = []
            page.views.append(view)

        self._data.history_routes.append((route, pagesy.index))
        page.update()

        await self._run_after_request_middlewares(pagesy)

    async def _render_imperative_component(self, route: str, pagesy: Pagesy) -> None:
        """Renders an @ft.component page in imperative mode.

        Uses _build_component_view_only to get the factory and delegates
        rendering to Flet's native _render engine.
        """
        self._logger.debug("Building imperative component: %s", route)

        page = self._page
        _render = getattr(page, "render_views", None) or getattr(page, "render", None)
        if _render is None:
            raise ViewError(
                f"Flet version does not support page.render() or page.render_views(). "
                f"Cannot render declarative component for route '{pagesy.route}'."
            )

        render_target = await self._build_component_view_only(route, pagesy)

        _render(render_target)
        self._page.update()

        self._resolved_views[route] = render_target
        self._data.history_routes.append((route, pagesy.index))

        await self._run_after_request_middlewares(pagesy)

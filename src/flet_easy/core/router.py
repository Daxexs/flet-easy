import asyncio
from collections import deque
from functools import partial
from inspect import getmodule, iscoroutinefunction, signature
from re import Pattern, compile, escape
from types import FunctionType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from flet import (
    AppBar,
    ControlEvent,
    IconButton,
    Icons,
    KeyboardEvent,
    NavigationBar,
    NavigationDrawer,
    Page,
    PagePlatform,
    RouteChangeEvent,
    View,
    ViewPopEvent,
)

try:
    # support component decorator in flet 0.80.*
    from flet import component as ft_component
except ImportError:
    ft_component = None


from flet_easy.core.data import Datasy
from flet_easy.core.middleware import MiddlewareHandler, MiddlewareRequest
from flet_easy.core.models import TYPE_PATTERNS, Msg, Redirect
from flet_easy.core.pages import Pagesy
from flet_easy.exceptions import (
    ConfigurationError,
    CustomParamsError,
    LoginRequiredError,
    MiddlewareError,
    RouteError,
    ViewError,
)
from flet_easy.logger import get_logger
from flet_easy.migration import go_page
from flet_easy.ui.controls import Keyboardsy, Resizesy, Viewsy
from flet_easy.ui.view_404 import page_404_fs


class FletEasyX:
    __compiled_patterns_cache: Dict[str, Tuple[Pattern[str], List[Tuple[str, Callable]]]] = {}

    __slots__ = (
        "__page_on_keyboard",
        "__route_prefix",
        "__route_init",
        "__route_login",
        "__on_resize",
        "__on_keyboard",
        "__pages",
        "__history_pages",
        "__view_404",
        "__automatically_imply_leading",
        "__can_pop_supported",
        "__page",
        "__page_404",
        "__config_login",
        "__middlewares_after",
        "__pagesy",
        "__middlewares",
        "__auto_logout",
        "__secret_key",
        "__page_on_resize",
        "_data",
        "__view_data_func",
        "__view_config_func",
        "__config_event_func",
        "_logger",
        "__exact_routes_map",
    )

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        page_404: Callable[[Datasy], View],
        pages: deque[Pagesy],
        view_data: Callable[[Datasy], Viewsy],
        config_login: Callable[[Datasy], bool],
        view_config: Callable[[Datasy], None],
        config_event: Callable[[Datasy], None],
        middlewares: List[Union[MiddlewareHandler, MiddlewareRequest]],
        middlewares_after: List[Union[MiddlewareHandler, MiddlewareRequest]],
        on_resize: bool,
        on_keyboard: bool,
        secret_key: str,
        auto_logout: bool,
    ):
        self.__page_on_keyboard = Keyboardsy()

        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__on_resize = on_resize
        self.__on_keyboard = on_keyboard

        self.__pages = pages
        self.__history_pages: Dict[str, View] = {}
        self.__view_404 = page_404_fs
        self.__automatically_imply_leading = False
        self.__can_pop_supported = hasattr(View(), "can_pop")

        self.__page: Page = page
        self.__page_404: Pagesy = page_404
        self.__config_login: Callable[[Datasy], bool] = config_login

        self.__middlewares_after = middlewares_after
        self.__pagesy: Pagesy = None
        self.__middlewares = middlewares

        self.__auto_logout = auto_logout
        self.__secret_key = secret_key

        # Fast lookup for routes without parameters will be populated below
        self.__page_on_resize = Resizesy(self.__page)
        self._data: Datasy = Datasy(
            page=self.__page,
            route_prefix=self.__route_prefix,
            route_init=self.__route_init,
            route_login=self.__route_login,
            secret_key=self.__secret_key,
            auto_logout=self.__auto_logout,
            page_on_keyboard=self.__page_on_keyboard,
            page_on_resize=self.__page_on_resize,
            go=self._go,
        )

        # Add data to middleware request
        MiddlewareRequest._data = self._data

        # Normalize page-level middleware and build fast lookup for routes
        self.__exact_routes_map: Dict[str, Pagesy] = {}
        for p in self.__pages:
            if "{" not in p.route:
                self.__exact_routes_map[p.route] = p
            p._check_middleware(middlewares)

        # Add login
        if self.__route_login is not None:
            self._data._create_login()

        # Store initial configuration callbacks for run()
        self.__view_data_func = view_data
        self.__view_config_func = view_config
        self.__config_event_func = config_event

        # logger
        self._logger = get_logger("FletEasyX")

    # -------- ---------[Handling 'flet' event]----------

    async def __route_change(self, e: RouteChangeEvent) -> None:
        if self.__pagesy is None:
            if e.route == "/" and self.__route_init != "/":
                await go_page(self.__page, self.__route_init)
                return

            await self._go(e.route, True)
        else:
            await self._view_append(e.route, self.__pagesy)
            self.__pagesy = None

    def __view_pop(self, e: ViewPopEvent) -> None:
        self._data.go_back()

    def __on_keyboard_event(self, e: KeyboardEvent) -> None:
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            self.__check_async(self.__page_on_keyboard._run_controls)

    def __page_resize(self, e: ControlEvent) -> None:
        self.__page_on_resize.e = e

    def __disconnect(self, e: ControlEvent) -> None:
        if self._data._login_done and self.__page.web:
            self.__page.pubsub.send_others_on_topic(
                self.__page.client_ip,
                Msg("updateLoginSessions", value=self._data._login_done),
            )

    # --------------[End of 'flet' event]------------

    # ------------ [ configuration when initializing 'flet' ]

    def __check_async(
        self, func: Callable[[Union[Datasy, Page]], Any], *args, result: bool = False, **kwargs
    ) -> Union[View, bool, None]:
        """Check if the function is async or not"""

        if func is None:
            return

        if iscoroutinefunction(func):
            if result:
                # Use Flet's primary event loop to avoid deadlocks with Flet internal futures
                try:
                    current_loop = asyncio.get_running_loop()
                except RuntimeError:
                    current_loop = None

                if current_loop and current_loop is self.__page.loop:
                    return func(*args, **kwargs)
                else:
                    future = asyncio.run_coroutine_threadsafe(
                        func(*args, **kwargs), self.__page.loop
                    )
                    return future.result()
            else:
                self.__page.run_task(func, *args, **kwargs)
                return None
        else:
            return func(*args, **kwargs)

    async def _await_func(self, func: Callable, *args, **kwargs) -> Any:
        if func is None:
            return None

        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    def _resolve_components(self) -> None:
        """Scan modules for @ft.component-wrapped page functions (reverse decorator order).

        When @ft.component is applied AFTER @app.page (i.e. on top), the Pagesy stores
        the raw function without __is_component__. This method finds the component wrapper
        by looking up the original module where the function was defined.
        """

        unresolved = [p for p in self.__pages if not p._is_component]
        if not unresolved:
            return

        for p in unresolved:
            if hasattr(p.view, "__flet_easy_pagesy__"):
                # Fast precise lookup: Get the exact module where this function lives
                module = getmodule(p.view)
                if not module:
                    continue

                # The decorated wrapper replaces the original function name in its module
                func_name = p.view.__name__
                current_func = getattr(module, func_name, None)

                # Check if the current function in the module is our component wrapper
                if (
                    callable(current_func)
                    and getattr(current_func, "__is_component__", False)
                    and getattr(current_func, "__wrapped__", None) is p.view
                ):
                    p.view = current_func
                    p._is_component = True

    def run(self):
        """configure the route init"""

        # Resolve any @ft.component decorators applied after @app.page
        self._resolve_components()

        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init

        """ Executing charter events """
        self.__page.on_route_change = self.__route_change
        self.__page.on_view_pop = self.__view_pop
        self.__page.on_error = lambda e: self._logger.error(f"Page error: {e}")
        self.__page.on_disconnect = self.__disconnect

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize
        if self.__on_keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard_event

        async def _init_and_go():
            # Execute configuration callbacks concurrently
            view_result, _, _ = await asyncio.gather(
                self._await_func(self.__view_data_func, self._data),
                self._await_func(self.__view_config_func, self.__page),
                self._await_func(self.__config_event_func, self._data),
            )
            self._data.view = view_result

            # Start routing
            await self._go(self.__page.route, use_reload=True)

        self.__page.run_task(_init_and_go)

    # ---------------------------[Route controller]-------------------------------------

    async def _view_append(self, route: str, pagesy: Pagesy) -> None:
        """Add a new page and update it."""
        self._logger.debug(f"Building view: {route}")

        if pagesy._is_component:
            await self.__render_declarative_component(route, pagesy)
        else:
            await self.__render_imperative_view(route, pagesy)

    async def __render_declarative_component(self, route: str, pagesy: Pagesy) -> None:
        """Handle rendering of declarative (@ft.component) pages."""
        page = self.__page
        _render = getattr(page, "render_views", None) or getattr(page, "render", None)
        if _render is None:
            raise ViewError(
                f"Flet version does not support page.render() or page.render_views(). "
                f"Cannot render declarative component for route '{pagesy.route}'."
            )

        # Resolve render target, using cache when available
        render_target = self.__history_pages.get(route) if pagesy.cache else None

        if render_target is None:
            component_fn = pagesy.view

            # Wrap to inject data/url_params if the component expects parameters
            if signature(component_fn).parameters:
                data = self._data
                url_params = self._data.url_params or {}

                @ft_component
                def _root():
                    return component_fn(data, **url_params)

                render_target = _root
            else:
                render_target = component_fn

            if pagesy.cache:
                self.__history_pages[route] = render_target

        _render(render_target)
        self.__page.update()
        self._data.history_routes.append((route, pagesy.index))

        await self.__run_after_request_middlewares(pagesy)

    async def __render_imperative_view(self, route: str, pagesy: Pagesy) -> None:
        """Handle rendering of standard imperative Flet views."""
        page = self.__page
        view = self.__pop_supported(route)

        # Build if not cached
        if view is None:
            pv = pagesy.view

            if isinstance(pv, FunctionType):
                view = await self._await_func(pv, self._data, **self._data.url_params)
            elif isinstance(pv, type):
                view_instance = pv(self._data, **self._data.url_params)
                view = await self._await_func(view_instance.build)
            else:
                raise ViewError(
                    f"Page view for route '{pagesy.route}' must be a function or a class with build(), "
                    f"got {type(pv).__name__}: {pv}"
                )

            if isinstance(view, Redirect):
                await self._go(view.route)
                return

            view.route = route

            # support pop flet >= 0.28.0
            if (
                self.__can_pop_supported
                and route != self.__route_init
                and view.on_confirm_pop is None
            ):
                view.can_pop = False
                view.on_confirm_pop = self._data.confirm_pop

            if pagesy.cache:
                self.__history_pages[route] = view

        # Clean the previous views safely before adding the new one
        self.__clean_page_views(route)

        # Run dynamic control if present
        dyn = self._data._dynamic_control.get(route)
        if dyn:
            for control, func_update in dyn:
                await self._await_func(func_update, control)

        # add view to the page and update it
        self.__manage_dynamic_appbar(
            route, view.appbar, view.drawer, self.__can_pop_supported, pagesy.clear
        )
        self.__manage_dynamic_navigationBar(view.navigation_bar, pagesy.index)

        # Re-capture page.views after clean (render_views may have replaced it)
        page.views.append(view)
        self._data.history_routes.append((route, pagesy.index))
        page.update()

        await self.__run_after_request_middlewares(pagesy)

    async def __run_after_request_middlewares(self, pagesy: Pagesy) -> None:
        """Execute all post-request middlewares."""
        if pagesy._valid_middlewares_request():
            for i, middleware in enumerate(pagesy._middlewares_request):
                self.__verify_instance_middleware(pagesy._middlewares_request, middleware, i)
                await self._await_func(pagesy._middlewares_request[i].after_request)

    def __manage_dynamic_navigationBar(self, navigation_bar: NavigationBar, index: int) -> None:
        """Manage the navigation bar selected index"""

        if navigation_bar is None:
            return

        navigation_bar.selected_index = index

    def __manage_dynamic_appbar(
        self,
        route: str,
        appbar: AppBar,
        drawer: NavigationDrawer,
        can_pop: bool = False,
        clear: bool = False,
    ) -> None:
        """Manage the appbar automatically_imply_leading parameter"""

        # clear: to cancel the leading configuration
        if appbar is None or clear:
            return

        # support for flet < v0.28.0
        if route == self.__route_init:
            if can_pop:
                appbar.leading = None
            elif appbar.automatically_imply_leading:
                appbar.automatically_imply_leading = False
                self.__automatically_imply_leading = True
            return

        if (
            can_pop
            and appbar.automatically_imply_leading
            and len(self._data.history_routes) != 0
            and appbar.leading is None
            and drawer is None
        ):
            appbar.leading = IconButton(Icons.ARROW_BACK, on_click=self._data.go_back)
        elif not appbar.automatically_imply_leading and self.__automatically_imply_leading:
            appbar.automatically_imply_leading = True

    def __pop_supported(self, route: str) -> Union[View, None]:
        """Pop the view from the page if it is supported"""
        view = None

        if self.__can_pop_supported:
            view = self.__history_pages.get(route)
        else:
            # support for flet < v0.28.0
            plat = self.__page.platform

            if plat not in (PagePlatform.ANDROID, PagePlatform.IOS):
                # cache is available
                view = self.__history_pages.get(route)

        return view

    def __clean_page_views(self, route: str) -> None:
        """Clear page views safely before adding the new view"""
        if route == self.__route_init:
            self._data.history_routes.clear()

        # After render_views(), page.views may be a Component instead of a list.
        # Reset to a list so the imperative view pipeline works.
        # We check for .append to be sure it's a list-like object.
        if not hasattr(self.__page.views, "append"):
            self.__page.views = []
            return

        if self.__can_pop_supported:
            self.__page.views.clear()
        else:
            plat = self.__page.platform
            if plat in (PagePlatform.ANDROID, PagePlatform.IOS) and route == self.__route_init:
                # cache not available
                self.__page.views.clear()

            # Keep only last view on stack
            try:
                if len(self.__page.views) > 1:
                    self.__page.views.pop()
            except TypeError:
                # Fallback if len() fails on some proxy objects
                self.__page.views = []

    async def __reload_datasy(
        self,
        pagesy: Pagesy,
        url_params: Dict[str, Any] = dict(),
    ) -> None:
        """Update `datasy` values when switching between pages."""

        self.__page.title = pagesy.title

        if not pagesy.share_data and self._data.history_routes:
            await self._await_func(self._data.share.clear)
        if self.__on_keyboard:
            self._data.on_keyboard_event.current_route = pagesy.route
            if not pagesy.cache:
                self._data.on_keyboard_event.clear()

        self._data.url_params = url_params
        self._data.route = pagesy.route

    def __verify_instance_middleware(
        self, middlewares: List[MiddlewareRequest], middleware: MiddlewareRequest, index: int
    ) -> MiddlewareRequest:
        """Verify if the middleware is a class or a function"""
        try:
            if isinstance(middleware, type):
                middleware = middleware()
                middlewares[index] = middleware
                self._logger.debug(f"Middleware instantiated: {middleware}")

        except Exception as e:
            raise MiddlewareError(
                f"Failed to instantiate middleware class '{type(middleware).__name__}' at index {index}.",
                detail=e,
            )

    async def __execute_middleware(
        self,
        pagesy: Pagesy,
        url_params: Dict[str, Any],
        middleware_list: List[Union[MiddlewareRequest, MiddlewareHandler]],
    ) -> bool:
        """Execute the middleware"""

        if not middleware_list:
            return False

        await self.__reload_datasy(pagesy, url_params)

        try:
            for i, middleware in enumerate(middleware_list):
                self.__verify_instance_middleware(middleware_list, middleware, i)
                m = middleware_list[i]

                self._logger.debug(
                    f"Execute middleware: index: {i} | {m} == {middleware} | {middleware_list is self.__middlewares}"
                )

                if isinstance(m, MiddlewareRequest):
                    res = await self._await_func(m.before_request)
                else:
                    res = await self._await_func(m, self._data)

                if await self._handle_middleware_result(res):
                    return True

            return False

        except Exception as e:
            raise MiddlewareError(
                f"Middleware execution failed for route '{pagesy.route}'. "
                f"Check that all middlewares return None, False, or Redirect.",
                detail=e,
            )

    async def _handle_middleware_result(self, result: Union[bool, Redirect]) -> bool:
        """Helper method to handle middleware results"""

        if not result:
            return False

        if isinstance(result, Redirect):
            await self._go(result.route)
            return True

        return False

    async def _go(
        self,
        route: Union[str, int],
        use_route_change: bool = False,
        use_reload: bool = False,
        page_reload: bool = False,
    ) -> None:
        """Method to go to the route, if the route is not found, it will return a 404 page."""

        # 1. Handle integer routes (index lookup)
        if isinstance(route, int):
            for page in self.__pages:
                if page.index == route:
                    route = page.route
                    break
            else:
                await self._handle_404_case(route, use_route_change, use_reload)
                return

        # 2. Fast lookup for exact routes
        page = self.__exact_routes_map.get(route)
        if page:
            route_match = {}
            if page_reload:
                return await self.__run_middlewares_optimized(
                    route, route_match, page, use_route_change, use_reload, page_reload
                )

            try:
                if page.protected_route and not await self.__check_protected_route_optimized(
                    page, route, route_match, use_route_change, use_reload
                ):
                    return

                if await self.__run_middlewares_optimized(
                    route, route_match, page, use_route_change, use_reload
                ):
                    return
            except Exception as e:
                raise RouteError(
                    detail=f"Error processing route '{route}' (page: {page.route}): {e}"
                )

        # 3. Fallback to regex matching for dynamic routes
        for page in self.__pages:
            if "{" not in page.route:
                continue

            route_match = self._verify_url(page.route, route, page.custom_params)
            if route_match is None:
                continue

            if page_reload:
                return await self.__run_middlewares_optimized(
                    route, route_match, page, use_route_change, use_reload, page_reload
                )

            try:
                if page.protected_route:
                    if not await self.__check_protected_route_optimized(
                        page, route, route_match, use_route_change, use_reload
                    ):
                        return
                    break

                if await self.__run_middlewares_optimized(
                    route, route_match, page, use_route_change, use_reload
                ):
                    break

            except Exception as e:
                raise RouteError(
                    detail=f"Error processing route '{route}' (page: {page.route}): {e}"
                )
            return

        # 4. Handle 404
        if page is None:
            await self._handle_404_case(route, use_route_change, use_reload)

    async def __check_protected_route_optimized(
        self, pagesy: Pagesy, route: str, route_match: str, use_route_change: bool, use_reload: bool
    ) -> bool:
        """Optimized protected route checker"""

        if self.__route_login is None:
            raise ConfigurationError(
                "Cannot check protected route: 'route_login' is not set in FletEasy(). "
                "Add route_login='/your-login-route' to the FletEasy constructor."
            )

        try:
            auth = await self._await_func(self.__config_login, self._data)
            if not auth:
                await self._go(self.__route_login)
                return False

            await self.__reload_datasy(pagesy, route_match)
            await self._navigate(route, pagesy, use_route_change, use_reload)
            return True
        except Exception as e:
            raise LoginRequiredError(
                f"Protected route '{route}' authentication check failed. "
                f"Ensure the 'login' config function is async and returns bool.",
                detail=e,
            )

    async def __run_middlewares_optimized(
        self,
        route: str,
        route_match: str,
        pagesy: Pagesy,
        use_route_change: bool,
        use_reload: bool,
        page_reload: bool = False,
    ) -> bool:
        """Optimized middleware runner"""
        self._logger.debug(f"Middlewares: {self.__middlewares}")
        self._logger.debug(f"Middleware Pagesy: {pagesy.middleware}")

        if pagesy.middleware and await self.__execute_middleware(
            pagesy, route_match, pagesy.middleware
        ):
            return True

        await self.__reload_datasy(pagesy, route_match)
        await self._navigate(route, pagesy, use_route_change, use_reload, page_reload)
        return True

    async def _navigate(
        self,
        route: str,
        pagesy: Pagesy,
        use_route_change: bool,
        use_reload: bool,
        page_reload: bool = False,
    ) -> None:
        """Unified navigation handler"""

        if use_route_change:
            await self._view_append(route, pagesy)
        else:
            if page_reload:
                return await self.__page_reload(route, pagesy)

            if self.__page.route != route:
                self.__pagesy = pagesy
                self._logger.debug(f"Navigating to: {route}")
                await go_page(self.__page, route)
            else:
                await self._view_append(route, pagesy)

    async def _handle_404_case(self, route: str, use_route_change: bool, use_reload: bool) -> None:
        """Optimized 404 handler"""

        page = self.__page_404 or Pagesy(route, self.__view_404, "Flet-Easy 404")
        if page.route is None:
            page.route = route

        await self.__reload_datasy(page)
        await self._navigate(page.route, page, use_route_change, use_reload)

    async def __page_reload(self, route: str, pagesy: Pagesy) -> None:
        """Use this method to reload the page"""

        if pagesy.cache:
            try:
                self._data.history_routes.pop()
                self.__history_pages.pop(route)
            except (IndexError, KeyError):
                self._logger.warning(
                    f"Page reload for '{route}': cache entry not found, rebuilding from scratch."
                )

        await self._view_append(route, pagesy)

    @classmethod
    def _get_compiled_pattern_and_segments(
        cls,
        url_pattern: str,
        custom_types: Optional[Dict[str, Callable[[str], Optional[bool]]]] = None,
    ) -> Tuple[Pattern[str], List[Tuple[str, Callable[[str], Optional[bool]]]]]:

        if url_pattern in cls.__compiled_patterns_cache:
            return cls.__compiled_patterns_cache[url_pattern]

        combined_patterns = {
            **TYPE_PATTERNS,
            **{k: (compile(r"[^/]+"), v) for k, v in (custom_types or {}).items()},
        }

        segments: list[Tuple[str, Callable[[str], Optional[bool]]]] = []
        pattern_parts: list[str] = []
        type_patterns: list[str] = []

        for segment in url_pattern.strip("/").split("/"):
            if segment == "":
                continue

            if segment[0] in "<{" and segment[-1] in ">}":
                name, type_ = (
                    segment[1:-1].split(":", 1) if ":" in segment else (segment[1:-1], "str")
                )
                type_patterns.append(type_)
                try:
                    regex_part, parser = combined_patterns[type_]
                except KeyError:
                    raise CustomParamsError(
                        f"Unrecognized URL parameter type '{type_}' in route '{url_pattern}'. "
                        f"Built-in types: d (int), l (str), f (float). "
                        f"Register custom types via 'custom_params' parameter."
                    )
                pattern_parts.append(f"({regex_part.pattern})")
                segments.append((name, parser))
            else:
                pattern_parts.append(escape(segment))

        if custom_types:
            for type_ in custom_types:
                if type_ not in type_patterns:
                    raise CustomParamsError(
                        f"Route '{url_pattern}' declares custom_params {list(custom_types.keys())} "
                        f"but none are used in the route pattern. Remove custom_params or use them in the route."
                    )

        pattern_key = "/".join(pattern_parts)
        pattern = compile(f"^/{pattern_key}/?$")

        cls.__compiled_patterns_cache[url_pattern] = (pattern, segments)
        return pattern, segments

    @classmethod
    def _verify_url(
        cls,
        url_pattern: str,
        url: str,
        custom_types: Optional[Dict[str, Callable[[str], Optional[bool]]]] = None,
    ) -> Optional[Dict[str, Optional[bool]]]:

        pattern, segments = cls._get_compiled_pattern_and_segments(url_pattern, custom_types)
        match = pattern.fullmatch(url)
        if not match:
            return None

        result = {name: parser(match.group(i + 1)) for i, (name, parser) in enumerate(segments)}

        return None if None in result.values() else result

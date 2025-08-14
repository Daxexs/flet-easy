import re
from collections import deque
from inspect import iscoroutinefunction
from re import Pattern, compile, escape
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from flet import (
    AppBar,
    ControlEvent,
    IconButton,
    Icons,
    KeyboardEvent,
    Page,
    PagePlatform,
    RouteChangeEvent,
    View,
    ViewPopEvent,
)

from flet_easy.datasy import Datasy
from flet_easy.exceptions import LoginRequiredError, MidlewareError, RouteError
from flet_easy.extra import TYPE_PATTERNS, Msg, Redirect
from flet_easy.inheritance import Keyboardsy, Resizesy, Viewsy
from flet_easy.middleware import Middleware
from flet_easy.pagesy import MiddlewareRequest, Pagesy
from flet_easy.view_404 import page_404_fs


class FletEasyX:
    __compiled_patterns_cache: Dict[str, re.Pattern[str]] = {}

    def __init__(
        self,
        route_prefix: str,
        route_init: str,
        route_login: str,
        on_resize: bool,
        on_Keyboard: bool,
        secret_key: str,
        auto_logout: bool,
    ):
        self.__page_on_keyboard = Keyboardsy()

        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__on_resize = on_resize
        self.__on_Keyboard = on_Keyboard

        self._pages = deque()
        self.__history_pages: Dict[str, View] = {}
        self.__view_404 = page_404_fs
        self.__automatically_imply_leading = False

        self.__page: Page = None
        self._page_404: Pagesy = None
        self._view_data: Callable[[Datasy], Viewsy] = None
        self._config_login: Callable[[Datasy], bool] = None
        self._view_config: Callable[[Datasy], None] = None
        self._config_event: Callable[[Datasy], None] = None
        self._middlewares_after: Optional[List[MiddlewareRequest]] = None
        self.__pagesy: Pagesy = None
        self._middlewares: Middleware = None

        self.__auto_logout = auto_logout
        self.__secret_key = secret_key
        self.__page_on_resize: Resizesy = None
        self._data: Datasy = Datasy(
            route_prefix="" if self.__route_prefix is None else self.__route_prefix,
            route_init=self.__route_init,
            route_login=self.__route_login,
            secret_key=self.__secret_key,
            auto_logout=self.__auto_logout,
            page_on_keyboard=self.__page_on_keyboard,
            go=self._go,
        )

    # -------- ---------[Handling 'flet' event]----------

    def __route_change(self, e: RouteChangeEvent):
        if self.__pagesy is None:
            if e.route == "/" and self.__route_init != "/":
                return self.__page.go(self.__route_init)

            self._go(e.route, True)
        else:
            self._view_append(e.route, self.__pagesy)
            self.__pagesy = None

    def __view_pop(self, e: ViewPopEvent):
        self._data.go_back()()

    async def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.e = e

    def __disconnect(self, e):
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
            res = self.__page.run_task(func, *args, **kwargs)

            if result:
                return res.result(5)
            else:
                return res
        else:
            return func(*args, **kwargs)

    def __config_datasy(self):
        """configure datasy"""
        self.__page_on_resize = Resizesy(self.__page)
        self._data.page = self.__page
        self._data.on_resize = self.__page_on_resize

        """Add the `View` configuration, to reuse on every page."""
        self._data.view = self.__check_async(self._view_data, self._data, result=True)

        if self.__route_login is not None:
            self._data._create_login()

    def _add_configuration_start(self, page: Page):
        """Add general settings to the pages."""
        self.__page = page
        self.__config_datasy()

        """ Add view configuration """
        self.__check_async(self._view_config, self.__page)

        """ Add configuration event """
        self.__check_async(self._config_event, self._data)

    # ------------[Initialization]----------

    def _run(self):
        """configure the route init"""
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init

        """ Executing charter events """
        self.__page.on_route_change = self.__route_change
        self.__page.on_view_pop = self.__view_pop
        self.__page.on_error = lambda e: print("Page error:", e)
        self.__page.on_disconnect = self.__disconnect

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize
        if self.__on_Keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard

        self._go(self.__page.route, use_reload=True)

    # ---------------------------[Route controller]-------------------------------------

    def _view_append(self, route: str, pagesy: Pagesy) -> None:
        """Add a new page and update it."""

        page = self.__page
        page_views = page.views
        view = self.__pop_supported(route)

        # Build if not cached
        if view is None:
            pv = pagesy.view
            if callable(pv) and not isinstance(pv, type):
                view = self.__check_async(pv, self._data, **self._data.url_params, result=True)
            elif isinstance(pv, type):
                view_instance = pv(self._data, **self._data.url_params)
                view = self.__check_async(view_instance.build, result=True)
            else:
                view = pv

            view.route = route

            if self._can_pop_supported and route != self.__route_init and view.confirm_pop is None:
                view.can_pop = False
                view.confirm_pop = self._data.confirm_pop

            if pagesy.cache:
                self.__history_pages[route] = view

        # Run dynamic control if present
        dyn = self._data._dynamic_control.get(route)
        if dyn:
            for control, func_update in dyn:
                self.__check_async(func_update, control, result=True)

        # add view to the page and update it
        self.__manage_dynamic_appbar(route, view.appbar, self._can_pop_supported, pagesy.clear)
        page_views.append(view)
        self._data.history_routes.append((route, pagesy.index))
        page.update()

        # After-request middlewares
        if self._middlewares_after:
            for middleware in self._middlewares_after:
                self.__check_async(middleware.after_request)

        if pagesy._valid_middlewares_request():
            for middleware in pagesy._middlewares_request:
                self.__check_async(middleware.after_request)

    def __manage_dynamic_appbar(
        self, route: str, appbar: AppBar, can_pop: bool = False, clear: bool = False
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

        if can_pop and appbar.automatically_imply_leading:
            appbar.leading = IconButton(Icons.ARROW_BACK, on_click=self._data.go_back())
        elif not appbar.automatically_imply_leading and self.__automatically_imply_leading:
            appbar.automatically_imply_leading = True

    def __pop_supported(self, route: str) -> Union[View, None]:
        """Pop the view from the page if it is supported"""

        if not hasattr(self, "_can_pop_supported"):
            self._can_pop_supported = hasattr(View(), "can_pop")

        view = None

        if route == self.__route_init:
            self._data.history_routes.clear()

        if self._can_pop_supported:
            self.__page.views.clear()
            view = self.__history_pages.get(route)
        else:
            # support for flet < v0.28.0
            plat = self.__page.platform

            if plat not in (PagePlatform.ANDROID, PagePlatform.IOS):
                view = self.__history_pages.get(route)
            elif route == self.__route_init:
                self.__page.views.clear()

            # Keep only last view on stack
            if len(self.__page.views) > 1:
                self.__page.views.pop()

        return view

    def __reload_datasy(
        self,
        pagesy: Pagesy,
        url_params: Dict[str, Any] = dict(),
    ):
        """Update `datasy` values when switching between pages."""
        self.__page.title = pagesy.title

        if not pagesy.share_data:
            self._data.share.clear()
        if self.__on_Keyboard:
            self._data.on_keyboard_event.clear()

        self._data.url_params = url_params
        self._data.route = pagesy.route

    def __execute_middleware(
        self, pagesy: Pagesy, url_params: Dict[str, Any], middleware_list: Middleware
    ) -> bool:
        if not middleware_list:
            return False

        self.__reload_datasy(pagesy, url_params)

        try:
            for middleware in middleware_list:
                res = (
                    self.__check_async(middleware.before_request, result=True)
                    if isinstance(middleware, MiddlewareRequest)
                    else self.__check_async(middleware, self._data, result=True)
                )

                if self._handle_middleware_result(res):
                    return True

            return False

        except Exception as e:
            raise MidlewareError(e)

    def _handle_middleware_result(self, result):
        """Helper method to handle middleware results"""
        if not result:
            return False

        if isinstance(result, Redirect):
            self._go(result.route)
            return True

        return False

    def _go(self, route: Union[str, int], use_route_change: bool = False, use_reload: bool = False):
        """method to go to the route, if the route is not found, it will return a 404 page."""
        pg_404 = True

        for page in self._pages:
            if isinstance(route, int):
                if page.index != route:
                    continue
                route = page.route

            route_match = self._verify_url(page.route, route, page.custom_params)

            if route_match is None:
                continue

            pg_404 = False

            try:
                if page.protected_route:
                    if not self.__check_protected_route_optimized(
                        page, route, route_match, use_route_change, use_reload
                    ):
                        return
                    break

                if self.__run_middlewares_optimized(
                    route, route_match, page, use_route_change, use_reload
                ):
                    break

            except Exception as e:
                raise RouteError(e)

        if pg_404:
            self._handle_404_case(route, use_route_change, use_reload)

    def __check_protected_route_optimized(
        self, page, route, route_match, use_route_change, use_reload
    ):
        """Optimized protected route checker"""
        if self.__route_login is None:
            raise AssertionError("Configure the route of the login page in Flet-Easy class")

        try:
            auth = self.__check_async(self._config_login, self._data, result=True)
            if not auth:
                self._go(self.__route_login)
                return False

            self.__reload_datasy(page, route_match)
            self._navigate(route, page, use_route_change, use_reload)
            return True
        except Exception as e:
            raise LoginRequiredError(
                "use async methods in the function decorated by 'login', to avoid conflicts.", e
            )

    def __run_middlewares_optimized(self, route, route_match, page, use_route_change, use_reload):
        """Optimized middleware runner"""
        if self._middlewares and self.__execute_middleware(page, route_match, self._middlewares):
            return True

        if page.middleware and self.__execute_middleware(page, route_match, page.middleware):
            return True

        self.__reload_datasy(page, route_match)
        self._navigate(route, page, use_route_change, use_reload)
        return True

    def _navigate(self, route, page, use_route_change, use_reload):
        """Unified navigation handler"""
        if use_route_change:
            self._view_append(route, page)
        else:
            if self.__page.route != route or use_reload:
                self.__pagesy = page
            self.__page.go(route)

    def _handle_404_case(self, route, use_route_change, use_reload):
        """Optimized 404 handler"""
        page = self._page_404 or Pagesy(route, self.__view_404, "Flet-Easy 404")
        if page.route is None:
            page.route = route

        self.__reload_datasy(page)
        self._navigate(page.route, page, use_route_change, use_reload)

    @classmethod
    def __compile_pattern(cls, pattern_parts: list[str]) -> Pattern[str]:
        pattern_key = "/".join(pattern_parts)
        if pattern_key not in cls.__compiled_patterns_cache:
            cls.__compiled_patterns_cache[pattern_key] = compile(f"^/{pattern_key}/?$")
        return cls.__compiled_patterns_cache[pattern_key]

    @classmethod
    def _verify_url(
        cls,
        url_pattern: str,
        url: str,
        custom_types: Optional[Dict[str, Callable[[str], Optional[bool]]]] = None,
    ) -> Optional[Dict[str, Optional[bool]]]:
        combined_patterns = {
            **TYPE_PATTERNS,
            **{k: (compile(r"[^/]+"), v) for k, v in (custom_types or {}).items()},
        }

        segments: list[Tuple[str, Callable[[str], Optional[bool]]]] = []
        pattern_parts: list[str] = []
        type_patterns: list[str] = []

        for segment in url_pattern.strip("/").split("/"):
            try:
                if segment == "":
                    continue

                if segment[0] in "<{" and segment[-1] in ">}":
                    name, type_ = (
                        segment[1:-1].split(":", 1) if ":" in segment else (segment[1:-1], "str")
                    )
                    type_patterns.append(type_)
                    regex_part, parser = combined_patterns[type_]
                    pattern_parts.append(f"({regex_part.pattern})")
                    segments.append((name, parser))
                else:
                    pattern_parts.append(escape(segment))
            except KeyError as e:
                raise ValueError(f"Unrecognized data type: {e}")

        if custom_types and type_ not in custom_types:
            raise ValueError(f"A custom data type is not being used: {custom_types.keys()}")

        pattern = cls.__compile_pattern(pattern_parts)
        match = pattern.fullmatch(url)
        if not match:
            return None

        result = {name: parser(match.group(i + 1)) for i, (name, parser) in enumerate(segments)}

        return None if None in result.values() else result

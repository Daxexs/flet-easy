import re
from inspect import iscoroutinefunction
from re import Pattern, compile, escape
from typing import Any, Callable, Dict, List, Optional, Tuple

from flet import ControlEvent, KeyboardEvent, Page, RouteChangeEvent, View

from flet_easy.datasy import Datasy
from flet_easy.exceptions import LoginRequiredError, MidlewareError, RouteError
from flet_easy.extra import TYPE_PATTERNS, Msg, Redirect
from flet_easy.inheritance import Keyboardsy, Resizesy, Viewsy
from flet_easy.pagesy import Middleware, Pagesy
from flet_easy.view_404 import page_404_fs


class FletEasyX:
    __compiled_patterns_cache: Dict[str, re.Pattern[str]] = {}

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        config_login: Callable[[Datasy], bool],
        pages: List[Pagesy],
        page_404: Pagesy,
        view_data: Callable[[Datasy], Viewsy],
        view_config: Callable[[Datasy], None],
        config_event_handler: Callable[[Datasy], None],
        on_resize: bool,
        on_Keyboard: bool,
        secret_key: str,
        auto_logout: bool,
        middleware: Middleware,
    ):
        self.__page = page
        self.__page_on_keyboard = Keyboardsy()
        self.__page_on_resize = Resizesy(self.__page)

        self.__route_init = route_init
        self.__route_login = route_login
        self.__config_login = config_login
        self.__on_resize = on_resize
        self.__on_Keyboard = on_Keyboard
        self.__middlewares = middleware
        # ----
        self.__pages = pages
        self.__view_404 = page_404_fs
        self.__page_404 = page_404
        self.__view_data = view_data
        self.__view_config = view_config
        self.__config_event = config_event_handler
        self.__pagesy: Pagesy = None

        self.__data = Datasy(
            page=self.__page,
            route_prefix="" if route_prefix is None else route_prefix,
            route_init=self.__route_init,
            route_login=self.__route_login,
            secret_key=secret_key,
            auto_logout=auto_logout,
            page_on_keyboard=self.__page_on_keyboard,
            page_on_resize=self.__page_on_resize,
            go=self._go,
        )
        self.__data.view = self.__view_data_config() if self.__view_data is not None else None
        if self.__route_login is not None:
            self.__data._create_login()

    # ----------- Supports async
    def __route_change(self, e: RouteChangeEvent):
        if self.__pagesy is None:
            if e.route == "/" and self.__route_init != "/":
                return self.__page.go(self.__route_init)

            self._go(e.route, True)
        else:
            self._view_append(e.route, self.__pagesy)
            self.__pagesy = None

    def __view_pop(self, e):
        if len(self.__data.history_routes) > 1:
            self.__data.history_routes.pop()
            self._go(self.__data.history_routes.pop())

    async def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.e = e

    def __add_configuration_start(self):
        """Add general settings to the pages."""
        if self.__view_config:
            if iscoroutinefunction(self.__view_config):
                self.__page.run_task(self.__view_config, self.__page).result()
            else:
                self.__view_config(self.__page)

        if self.__config_event:
            if iscoroutinefunction(self.__config_event):
                self.__page.run_task(self.__config_event, self.__data).result()
            else:
                self.__config_event(self.__data)

    def __disconnect(self, e):
        if self.__data._login_done and self.__page.web:
            self.__page.pubsub.send_others_on_topic(
                self.__page.client_ip,
                Msg("updateLoginSessions", value=self.__data._login_done),
            )

    # -- initialization

    def run(self):
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init

        """ Add custom events """
        self.__add_configuration_start()

        """ Executing charter events """
        self.__page.on_route_change = self.__route_change
        self.__page.on_view_pop = self.__view_pop
        self.__page.on_error = lambda e: print("Page error:", e.data)
        self.__page.on_disconnect = self.__disconnect

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize
        if self.__on_Keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard

        self._go(self.__page.route, use_reload=True)

    # ---------------------------[Route controller]-------------------------------------
    def __view_data_config(self):
        """Add the `View` configuration, to reuse on every page."""
        if iscoroutinefunction(self.__view_data):
            return self.__page.run_task(self.__view_data, self.__data).result()
        else:
            return self.__view_data(self.__data)

    def _view_append(self, route: str, pagesy: Pagesy):
        """Add a new page and update it."""

        self.__page.views.clear()

        if not pagesy.clear and len(self.__data.history_routes) > 0:
            self.__page.views.append(View())

        if callable(pagesy.view) and not isinstance(pagesy.view, type):
            view = (
                self.__page.run_task(pagesy.view, self.__data, **self.__data.url_params).result()
                if iscoroutinefunction(pagesy.view)
                else pagesy.view(self.__data, **self.__data.url_params)
            )
        elif isinstance(pagesy.view, type):
            view_class = pagesy.view(self.__data, **self.__data.url_params)
            view = (
                self.__page.run_task(view_class.build).result()
                if iscoroutinefunction(view_class.build)
                else view_class.build()
            )
        view.route = route
        self.__page.views.append(view)
        self.__data.history_routes.append(route)
        self.__page.update()

    def __reload_datasy(
        self,
        pagesy: Pagesy,
        url_params: Dict[str, Any] = dict(),
    ):
        """Update `datasy` values when switching between pages."""
        self.__page.title = pagesy.title

        if not pagesy.share_data:
            self.__data.share.clear()
        if self.__on_Keyboard:
            self.__data.on_keyboard_event.clear()

        self.__data.url_params = url_params
        self.__data.route = pagesy.route

    def __execute_middleware(
        self, pagesy: Pagesy, url_params: Dict[str, Any], middleware_list: Middleware
    ):
        if middleware_list is None:
            return False

        for middleware in middleware_list:
            self.__reload_datasy(pagesy, url_params)
            res_middleware = (
                self.__page.run_task(middleware, self.__data).result()
                if iscoroutinefunction(middleware)
                else middleware(self.__data)
            )
            if res_middleware is None:
                continue

            if isinstance(res_middleware, Redirect):
                self._go(res_middleware.route)
                return True

            if not res_middleware:
                raise MidlewareError(
                    "Ocurrió un error en una función middleware. Usa los métodos para redirigir (data.redirect) o devolver False."
                )

    def __run_middlewares(
        self,
        route: str,
        middleware: Middleware,
        url_params: Dict[str, Any],
        pagesy: Pagesy,
        use_route_change: bool,
        use_reload: bool,
    ):
        """Controla los middleware de la aplicación en general y en cada una de las páginas."""

        if self.__execute_middleware(pagesy, url_params, middleware):
            return True

        if self.__execute_middleware(pagesy, url_params, pagesy.middleware):
            return True

        self.__reload_datasy(pagesy, url_params)
        if use_route_change:
            self._view_append(route, pagesy)
        else:
            if self.__page.route != route or use_reload:
                self.__pagesy = pagesy
            self.__page.go(route)

        return True

    def _go(self, route: str, use_route_change: bool = False, use_reload: bool = False):
        pg_404 = True

        for page in self.__pages:
            route_math = self._verify_url(page.route, route, page.custom_params)
            if route_math is not None:
                pg_404 = False
                try:
                    if page.protected_route:
                        assert (
                            self.__route_login is not None
                        ), "Configure the route of the login page, in the Flet-Easy class in the parameter (route_login)"

                        if iscoroutinefunction(self.__config_login):
                            try:
                                auth = self.__page.run_task(
                                    self.__config_login, self.__data
                                ).result()
                            except Exception as e:
                                raise LoginRequiredError(
                                    "Use async methods in the function decorated by 'login', to avoid conflicts.",
                                    e,
                                )
                        else:
                            auth = self.__config_login(self.__data)

                        if auth:
                            self.__reload_datasy(page, route_math)

                            if use_route_change:
                                self._view_append(route, page)

                            else:
                                if self.__page.route != route or use_reload:
                                    self.__pagesy = page
                                self.__page.go(route)

                        else:
                            self._go(self.__route_login)

                        break
                    else:
                        if self.__run_middlewares(
                            route=route,
                            middleware=self.__middlewares,
                            url_params=route_math,
                            pagesy=page,
                            use_route_change=use_route_change,
                            use_reload=use_reload,
                        ):
                            break
                except Exception as e:
                    raise RouteError(e)
        if pg_404:
            page = self.__page_404 or Pagesy(route, self.__view_404, "Flet-Easy 404")

            if page.route is None:
                page.route = route

            self.__reload_datasy(page)

            if use_route_change:
                self._view_append(page.route, page)
            else:
                if self.__page.route != route or use_reload:
                    self.__pagesy = page
                self.__page.go(page.route)

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

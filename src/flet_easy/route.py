from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, List

from flet import ControlEvent, KeyboardEvent, Page, RouteChangeEvent
from parse import parse

from flet_easy.datasy import Datasy
from flet_easy.extra import Msg, Redirect
from flet_easy.inheritance import Keyboardsy, Resizesy, Viewsy
from flet_easy.pagesy import Middleware, Pagesy
from flet_easy.view_404 import ViewError


class FletEasyX:
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
        self.__view_404 = ViewError(route_init)
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
            login_async=iscoroutinefunction(self.__config_login),
            go=self._go,
        )
        self.__data.view = (
            self.__page.run_task(self.__view_data_config).result()
            if self.__view_data is not None
            else None
        )
        if self.__route_login is not None:
            self.__data._create_login()

    # ----------- Supports async
    def __route_change(self, e: RouteChangeEvent):
        if not self.__data._check_event_router:
            route = (
                self.__data.route_init
                if self.__data.route_init != "/" and e.route == "/"
                else e.route
            )
            self._go(route)
        self.__data._check_event_router = False

    def __view_pop(self, e):
        if self.__page.views[-1].route == self.__page.views[-2].route:
            self.__page.views.pop()
        self.__page.views.pop()
        self._go(self.__page.views[-1].route)

    async def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.e = e

    async def __add_configuration_start(self):
        """Add general settings to the pages."""
        if self.__view_config:
            if iscoroutinefunction(self.__view_config):
                await self.__view_config(self.__page)
            else:
                self.__view_config(self.__page)

        if self.__config_event:
            if iscoroutinefunction(self.__config_event):
                await self.__config_event(self.__data)
            else:
                self.__config_event(self.__data)

    def __disconnect(self, e):
        if self.__data._login_done:
            self.__page.pubsub.send_others_on_topic(
                self.__page.client_ip,
                Msg("updateLoginSessions", value=self.__data._login_done),
            )

    # -- initialization

    def run(self):
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init

        if len(self.__page.views) == 1:
            self.__page.views.clear()

        """ Add custom events """
        self.__page.run_task(self.__add_configuration_start)

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

        self._go(self.__page.route)

    # ---------------------------[Route controller]-------------------------------------
    async def __view_data_config(self):
        """Add the `View` configuration, to reuse on every page."""
        if iscoroutinefunction(self.__view_data):
            return await self.__view_data(self.__data)
        else:
            return self.__view_data(self.__data)

    async def _view_append(self, route: str):
        """Add a new page and update it."""
        view = (
            await self.__pagesy.view(self.__data, **self.__data.url_params)
            if iscoroutinefunction(self.__pagesy.view)
            else self.__pagesy.view(self.__data, **self.__data.url_params)
        )

        view.route = route
        self.__page.views.append(view)
        self.__page.route = route
        self.__page.query()
        self.__page.update()

    def __reload_datasy(self, url_params: Dict[str, Any] = None):
        """Update `datasy` values when switching between pages."""
        self.__page.title = self.__pagesy.title

        if self.__pagesy.clear:
            self.__page.views.clear()
        if not self.__pagesy.share_data:
            self.__data.share.clear()

        self.__data.url_params = url_params
        self.__data.route = self.__pagesy.route

    def __run_middlewares(self, route: str, middleware: Middleware, url_params: Dict[str, Any]):
        """It controls the middleware of the app in general and in each of the pages (both can be used)."""
        _middlewares = middleware
        _middlewares_two = False

        while True:
            if _middlewares is not None:
                for middleware in _middlewares:
                    self.__reload_datasy(url_params)
                    res_middleware = (
                        self.__page.run_task(middleware, self.__data).result()
                        if iscoroutinefunction(middleware)
                        else middleware(self.__data)
                    )
                    if res_middleware is None:
                        continue

                    if isinstance(res_middleware, Redirect):
                        self._go(res_middleware.route)
                        return False

                    if not res_middleware:
                        raise Exception(
                            "A middleware function has occurred, use the methods to return (data.redirect) or not return False."
                        )
            if self.__pagesy.middleware is None or _middlewares_two:
                self.__reload_datasy(url_params)
                self.__page.run_task(self._view_append, route)
                return False
            else:
                _middlewares = self.__pagesy.middleware
                _middlewares_two = True

    def __process_route(self, custom_params: Dict[str, Callable[[], bool]], path: str, route: str):
        if custom_params is None:
            route_math = parse(route, path)
            return [route_math, route_math]

        else:
            try:
                route_math = parse(route, path, custom_params)
                route_check = (
                    all(
                        valor is not False and valor is not None
                        for valor in dict(route_math.named).values()
                    )
                    if route_math
                    else route_math
                )
                return [route_math, route_check]

            except Exception as e:
                raise Exception(
                    f"The url parse has failed, check the url -> ({route}) parameters for correctness. Error-> {e}"
                )

    def _go(self, route: str):
        pg_404 = True
        self.__data._check_event_router = True
        self.__data.on_keyboard_event.clear()
        path = self.__route_init if route == "/" else route

        for page in self.__pages:
            route_math, route_check = self.__process_route(page.custom_params, path, page.route)
            if route_check:
                pg_404 = False
                self.__pagesy = page
                try:
                    if page.protected_route:
                        if iscoroutinefunction(self.__config_login):
                            try:
                                auth = self.__page.run_task(
                                    self.__config_login, self.__data
                                ).result()
                            except Exception as e:
                                raise Exception(
                                    "Use async methods in the function decorated by 'login', to avoid conflicts.",
                                    e,
                                )
                        else:
                            auth = self.__config_login(self.__data)
                        if auth:
                            self.__reload_datasy(route_math.named)
                            self.__page.run_task(self._view_append, route).result()
                            break
                        else:
                            self._go(self.__route_login)
                            break
                    else:
                        response = self.__run_middlewares(
                            route=route, middleware=self.__middlewares, url_params=route_math.named
                        )
                        if not response:
                            break
                except Exception as e:
                    raise Exception(e)
        if pg_404:
            if self.__page_404:
                self.__pagesy = self.__page_404
                self.__page.route = self.__page_404
                self.__reload_datasy()
                self.__page.views.append(self.__page_404.view(self.__page))

            else:
                self.__page.route = self.__view_404.route
                self.__page.views.append(self.__view_404.view(self.__page))
            self.__page.query()
            self.__page.update()

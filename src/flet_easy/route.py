from flet import Page, RouteChangeEvent, KeyboardEvent, ControlEvent, View
from .inheritance import Keyboardsy, Resizesy, Pagesy, Datasy, Viewsy
from .view_404 import ViewError
from typing import Callable
from inspect import iscoroutinefunction
from parse import parse


class FletEasyX:
    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        config_login: Callable,
        pages: list[Pagesy],
        page_404: Callable,
        view_data: Callable,
        view_config: Callable,
        config_event_handler: Callable,
        on_resize: bool,
        on_Keyboard: bool,
    ):
        self.__page = page
        self.__page_on_keyboard = Keyboardsy()
        self.__page_on_resize = Resizesy(self.__page)

        self.__route_init = route_init
        self.__route_login = route_login
        self.__config_login = config_login
        self.__on_resize = on_resize
        self.__on_Keyboard = on_Keyboard
        # ----
        self.__pages = pages

        self.__data = Datasy(
            "" if route_prefix is None else route_prefix,
            self.__route_init,
            self.__route_login,
        )

        self.__view_404 = ViewError()
        self.__page_404: Pagesy = page_404
        self.__view_data: Viewsy = view_data
        self.__view_config: Callable = view_config
        self.__config_event: Callable = config_event_handler

        self.__pubsub_user: bool = True if self.__route_login is not None else False

    # -----------
    def __route_change(self, route: RouteChangeEvent):
        pg_404 = True
        self.__page_on_resize.clear()
        self.__page_on_keyboard.clear()

        for page in self.__pages:
            if page.custom_params is None:
                route_math = parse(page.route, route.route)
                route_check = route_math
            else:
                try:
                    route_math = parse(page.route, route.route, page.custom_params)

                    if route_math:
                        route_check = all(
                            valor is not False and valor is not None
                            for valor in dict(route_math.named).values()
                        )
                    else:
                        route_check = route_math
                except:  # noqa: E722
                    break

            if route_check:
                pg_404 = False
                try:
                    if page.protected_route:
                        if self.__config_login(self.__page):
                            if page.clear:
                                self.__page.views.clear()
                            self.__add_events_params(page.view, route_math.named)
                            break
                        else:
                            self.__page.go(self.__route_login)
                            break

                    else:
                        if page.clear:
                            self.__page.views.clear()
                        self.__add_events_params(page.view, route_math.named)
                        break

                except Exception as e:
                    raise e

        if pg_404:
            if self.__page_404:
                if self.__page_404.clear:
                    self.__page.views.clear()
                if self.__page_404.route:
                    self.__page.route = self.__page_404.route

                self.__add_events_params(self.__page_404.view)
            else:
                self.__page.route = "/Flet-Easy-404"
                self.__view_404.route_index = self.__route_init
                self.__page.views.append(self.__view_404.view(self.__page))
                self.__page.update()

    def __add_events_params(self, view: View, url_params: dict = None):
        self.__data.page = self.__page
        self.__data.on_keyboard_event = self.__page_on_keyboard
        self.__data.on_resize = self.__page_on_resize
        self.__data.url_params = url_params
        self.__data.view: Viewsy = (
            self.__view_data(self.__data) if self.__view_data else None
        )

        if url_params:
            self.__page.views.append(view(self.__data, **url_params))
        else:
            self.__page.views.append(view(self.__data))

        if self.__pubsub_user:
            self.__data._create_login()
            self.__pubsub_user = False
        self.__page.update()

    def __view_pop(self, e):
        self.__page.views.pop()
        top_view = self.__page.views[-1]
        self.__page.go(top_view.route)

    def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.page = self.__page
        self.__page_on_resize.width = float(e.control.width)
        self.__page_on_resize.height = float(e.control.height)

        if self.__page_on_resize.add_controls_f is not None:
            self.__page_on_resize._run()

    # -- initialization

    def run(self):
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init
        if self.__view_config:
            self.__view_config(self.__page)
        if len(self.__page.views) == 1:
            self.__page.views.clear()

        """ Add custom events """
        if self.__config_event:
            self.__config_event(self.__page)

        self.__page.on_route_change = self.__route_change
        self.__page.on_view_pop = self.__view_pop
        self.__page.on_error = lambda e: print("Page error:", e.data)

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize
        if self.__on_Keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard

        self.__page.go(self.__page.route)

    # ---- Async ----------------------------------------------------------------
    async def __route_change_async(self, route: RouteChangeEvent):
        pg_404 = True
        self.__page_on_resize.clear()
        self.__page_on_keyboard.clear()

        for page in self.__pages:
            if page.custom_params is None:
                route_math = parse(page.route, route.route)
                route_check = route_math
            else:
                try:
                    route_math = parse(page.route, route.route, page.custom_params)

                    if route_math:
                        route_check = all(
                            valor is not False and valor is not None
                            for valor in dict(route_math.named).values()
                        )
                    else:
                        route_check = route_math
                except:  # noqa: E722
                    break

            if route_check:
                pg_404 = False
                try:
                    if page.protected_route:
                        assert self.__config_login, f"The function -> ({page.view.__name__}), which is being decorated has path protection enabled, but it is not configured yet. To configure it use the 'FletEasy' decorator (login)."

                        if await self.__config_login(self.__page):
                            if page.clear:
                                self.__page.views.clear()
                            await self.__add_events_params_async(
                                page.view, route_math.named
                            )
                            break
                        else:
                            await self.__page.go_async(self.__route_login)
                            break

                    else:
                        if page.clear:
                            self.__page.views.clear()
                        await self.__add_events_params_async(
                            page.view, route_math.named
                        )
                        break

                except Exception as e:
                    raise e

        if pg_404:
            if self.__page_404:
                if self.__page_404.clear:
                    self.__page.views.clear()
                if self.__page_404.route:
                    self.__page.route = self.__page_404.route

                await self.__add_events_params_async(self.__page_404.view)
            else:
                self.__page.route = "/Flet-Easy-404"
                self.__view_404.route_index = self.__route_init
                self.__page.views.append(await self.__view_404.view_async(self.__page))
                await self.__page.update_async()

    async def __add_events_params_async(self, view: View, url_params: dict = None):
        self.__data.page = self.__page
        self.__data.on_keyboard_event = self.__page_on_keyboard
        self.__data.on_resize = self.__page_on_resize
        self.__data.url_params = url_params
        self.__data.view: Viewsy = (
            await self.__view_data(self.__data) if self.__view_data else None
        )

        if iscoroutinefunction(view):
            if url_params:
                self.__page.views.append(await view(self.__data, **url_params))
            else:
                self.__page.views.append(await view(self.__data))
        else:
            self.__page.views.append(view(self.__data, **url_params))

        if self.__pubsub_user:
            await self.__data._create_login_async()
            self.__pubsub_user = False
        await self.__page.update_async()

    # ---- event handlers --------------------------------
    async def __view_pop_async(self, e):
        self.__page.views.pop()
        top_view = self.__page.views[-1]
        await self.__page.go_async(top_view.route)

    async def __on_keyboard_async(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls_async()

    async def __page_resize_async(self, e: ControlEvent):
        self.__page_on_resize.page = self.__page
        self.__page_on_resize.width = float(e.control.width)
        self.__page_on_resize.height = float(e.control.height)

        if self.__page_on_resize.add_controls_f is not None:
            await self.__page_on_resize._run_async()

    # -- initialize

    async def run_async(self):
        if self.__route_init != "/" and self.__page.route == "/":
            self.__page.route = self.__route_init
        if self.__view_config:
            await self.__view_config(self.__page)
        if len(self.__page.views) == 1:
            self.__page.views.clear()

        """ Add custom events """
        if self.__config_event:
            await self.__config_event(self.__page)

        self.__page.on_route_change = self.__route_change_async
        self.__page.on_view_pop = self.__view_pop_async
        self.__page.on_error = lambda e: print("Page error:", e.data)

        """ activation of charter events """
        if self.__on_resize:
            self.__page.on_resize = self.__page_resize_async
        if self.__on_Keyboard:
            self.__page.on_keyboard_event = self.__on_keyboard_async

        await self.__page.go_async(self.__page.route)

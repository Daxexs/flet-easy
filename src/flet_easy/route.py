from inspect import iscoroutinefunction
from typing import Callable

from flet import ControlEvent, KeyboardEvent, Page, RouteChangeEvent, View
from parse import parse

from flet_easy.datasy import Datasy
from flet_easy.extra import Msg
from flet_easy.inheritance import Keyboardsy, Pagesy, Resizesy, Viewsy
from flet_easy.view_404 import ViewError


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
        secret_key: str,
        auto_logout: bool,
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
            self.__page,
            "" if route_prefix is None else route_prefix,
            self.__route_init,
            self.__route_login,
            secret_key,
            auto_logout,
            iscoroutinefunction(self.__config_login),
        )

        self.__view_404 = ViewError(route_init)
        self.__page_404: Pagesy = page_404
        self.__view_data: Viewsy = view_data
        self.__view_config: Callable = view_config
        self.__config_event: Callable = config_event_handler

        self.__pubsub_user: bool = self.__route_login is not None

    # ----------- Supports async
    def __route_change(self, route: RouteChangeEvent):
        pg_404 = True
        self.__page_on_keyboard.clear()
        path = self.__route_init if route.route == "/" else route.route

        for page in self.__pages:
            if page.custom_params is None:
                route_math = parse(page.route, path)
                route_check = route_math
            else:
                try:
                    route_math = parse(page.route, path, page.custom_params)

                    route_check = all(valor is not False and valor is not None for valor in dict(route_math.named).values()) if route_math else route_math

                except Exception as e:
                    raise Exception(f"The url parse has failed, check the url -> ({route.route}) parameters for correctness. Error-> {e}")

            if route_check:
                pg_404 = False
                try:
                    if page.protected_route:
                        if iscoroutinefunction(self.__config_login):
                            try:
                                auth = self.__page.run_task(self.__config_login, self.__data).result()
                            except TimeoutError as e:
                                raise Exception(
                                    "Use async methods in the function decorated by 'login', to avoid conflicts.",
                                    e,
                                )
                        else:
                            auth = self.__config_login(self.__data)

                        assert auth, "Use async methods in the function decorated by 'login', to avoid conflicts."

                        if auth:
                            if page.clear:
                                self.__page.views.clear()
                            if not page.share_data:
                                self.__data.share.clear()
                            self.__page.run_task(
                                self.__add_events_params,
                                page.view,
                                page.title,
                                route_math.named,
                            )
                            break
                        else:
                            self.__page.go(self.__route_login)
                            break

                    else:
                        if page.clear:
                            self.__page.views.clear()
                        if not page.share_data:
                            self.__data.share.clear()
                        self.__page.run_task(
                            self.__add_events_params,
                            page.view,
                            page.title,
                            route_math.named,
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

                self.__page.run_task(self.__add_events_params, self.__page_404.view, page.title)
            else:
                self.__page.views.append(self.__view_404.view(self.__page))
                self.__page.update()

    async def __add_events_params(self, view: View, title: str, url_params: dict = None):
        self.__data.on_keyboard_event = self.__page_on_keyboard
        self.__data.on_resize = self.__page_on_resize
        self.__data.url_params = url_params
        self.__data.page.title = title

        if iscoroutinefunction(self.__view_data):
            self.__data.view = await self.__view_data(self.__data)
        else:
            self.__data.view = self.__view_data(self.__data)

        if iscoroutinefunction(view):
            if url_params:
                self.__page.views.append(await view(self.__data, **url_params))
            else:
                self.__page.views.append(await view(self.__data))
        else:
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

    async def __on_keyboard(self, e: KeyboardEvent):
        self.__page_on_keyboard.call = e
        if self.__page_on_keyboard._controls():
            await self.__page_on_keyboard._run_controls()

    def __page_resize(self, e: ControlEvent):
        self.__page_on_resize.e = e

    async def __add_configuration_start(self):
        if self.__view_config:
            if iscoroutinefunction(self.__view_config):
                await self.__view_config(self.__page)
            else:
                self.__page.run_thread(self.__view_config, self.__page)

        if self.__config_event:
            if iscoroutinefunction(self.__view_config):
                await self.__config_event(self.__page)
            else:
                self.__page.run_thread(self.__config_event, self.__page)

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

        self.__page.go(self.__page.route)

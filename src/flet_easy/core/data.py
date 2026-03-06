from collections import deque
from typing import Any, Callable, Dict, List, Tuple, Union

from flet import Control, ControlEvent, Page, View, ViewPopEvent

from flet_easy.core.models import Redirect
from flet_easy.logger import get_logger
from flet_easy.migration import NEW_FLET_VERSION
from flet_easy.security.auth import AuthMixin
from flet_easy.security.config import SecretKey
from flet_easy.ui.controls import (
    Keyboardsy,
    Resizesy,
    SessionStorageEdit,
    SharedPreferencesEdit,
    Viewsy,
)

_logger = get_logger("Datasy")


class Datasy(AuthMixin):
    """The decorated function will always receive a parameter which is `data` (can be any name), which will make an object of type `Datasy` of `Flet-Easy`.

    This class has the following attributes, in order to access its data:

    * `page` : We get the values of the page provided by `Flet`.
    * `url_params` : We obtain a dictionary with the values passed through the url.
    * `view` : Get a `View` object from `Flet`, previously configured with the `view` decorator of `Flet-Easy`.
    * `route_prefix` : Value entered in the `FletEasy` class parameters to create the app object.
    * `route_init` : Value entered in the `FletEasy` class parameters to create the app object.
    * `route_login` : Value entered in the `FletEasy` class parameters to create the app object.
    ---
    * `share` : It is used to be able to store and to obtain values in the client session.
    * `on_keyboard_event` : get event values to use in the page.
    * `on_resize` : get event values to use in the page.
    * `logout` : method to close sessions of all sections in the browser (client storage).
    * `login` : method to create sessions of all sections in the browser (client storage).
    * `go` / `go_route`: Method to change the application path.
    * `go_back` : Method to go back to the previous route.
    * `go_navigation_bar` : Handles navigation bar changes.
    * `history_routes` : Get the history of the routes.
    * `route` : Route provided by the route event.
    * `redirect` : To redirect to a path before the page loads, it is used in middleware.
    * `page_reload` : Use this method to reload the page.
    * `dynamic_control` : Adds dynamic control to the page.
    * `confirm_pop` : Confirm pop view.
    """

    __slots__ = (
        "__page",
        "__url_params",
        "__view",
        "__route_prefix",
        "__route_init",
        "__route_login",
        "__share",
        "__on_keyboard_event",
        "__on_resize",
        "__route",
        "_run_go",
        "__history_routes",
        "_dynamic_control",
        "__secret_key",
        "__auto_logout",
        "__sleep",
        "_key_login",
        "_login_done",
        "_shared_preferences",
    )

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        secret_key: str,
        auto_logout: bool,
        page_on_keyboard: Keyboardsy,
        page_on_resize: Resizesy,
        go: Callable[[Union[str, int], bool], None] = None,
    ) -> None:
        self.__page: Page = page
        self.__url_params: Dict[str, Any] = None
        self.__view: Viewsy = None
        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        if NEW_FLET_VERSION:
            self.__share = SharedPreferencesEdit(prefix="fs-share:")
            self._shared_preferences = SharedPreferencesEdit()
        else:
            self.__share = SessionStorageEdit(page)
            self._shared_preferences = SessionStorageEdit(page)

        self.__on_keyboard_event = page_on_keyboard
        self.__on_resize: Resizesy = page_on_resize
        self.__route: str = None
        self._run_go = go
        self.__history_routes: deque[Tuple[str, int]] = deque()
        self._dynamic_control: Dict[str, List[Tuple[Control, Callable[[Control]], None]]] = {}

        self.__secret_key: SecretKey = secret_key
        self.__auto_logout: bool = auto_logout
        self._sleep_auth: int = 1
        self._key_login: str = None
        self._login_done: bool = False

        _logger.info(
            "Using SharedPreferences (Flet >= 0.80)"
            if NEW_FLET_VERSION
            else "Using SessionStorage (Flet < 0.80)"
        )

    @property
    def page(self) -> Page:
        return self.__page

    @page.setter
    def page(self, page: Page):
        self.__page = page

    @property
    def history_routes(self) -> deque[Tuple[str, int]]:
        return self.__history_routes

    @property
    def url_params(self) -> Dict[str, Any]:
        return self.__url_params

    @url_params.setter
    def url_params(self, url_params: Dict[str, Any]):
        self.__url_params = url_params

    @property
    def view(self) -> Union[Viewsy, View]:
        return self.__view

    @view.setter
    def view(self, view: Union[Viewsy, View]):
        self.__view = view

    @property
    def route_prefix(self) -> str:
        return self.__route_prefix

    @route_prefix.setter
    def route_prefix(self, route_prefix: str):
        self.__route_prefix = route_prefix

    @property
    def route_init(self) -> str:
        return self.__route_init

    @route_init.setter
    def route_init(self, route_init: str):
        self.__route_init = route_init

    @property
    def route_login(self) -> str:
        return self.__route_login

    @route_login.setter
    def route_login(self, route_login: str):
        self.__route_login = route_login

    @property
    def share(self) -> Union[SessionStorageEdit, SharedPreferencesEdit]:
        return self.__share

    # events
    @property
    def on_keyboard_event(self) -> Keyboardsy:
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, on_keyboard_event: object):
        self.__on_keyboard_event = on_keyboard_event

    @property
    def on_resize(self) -> Resizesy:
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, on_resize: object):
        self.__on_resize = on_resize

    @property
    def key_login(self) -> str:
        return self._key_login

    @property
    def auto_logout(self) -> bool:
        return self.__auto_logout

    @property
    def secret_key(self) -> SecretKey:
        return self.__secret_key

    @property
    def route(self) -> str:
        return self.__route

    @route.setter
    def route(self, route: str):
        self.__route = route

    """ Page go  """

    def go(self, route: str) -> Callable[[ControlEvent], None]:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""

        return lambda _=None: self.go_route(route)

    def go_route(self, route: Union[str, int]) -> None:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""

        async def _go_route():
            await self._run_go(route)

        self.page.run_task(_go_route)

    def go_navigation_bar(self, e: ControlEvent) -> None:
        """Handles navigation bar changes. Use this method in the on_change event of
        'ft.NavigationBar' or 'ft.CupertinoNavigationBar' controls."""

        async def _go_nav():
            route = e.control.selected_index
            await self._run_go(route)

        self.page.run_task(_go_nav)

    def redirect(self, route: str) -> Redirect:
        """Useful if you do not want to access a route that has already been sent."""
        return Redirect(route)

    def go_back(self, e: ControlEvent = None) -> None:
        """Go back to the previous route."""

        if len(self.history_routes) > 1:
            self.history_routes.pop()
            route, index = self.history_routes.pop()

            if index is not None:
                self.view.navigation_bar.selected_index = index

            async def _go_back():
                await self._run_go(route)

            self.page.run_task(_go_back)
        else:
            print("-> I can't go back! there is no history. ")

    def page_reload(self):
        """Use this method to reload the page, restores the default values of the page"""
        self._run_go(self.page.route, page_reload=True)

    def dynamic_control(self, control: Control, func_update: Callable[[Control], None]) -> None:
        """Adds dynamic control to the page, allowing real-time updates when caching is enabled on the page."""
        if self.page.route not in self._dynamic_control:
            self._dynamic_control[self.page.route] = [(control, func_update)]
        else:
            self._dynamic_control[self.page.route].append((control, func_update))

    def confirm_pop(self, e: ViewPopEvent) -> None:
        """Confirm pop view"""
        self.go_back()
        e.control.confirm_pop(False)

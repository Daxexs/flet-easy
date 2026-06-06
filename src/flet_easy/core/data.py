from collections import deque
from collections.abc import Awaitable
from typing import Any, Callable, Optional, Union

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
    """Core data object passed to route handlers in Flet-Easy.

    Provides access to the Flet `Page` instance, URL parameters, routing state,
    client storage, and authentication utilities.

    Attributes:
    * `page` : The active Flet `Page` instance.
    * `url_params` : A dictionary of parsed parameters from the current URL.
    * `view` : The `View` object configured by the `@app.view` decorator.
    * `route_prefix` : The configured application route prefix.
    * `route_init` : The initial application route.
    * `route_login` : The configured login route for protected endpoints.
    * `share` : Interface for storing and retrieving values in the client session.
    * `on_keyboard_event` : Contains keyboard event data if enabled.
    * `on_resize` : Contains window resize event data if enabled.
    * `logout` : Closes the active session in client storage.
    * `login` : Creates a new session in client storage.
    * `go` / `go_route`: Navigates to a new application route.
    * `go_back` : Navigates back to the previous route.
    * `go_navigation_bar` : Handles navigation bar index updates.
    * `history_routes` : History of visited routes in the current session.
    * `route` : The current application route.
    * `redirect` : Returns a `Redirect` object to bypass the current view (useful in middleware).
    * `page_reload` : Reloads the current route.
    * `dynamic_control` : Registers a dynamically updatable control for the current route.
    * `confirm_pop` : Triggers the `ViewPopEvent` manually.
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
        "_sleep_auth",
        "_key_login",
        "_login_done",
        "_shared_preferences",
        "_use_client_storage",
    )

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: Optional[str],
        secret_key: Optional[SecretKey],
        auto_logout: bool,
        page_on_keyboard: Keyboardsy,
        page_on_resize: Resizesy,
        go: Callable[..., Awaitable[None]],
    ) -> None:
        self.__page = page
        self.__url_params: dict[str, Any] = {}
        self.__view: Optional[Union[Viewsy, View]] = None
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
        self.__route: Optional[str] = None
        self._run_go = go
        self.__history_routes: deque[tuple[str, Optional[int]]] = deque()
        self._dynamic_control: dict[str, list[tuple[Control, Callable[[Control], None]]]] = {}

        self.__secret_key = secret_key
        self.__auto_logout: bool = auto_logout
        self._sleep_auth: int = 1
        self._key_login: Optional[str] = None
        self._login_done: bool = False
        # Cached once per session — storage API never changes at runtime
        self._use_client_storage: bool = hasattr(page, "client_storage")

        _logger.debug(
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
    def history_routes(self) -> deque[tuple[str, Optional[int]]]:
        return self.__history_routes

    @property
    def url_params(self) -> dict[str, Any]:
        return self.__url_params

    @url_params.setter
    def url_params(self, url_params: dict[str, Any]):
        self.__url_params = url_params

    @property
    def view(self) -> Optional[Union[Viewsy, View]]:
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
    def route_login(self) -> Optional[str]:
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
    def on_keyboard_event(self, on_keyboard_event: Keyboardsy):
        self.__on_keyboard_event = on_keyboard_event

    @property
    def on_resize(self) -> Resizesy:
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, on_resize: Resizesy):
        self.__on_resize = on_resize

    @property
    def key_login(self) -> Optional[str]:
        return self._key_login

    @property
    def auto_logout(self) -> bool:
        return self.__auto_logout

    @property
    def secret_key(self) -> Optional[SecretKey]:
        return self.__secret_key

    @property
    def route(self) -> Optional[str]:
        return self.__route

    @route.setter
    def route(self, route: str):
        self.__route = route

    """ Page go  """

    def go(self, route: str) -> Callable[[Any], None]:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""

        return lambda _=None: self.go_route(route)

    def go_route(self, route: Union[str, int]) -> None:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""
        self.page.run_task(self._run_go, route)

    def go_navigation_bar(self, e: ControlEvent) -> None:
        """Handles navigation bar changes. Use this method in the on_change event of
        'ft.NavigationBar' or 'ft.CupertinoNavigationBar' controls."""
        index = getattr(e.control, "selected_index", None)
        if index is not None:
            self.page.run_task(self._run_go, index)

    def redirect(self, route: str) -> Redirect:
        """Useful if you do not want to access a route that has already been sent."""
        return Redirect(route)

    def go_back(self, e: Optional[ControlEvent] = None) -> None:
        """Go back to the previous route."""

        if len(self.history_routes) > 1:
            self.history_routes.pop()
            route, index = self.history_routes.pop()

            if index is not None and self.view and self.view.navigation_bar:
                self.view.navigation_bar.selected_index = index

            self.page.run_task(self._run_go, route)
        else:
            _logger.warning("go_back: called with no navigation history to go back to.")

    def page_reload(self) -> None:
        """Use this method to reload the page, restores the default values of the page"""
        self.page.run_task(self._run_go, self.page.route, page_reload=True)

    def dynamic_control(self, control: Control, func_update: Callable[[Control], None]) -> None:
        """Adds dynamic control to the page, allowing real-time updates when caching is enabled on the page."""
        self._dynamic_control.setdefault(self.page.route, []).append((control, func_update))

    def confirm_pop(self, e: ViewPopEvent) -> None:
        """Confirm pop view"""
        self.go_back()
        if hasattr(e.view, "confirm_pop"):
            _ = getattr(e.view, "confirm_pop")(False)  # noqa: B009

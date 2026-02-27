from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Tuple, Union

from flet import Control, ControlEvent, Page, View, ViewPopEvent

from flet_easy.core.job import Job
from flet_easy.core.models import Msg, Redirect
from flet_easy.exceptions import ConfigurationError, LoginError, SecretKeyError
from flet_easy.logger import get_logger
from flet_easy.migration import NEW_FLET_VERSION, go_page
from flet_easy.security.config import (
    SecretKey,
    _decode_payload,
    encode_verified,
)
from flet_easy.ui.controls import (
    Keyboardsy,
    Resizesy,
    SessionStorageEdit,
    SharedPreferencesEdit,
    Viewsy,
)

_logger = get_logger("Datasy")


class Datasy:
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
        "__go",
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
        self.__share = (
            SharedPreferencesEdit(prefix="fs-share:")
            if NEW_FLET_VERSION
            else SessionStorageEdit(page)
        )
        self.__on_keyboard_event = page_on_keyboard
        self.__on_resize: Resizesy = page_on_resize
        self.__route: str = None
        self.__go = go
        self.__history_routes: deque[Tuple[str, int]] = deque()
        self._dynamic_control: Dict[str, List[Tuple[Control, Callable[[Control]], None]]] = {}

        self.__secret_key: SecretKey = secret_key
        self.__auto_logout: bool = auto_logout
        self.__sleep: int = 1
        self._key_login: str = None
        self._login_done: bool = False
        self._shared_preferences = (
            SharedPreferencesEdit() if NEW_FLET_VERSION else SessionStorageEdit(page)
        )

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

    """--------- Storage Compatibility Helpers -------"""

    def _storage_set(self, key: str, value: Any) -> None:
        if hasattr(self.page, "client_storage"):
            self.page.client_storage.set(key, value)
        else:
            self.page.run_task(self._shared_preferences.set, key, str(value))

    async def _storage_set_async(self, key: str, value: Any) -> None:
        if hasattr(self.page, "client_storage"):
            await self.page.client_storage.set_async(key, value)
        else:
            await self._shared_preferences.set(key, str(value))

    def _storage_get(self, key: str) -> Any:
        if hasattr(self.page, "client_storage"):
            return self.page.client_storage.get(key)
        else:
            self.page.run_task(self._shared_preferences.get, key)

    async def _storage_get_async(self, key: str) -> Any:
        if hasattr(self.page, "client_storage"):
            return await self.page.client_storage.get_async(key)

        return await self._shared_preferences.get(key)

    def _storage_remove(self, key: str) -> None:
        if hasattr(self.page, "client_storage"):
            self.page.client_storage.remove(key)
        else:
            self.page.run_task(self._shared_preferences.remove, key)

    async def _storage_remove_async(self, key: str) -> None:
        if hasattr(self.page, "client_storage"):
            await self.page.client_storage.remove_async(key)
        else:
            await self._shared_preferences.remove(key)

    """--------- login authentication : asynchronously | synchronously -------"""

    def _login_done_evaluate(self) -> bool:
        return self._login_done

    def _create_task_login_update(self, decode: Dict[str, Any]) -> None:
        """Updates the login status, in case it does not exist it creates a new task that checks the user's login status."""
        time_exp = datetime.fromtimestamp(float(decode.get("exp")), tz=timezone.utc)
        time_now = datetime.now(tz=timezone.utc)
        time_res = time_exp - time_now
        self._login_done = True
        Job(
            func=self.logout,
            key=self.key_login,
            every=time_res,
            page=self.page,
            login_done=self._login_done_evaluate,
            sleep_time=self.__sleep,
        ).start()

    def logout(self, key: str, next_route: str = None) -> None:
        """Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method.

        ### Example:
        ```python
        @app.page('/Dashboard', title='Dashboard', protected_route=True)
        def dashboard(data:fs.Datasy)
            return ft.View(
                controls=[
                    ft.FilledButton('Logout', onclick=lambda e: data.logout('key-login')),
            )
        ```
        """

        if self.route_login is None and next_route is None:
            raise ConfigurationError(
                "Cannot logout: no route to redirect to. "
                "Set 'route_login' in FletEasy() or pass 'next_route' to logout()."
            )

        if self.page.web:
            self.page.pubsub.send_all_on_topic(
                self.page.client_ip + self.page.client_user_agent,
                Msg("logout", key, {"next_route": next_route}),
            )
        else:
            self.page.run_task(self._storage_remove_async, key)
            go_page(self.page, next_route or self.route_login)

    async def __logout_init(self, topic, msg: Msg) -> None:
        if msg.method == "login":
            await self._storage_set_async(msg.key, msg.value.get("value"))
            if self.page.route == self.route_login:
                go_page(self.page, msg.value.get("next_route"))

        elif msg.method == "logout":
            self._login_done = False
            await self._storage_remove_async(msg.key)
            go_page(self.page, msg.value.get("next_route") or self.route_login)

        elif msg.method == "updateLogin":
            self._login_done = msg.value

        elif msg.method == "updateLoginSessions":
            self._login_done = msg.value
            try:
                jwt = await self._storage_get_async(self.key_login)
            except Exception:
                jwt = None
            self._create_task_login_update(
                decode=_decode_payload(
                    jwt=jwt,
                    secret_key=(
                        self.secret_key.secret
                        if self.secret_key.secret is not None
                        else self.secret_key.pem_key.public
                    ),
                    algorithms=self.secret_key.algorithm,
                )
            )
        else:
            raise ConfigurationError(
                f"Unknown pubsub method '{msg.method}' received in session handler. "
                f"Expected: 'login', 'logout', 'updateLogin', or 'updateLoginSessions'."
            )

    def _create_login(self) -> None:
        """Create the connection between sessions."""
        if self.page.web:
            self.page.pubsub.subscribe_topic(
                self.page.client_ip + self.page.client_user_agent, self.__logout_init
            )

    def _create_tasks(self, time_expiry: timedelta, key: str, sleep: int) -> None:
        """Creates the logout task when logging in."""
        if time_expiry is not None:
            Job(
                func=self.logout,
                key=key,
                every=time_expiry,
                page=self.page,
                login_done=self._login_done_evaluate,
                sleep_time=sleep,
            ).start()

    def __login(
        self,
        key: str,
        value: Union[Dict[str, Any], Any],
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ) -> Union[str, None]:
        if time_expiry:
            if not isinstance(value, Dict):
                raise ConfigurationError(
                    f"login() 'value' must be a dict when 'time_expiry' is set, "
                    f"got {type(value).__name__}. Use a dict for JWT payload or remove time_expiry."
                )
            if self.__secret_key is None:
                raise SecretKeyError(
                    "login() requires 'secret_key' in FletEasy() when 'time_expiry' is used. "
                    "Example: FletEasy(secret_key=SecretKey(secret='your-secret', algorithm='HS256'))"
                )

        if self.__secret_key:
            evaluate_secret_key(self)
            self._key_login = key
            self.__sleep = sleep
            value = encode_verified(self.secret_key, value, time_expiry)
            self._login_done = True

        if self.__auto_logout:
            self._create_tasks(time_expiry, key, sleep)

        if self.page.web:
            self.page.pubsub.send_others_on_topic(
                self.page.client_ip + self.page.client_user_agent,
                Msg("login", key, {"value": value, "next_route": next_route}),
            )

        return value

    def login(
        self,
        key: str,
        value: Union[Dict[str, Any], Any],
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ) -> None:
        """Registering in the client's storage the key and value in all browser sessions.

        ### Parameters to use:

        * `key` : It is the identifier to store the value in the client storage.
        * `value` : Recommend to use a dict if you use JWT.
        * `next_route` : Redirect to next route after creating login.
        * `time_expiry` : Time to expire the session, use the `timedelta` class  to configure. (Optional)
        * `sleep` : Time to do login checks, default is 1s. (Optional)
        """
        value = self.__login(key, value, next_route, time_expiry, sleep)

        try:
            self._storage_set(key, value)
        except TimeoutError:
            self.page.run_task(self._storage_set_async, key, value)
            raise LoginError(
                "The operation has timed out. Please use 'login_async()' instead of 'login()'."
            )
        finally:
            self.page.run_task(self.__go, next_route)

    async def login_async(
        self,
        key: str,
        value: Union[Dict[str, Any], Any],
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ) -> None:
        """Registering in the client's storage the key and value in all browser sessions.
        * This method is asynchronous.

        ### Parameters to use:

        * `key` : It is the identifier to store the value in the client storage.
        * `value` : Recommend to use a dict if you use JWT.
        * `next_route` : Redirect to next route after creating login.
        * `time_expiry` : Time to expire the session, use the `timedelta` class  to configure. (Optional)
        * `sleep` : Time to do login checks, default is 1s. (Optional)
        """

        value = self.__login(key, value, next_route, time_expiry, sleep)
        await self._storage_set_async(key, value)
        await self.__go(next_route)

    """ Page go  """

    def go(self, route: str) -> Callable[[ControlEvent], None]:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""

        return lambda _=None: self.go_route(route)

    def go_route(self, route: Union[str, int]) -> None:
        """To change the application path, it is important for better validation to avoid using `page.go()`."""

        async def _go_route():
            await self.__go(route)

        self.page.run_task(_go_route)

    def go_navigation_bar(self, e: ControlEvent) -> None:
        """Handles navigation bar changes. Use this method in the on_change event of
        'ft.NavigationBar' or 'ft.CupertinoNavigationBar' controls."""

        async def _go_nav():
            route = e.control.selected_index
            await self.__go(route)

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
                await self.__go(route)

            self.page.run_task(_go_back)
        else:
            print("-> I can't go back! there is no history. ")

    def page_reload(self):
        """Use this method to reload the page, restores the default values of the page"""
        self.__go(self.page.route, page_reload=True)

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


def evaluate_secret_key(data: Datasy) -> None:
    valid = (
        data.secret_key.secret is None
        and data.secret_key.algorithm == "RS256"
        or data.secret_key.pem_key is None
        and data.secret_key.algorithm == "HS256"
    )
    if not valid:
        raise SecretKeyError(
            f"Algorithm '{data.secret_key.algorithm}' mismatch: "
            f"HS256 requires 'secret' (pem_key must be None), "
            f"RS256 requires 'pem_key' (secret must be None). "
            f"Got secret={'set' if data.secret_key.secret else 'None'}, "
            f"pem_key={'set' if data.secret_key.pem_key else 'None'}."
        )

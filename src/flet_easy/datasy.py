from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict

from flet import Page

from flet_easy.exceptions import LoginError
from flet_easy.extra import Msg, Redirect
from flet_easy.extrasJwt import (
    SecretKey,
    _decode_payload,
    encode_verified,
)
from flet_easy.inheritance import Keyboardsy, Resizesy, SessionStorageEdit, Viewsy
from flet_easy.job import Job


class Datasy:
    """
    The decorated function will always receive a parameter which is `data` (can be any name), which will make an object of type `Datasy` of `Flet-Easy`.

    This class has the following attributes, in order to access its data:

    * `page` : We get the values of the page provided by `Flet` (https://flet.dev/docs/controls/page) .
    * `url_params` : We obtain a dictionary with the values passed through the url.
    * `view` : Get a `View` object from `Flet` (https://flet.dev/docs/controls/view), previously configured with the `view` decorator of `Flet-Easy`.
    * `route_prefix` : Value entered in the `FletEasy` class parameters to create the app object.
    * `route_init` : Value entered in the `FletEasy` class parameters to create the app object.
    * `route_login` : Value entered in the `FletEasy` class parameters to create the app object.
    ---
    * `share` : It is used to be able to store and to obtain values in the client session, the utility is to be able to have greater control in the pages in which it is wanted to share, for it the parameter `share_data` of the `page` decorator must be used. The methods to use are similar `page.session` (https://flet.dev/docs/guides/python/session-storage).

    Besides that you get some extra methods:

        * `contains` : Returns a boolean, it is useful to know if there is shared data.
        * `get_values` : Get a list of all shared values.
        * `get_all` : Get the dictionary of all shared values.
    ----
    * `on_keyboard_event` : get event values to use in the page.
    * `on_resize` : get event values to use in the page.
    * `logout` : method to close sessions of all sections in the browser (client storage), requires as parameter the key or the control (the parameter key of the control must have the value to delete), this is to avoid creating an extra function.
    * `login` : method to create sessions of all sections in the browser (client storage), requires as parameters the key and the value, the same used in the `page.client_storage.set` method.
    * `go` : `go`: Method to change the application path, supports url redirections.
    * `go_back` : Method to go back to the previous route.
    * `history_routes` : Get the history of the routes.
    * `route` : route provided by the route event, it is useful when using middlewares to check if the route is assecible.
    * `redirect` : To redirect to a path before the page loads, it is used in middleware.
    """

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
        go: Callable[[str], None] = None,
    ) -> None:
        self.__page: Page = page
        self.__url_params: Dict[str, Any] = None
        self.__view: Viewsy = None
        self.__route_prefix = route_prefix
        self.__route_init = route_init
        self.__route_login = route_login
        self.__share = SessionStorageEdit(self.__page)
        self.__on_keyboard_event = page_on_keyboard
        self.__on_resize = page_on_resize
        self.__route: str = None
        self.__go = go
        self.__history_routes: deque[str] = deque()

        self.__secret_key: SecretKey = secret_key
        self.__auto_logout: bool = auto_logout
        self.__sleep: int = 1
        self._key_login: str = None
        self._login_done: bool = False

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page: object):
        self.__page = page

    @property
    def history_routes(self):
        return self.__history_routes

    @history_routes.setter
    def history_routes(self, history_routes: deque[str]):
        self.__history_routes = history_routes

    @property
    def url_params(self):
        return self.__url_params

    @url_params.setter
    def url_params(self, url_params: Dict[str, Any]):
        self.__url_params = url_params

    @property
    def view(self):
        return self.__view

    @view.setter
    def view(self, view: Viewsy):
        self.__view = view

    @property
    def route_prefix(self):
        return self.__route_prefix

    @route_prefix.setter
    def route_prefix(self, route_prefix: str):
        self.__route_prefix = route_prefix

    @property
    def route_init(self):
        return self.__route_init

    @route_init.setter
    def route_init(self, route_init: str):
        self.__route_init = route_init

    @property
    def route_login(self):
        return self.__route_login

    @route_login.setter
    def route_login(self, route_login: str):
        self.__route_login = route_login

    @property
    def share(self):
        return self.__share

    # events
    @property
    def on_keyboard_event(self):
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, on_keyboard_event: object):
        self.__on_keyboard_event = on_keyboard_event

    @property
    def on_resize(self):
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, on_resize: object):
        self.__on_resize = on_resize

    @property
    def key_login(self):
        return self._key_login

    @property
    def auto_logout(self):
        return self.__auto_logout

    @property
    def secret_key(self):
        return self.__secret_key

    @property
    def route(self):
        return self.__route

    @route.setter
    def route(self, route: str):
        self.__route = route

    """--------- login authentication : asynchronously | synchronously -------"""

    def _login_done_evaluate(self):
        return self._login_done

    def _create_task_login_update(self, decode: Dict[str, Any]):
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

    def logout(self, key: str):
        """Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method.

        ### Example:
        ```python
        import flet as ft
        import flet_easy as fs

        @app.page('/Dashboard', title='Dashboard', protected_route=True)
        def dashboard(data:fs.Datasy)
            return ft.View(
                controls=[
                    ft.FilledButton('Logout', onclick=data.logout('key-login')),
            )
        ```
        """

        def execute(key: str):
            assert self.route_login is not None, "Adds a login path in the FletEasy Class"
            if self.page.web:
                self.page.pubsub.send_all_on_topic(
                    self.page.client_ip + self.page.client_user_agent, Msg("logout", key)
                )
            else:
                self.page.run_task(self.page.client_storage.remove_async, key)
                self.page.go(self.route_login)

        return lambda _=None: execute(key)

    async def __logaut_init(self, topic, msg: Msg):
        if msg.method == "login":
            await self.page.client_storage.set_async(msg.key, msg.value.get("value"))
            if self.page.route == self.route_login:
                self.page.go(msg.value.get("next_route"))

        elif msg.method == "logout":
            self._login_done = False
            await self.page.client_storage.remove_async(msg.key)
            self.page.go(self.route_login)

        elif msg.method == "updateLogin":
            self._login_done = msg.value

        elif msg.method == "updateLoginSessions":
            self._login_done = msg.value
            self._create_task_login_update(
                decode=_decode_payload(
                    jwt=await self.page.client_storage.get_async(self.key_login),
                    secret_key=(
                        self.secret_key.secret
                        if self.secret_key.secret is not None
                        else self.secret_key.pem_key.public
                    ),
                    algorithms=self.secret_key.algorithm,
                )
            )
        else:
            raise ValueError("Method not implemented in logout_init method.")

    def _create_login(self):
        """Create the connection between sessions."""
        if self.page.web:
            self.page.pubsub.subscribe_topic(
                self.page.client_ip + self.page.client_user_agent, self.__logaut_init
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
        value: Dict[str, Any] | Any,
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ) -> str | None:
        if time_expiry:
            assert isinstance(
                value, Dict
            ), "Use a dict in login method values or don't use time_expiry."
            assert (
                self.__secret_key is not None
            ), "Set the secret_key in the FletEasy class parameter or don't use time_expiry."

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
        value: Dict[str, Any] | Any,
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ):
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
            self.page.client_storage.set(key, value)
        except TimeoutError:
            raise LoginError(
                "The operation has timed out. Please use 'login_async()' instead of 'login()'."
            )

        self.__go(next_route)

    async def login_async(
        self,
        key: str,
        value: Dict[str, Any] | Any,
        next_route: str,
        time_expiry: timedelta = None,
        sleep: int = 1,
    ):
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
        await self.page.client_storage.set_async(key, value)
        self.page.run_thread(self.__go, next_route)

    """ Page go  """

    def go(self, route: str):
        """To change the application path, it is important for better validation to avoid using `page.go()`."""
        return lambda _=None: self.__go(route)

    def redirect(self, route: str):
        """Useful if you do not want to access a route that has already been sent."""
        return Redirect(route)

    def go_back(self):
        """Go back to the previous route."""
        return lambda _=None: (
            (self.history_routes.pop(), self.__go(self.history_routes.pop()))
            if len(self.history_routes) > 1
            else (print("-> I can't go back! There is no route history."), None)
        )


def evaluate_secret_key(data: Datasy):
    assert (
        data.secret_key.secret is None
        and data.secret_key.algorithm == "RS256"
        or data.secret_key.pem_key is None
        and data.secret_key.algorithm == "HS256"
    ), "The algorithm is not set correctly in the 'secret_key' parameter of the 'FletEasy' class."

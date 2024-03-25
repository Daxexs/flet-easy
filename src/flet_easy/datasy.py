from datetime import datetime, timedelta, timezone
from typing import Any

from flet import (
    ControlEvent,
    Page,
    View,
)

from flet_easy.extra import Msg
from flet_easy.extrasJwt import (
    SecretKey,
    _decode_payload_async,
    encode_verified,
)
from flet_easy.inheritance import Keyboardsy, Resizesy, SessionStorageEdit
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
    * `go` : Method to change the path of the application, in order to reduce the code, you must assign the value of the `key` parameter of the `control` used, for example buttons.
    """

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        secret_key: str,
        auto_logout: bool,
        login_async: bool = False,
    ) -> None:
        self.__page: Page = page
        self.__url_params: dict = None
        self.__view: View = None
        self.__route_prefix: str = route_prefix
        self.__route_init: str = route_init
        self.__route_login: str = route_login
        self.__share = SessionStorageEdit(self.__page)
        self.__on_keyboard_event: Keyboardsy = None
        self.__on_resize: Resizesy = None

        self.__secret_key: SecretKey = secret_key
        self.__key_login: str = None
        self.__auto_logout: bool = auto_logout
        self.__sleep: int = 1
        self._login_done: bool = False
        self._login_async: bool = login_async

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page: object):
        self.__page = page

    @property
    def url_params(self):
        return self.__url_params

    @url_params.setter
    def url_params(self, url_params: dict):
        self.__url_params = url_params

    @property
    def view(self):
        return self.__view

    @view.setter
    def view(self, view: View):
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
        return self.__key_login

    @property
    def auto_logout(self):
        return self.__auto_logout

    @property
    def secret_key(self):
        return self.__secret_key

    """--------- login authentication : asynchronously | synchronously -------"""

    def _login_done_evaluate(self):
        return self._login_done

    def _create_task_login_update(self, decode: dict[str, Any]):
        """Updates the login status, in case it does not exist it creates a new task that checks the user's login status."""
        time_exp = datetime.fromtimestamp(float(decode.get("exp")), tz=timezone.utc)
        time_now = datetime.now(tz=timezone.utc)
        time_res = time_exp - time_now
        self._login_done = True
        Job(
            self.logout,
            self.key_login,
            every=time_res,
            sleep_time=self.__sleep,
            page=self.page,
            login_done=self._login_done_evaluate,
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
        if self.page.web:
            self.page.pubsub.send_all_on_topic(self.page.client_ip, Msg("logout", key))
        else:
            self.page.client_storage.remove_async(key)
            self.page.go(self.route_login)

    async def __logaut_init(self, topic, msg: Msg):
        if msg.method == "login":
            self.page.run_task(self.page.client_storage.set_async, msg.key, msg.value)

        elif msg.method == "logout":
            self._login_done = False
            self.page.run_task(self.page.client_storage.remove_async, msg.key)
            self.page.go(self.route_login)

        elif msg.method == "updateLogin":
            self._login_done = msg.value

        elif msg.method == "updateLoginSessions":
            self._login_done = msg.value
            self._create_task_login_update(
                decode=await _decode_payload_async(
                    page=self.page,
                    key_login=self.key_login,
                    secret_key=(self.secret_key.secret if self.secret_key.secret is not None else self.secret_key.pem_key.public),
                    algorithms=self.secret_key.algorithm,
                )
            )
        else:
            Exception("Method not implemented in logout_init method.")

    def _create_login(self):
        """Create the connection between sessions."""
        self.page.pubsub.subscribe_topic(self.page.client_ip, self.__logaut_init)

    def _create_tasks(self, time_expiry: timedelta, key: str, sleep: int) -> None:
        """Creates the logout task when logging in."""
        if time_expiry is not None:
            Job(
                self.logout,
                key,
                every=time_expiry,
                sleep_time=sleep,
                page=self.page,
                login_done=self._login_done_evaluate,
            ).start()

    def login(
        self,
        key: str,
        value: dict[str, Any] | Any,
        time_expiry: timedelta = None,
        next_route: str = None,
        sleep: int = 1,
    ):
        """Registering in the client's storage the key and value in all browser sessions.

        ### Parameters to use:

        * `key` : It is the identifier to store the value in the client storage.
        * `value` : Recommend to use a dict if you use JWT.
        * `time_expiry` : Time to expire the session, use the `timedelta` class  to configure. (Optional)
        * `next_route` : Redirect to next route after creating login. (Optional)
        * `sleep` : Time to do login checks, default is 1s. (Optional)
        """
        if self.__secret_key.Jwt:
            evaluate_secret_key(self)
            self.__key_login = key
            self.__sleep = sleep
            value = encode_verified(self.secret_key, value, time_expiry)
            self._login_done = True

            if self.__auto_logout:
                self._create_tasks(time_expiry, key, sleep)

        self.page.run_task(self.page.client_storage.set_async, key, value)
        self.page.pubsub.send_others_on_topic(self.page.client_ip, Msg("login", key, value))

        if next_route is not None:
            self.page.go(next_route)

    """ Page go  """

    def go(self, route: ControlEvent | str):
        """To change the path of the app, in order to reduce code, you must assign the value of the `key` parameter of the `control` used, for example buttons."""
        if isinstance(route, str):
            self.page.go(route)
        else:
            self.page.go(route.control.key)


def evaluate_secret_key(data: Datasy):
    assert data.secret_key.secret is None and data.secret_key.algorithm == "RS256" or data.secret_key.pem_key is None and data.secret_key.algorithm == "HS256", "The algorithm is not set correctly in the 'secret_key' parameter of the 'FletEasy' class."

from flet import (
    Page,
    View,
    ControlEvent,
)
from typing import Any
from flet_easy.inheritance import SessionStorageEdit, Keyboardsy, Resizesy
from flet_easy.extra import Msg


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
    * `share` : It is used to be able to store and to obtain values in the client session, the utility is to be able to have greater control in the pages in which it is wanted to share and not in all the pages, for it the `share_data` parameter of the `page` decorator must be used. The methods to use are similar `page.session` (https://flet.dev/docs/guides/python/session-storage).

    Besides that you get some extra methods:

        * `contains` : Returns a boolean, it is useful to know if there is shared data.
        * `get_values` : Get a list of all shared values.
        * `get_all` : Get the dictionary of all shared values.
    ----
    * `on_keyboard_event` : get event values to use in the page.
    * `on_resize` : get event values to use in the page.
    * `logaut` : method to close sessions of all sections in the browser (client storage), requires as parameter the key or the control (the parameter key of the control must have the value to delete), this is to avoid creating an extra function.
    * `update_login` : method to create sessions of all sections in the browser (client storage), requires as parameters the key and the value, the same used in the `page.client_storage.set` method.
    * `go` : Method to change the path of the application, in order to reduce the code, you must assign the value of the `key` parameter of the `control` used, for example buttons.
    """

    def __init__(
        self,
        page: Page,
        route_prefix: str,
        route_init: str,
        route_login: str,
        fastapi: bool,
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
        self.__fastapi: bool = fastapi
        self.__client_storage: Msg = None

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

    """--------- login authentication : asynchronously | synchronously -------"""

    async def __fastapi_async(self):
        """Solution to using the methods of
        client_storage with fastapi
        """
        if self.__client_storage.method == "set":
            if self.__fastapi:
                await self.page.client_storage.set_async(
                    self.__client_storage.key, self.__client_storage.value
                )
            else:
                self.page.client_storage.set(
                    self.__client_storage.key, self.__client_storage.value
                )
        elif self.__client_storage.method == "remove":
            if self.__fastapi:
                await self.page.client_storage.remove_async(self.__client_storage.key)
            else:
                self.page.client_storage.set(self.__client_storage.key)

    def logaut(self, key: str):
        self.page.pubsub.send_all_on_topic(self.page.client_ip, Msg("logaut", key))

    def __logaut_init(self, topic, msg: Msg):
        if msg.method == "login":
            self.__client_storage = Msg("set", msg.key, msg.value)
            self.page.run_task(self.__fastapi_async)

        elif msg.method == "logaut":
            self.__client_storage = Msg("remove", msg.key)
            self.page.run_task(self.__fastapi_async)
            self.page.go(self.route_login)

    def _create_login(self):
        self.page.pubsub.subscribe_topic(self.page.client_ip, self.__logaut_init)

    def update_login(self, key: str, value: Any):
        """Registering in the client's storage the key and value in all browser sessions."""
        self.__client_storage = Msg("set", key, value)
        self.page.run_task(self.__fastapi_async)

        self.page.pubsub.send_others_on_topic(
            self.page.client_ip, Msg("login", key, value)
        )

    """ Page go  """

    def go(self, route: ControlEvent | str):
        """To change the path of the app, in order to reduce code, you must assign the value of the `key` parameter of the `control` used, for example buttons."""
        if isinstance(route, str):
            self.page.go(route)
        else:
            self.page.go(route.control.key)

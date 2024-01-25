from flet import (
    PaddingValue,
    Page,
    View,
    Text,
    MainAxisAlignment,
    CrossAxisAlignment,
    KeyboardEvent,
    FloatingActionButton,
    AppBar,
    ScrollMode,
    NavigationBar,
    OptionalNumber,
    NavigationDrawer,
    BottomAppBar,
    FloatingActionButtonLocation,
    CupertinoNavigationBar,
    alignment,
    ControlEvent,
)
from dataclasses import dataclass
from typing import Any, Callable, List
from flet_core import Control
from functools import wraps
from flet.canvas import Canvas

from flet_core.constrained_control import ConstrainedControl
from inspect import iscoroutinefunction


class Keyboardsy:
    """
    Class that manages the input of values by keyboard, contains the following methods:

    ```python
    add_control(function: Callable) # Add a controller configuration (method of a class or function), which is executed with the 'on_keyboard_event' event.
    key() # returns the value entered by keyboard.
    shift() # returns the value entered by keyboard.
    ctrl() # returns the value entered by keyboard.
    alt() # returns the keyboard input.
    meta() # returns keyboard input.
    test() #returns a message of all keyboard input values (key, Shift, Control, Alt, Meta).
    ```
    """

    def __init__(self, call=None) -> None:
        self.__call: KeyboardEvent = call
        self.__controls: list = []

    @property
    def call(self):
        return self.__call

    @call.setter
    def call(self, call: KeyboardEvent):
        self.__call = call

    def _controls(self) -> bool:
        if len(self.__controls) != 0:
            return True
        else:
            return False

    def clear(self):
        self.__controls.clear()

    def add_control(self, function: Callable):
        """Method to add functions to be executed by pressing a key `(supports async, if the app is one)`."""
        self.__controls.append(function)

    async def _run_controls_async(self):
        for value in self.__controls:
            if iscoroutinefunction(value):
                await value()
            else:
                value()

    def _run_controls(self):
        for value in self.__controls:
            value()

    def key(self):
        return self.call.key

    def shift(self):
        return self.call.shift

    def ctrl(self):
        return self.call.ctrl

    def alt(self):
        return self.call.alt

    def meta(self):
        return self.call.meta

    def test(self):
        return f"Key: {self.call.key}, Shift: {self.call.shift}, Control: {self.call.ctrl}, Alt: {self.call.alt}, Meta: {self.call.meta}"


class Resizesy:
    """
    For the manipulation of the `on_resize` event of flet, it contains the following methods:

    ---
    - `add_control(control: object, _self: object = None, min_height: int | float = None)` -> Used to add a flet     control, which will be resposive on the height of the page.
    ### Contains the following parameters:
        - `control: object:` -> To add a flet control (https://flet.dev/docs/controls).
        - `_self: object = None:` -> To add the class object if the class inherits from `UserControl` (https://flet.dev/docs/guides/python/user-controls)
        * ``min_height: int | float = None` -> Add a numerical value, if you want to limit the height of the control     that     is responsive to the page.
    ---
    - `add_controls()` -> used to add all controls added by `add_control` method, to the `on_resize` event of flet.
    ```

    """

    def __init__(self, page: Page = None) -> None:
        self.__page = page
        self.__height: float = None
        self.__width: float = None
        self.__add_controls_f: Callable = None
        self.__add_control: list = []
        self.__margin_y: float | int = 0
        self.__margin_x: float | int = 0

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page: object):
        self.__page = page

    @property
    def margin_y(self):
        return self.__margin_y

    @margin_y.setter
    def margin_y(self, value: int):
        """
        Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied.

        For example:
        * If the `appBar` is activated, it would be a value of 28 and the margin of the `View` control would be 0.
        * If the `appBar` is deactivated, the margin of the `View` control must be 0 and the value of the margin of `on_resize` should not be changed.
        """
        self.__margin_y = value * 2

    @property
    def margin_x(self):
        return self.__margin_x

    @margin_x.setter
    def margin_x(self, value: int):
        """
        Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied."""
        self.__margin_x = value * 2

    @property
    def add_controls_f(self):
        return self.__add_controls_f

    @property
    def height(self):
        if self.__height:
            return self.__height - self.__margin_y
        else:
            return self.__page.height - self.__margin_y

    @height.setter
    def height(self, height: float):
        self.__height = height

    @property
    def width(self):
        if self.__width:
            return self.__width
        else:
            return self.__page.width

    @width.setter
    def width(self, width: float):
        self.__width = width

    def clear(self):
        self.__add_controls_f = None
        self.__add_control.clear()

    def add_control(
        self, control: object, _self: object = None, min_height: int | float = None
    ):
        assert control.height, f"In the 'control' parameter of the function -> '{self.add_control.__name__}' correctly add the flet control"
        assert _self.build, f"In the '_self' parameter of the function -> '{self.add_control.__name__}' correctly adds the object."

        _control = {
            "object": _self,
            "control": control,
            "control_height": float(control.height),
            "min_height": float(min_height) if min_height else None,
        }
        self.__add_control.append(_control)

    def heightX(self, height: int):
        """Function to calculate the percentage of high that will be used in the page, 100 means 100%, the values that can be entered is from (1-100)"""
        if height < 100:
            return (self.page.height - self.margin_y) * float("0." + str(height))
        else:
            return self.page.height - self.margin_y

    def widthX(self, width: int):
        """Function to calculate the percentage of width that will be used in the page, 100 means 100%, the values that can be entered is from (1-100)"""
        if width < 100:
            return (self.page.width - self.margin_x) * float("0." + str(width))
        else:
            return self.page.width - self.margin_x

    async def __response_async(self, conteiner: list):
        """Function to be executed with the `on_resize` event, which will update the controllers added in the `add_control` method."""

        for value in conteiner:
            if value["min_height"]:
                print("height control:", value["control"].height)
                if self.page.height >= int(value["min_height"]):
                    value["control"].height = (
                        self.page.height - self.margin_y
                        if (self.page.height - self.margin_y) <= value["control"].height
                        else value["control_height"]
                    )
                    await value["object"].update_async() if value[
                        "object"
                    ] else await self.page.update_async()
                else:
                    print("pasado")
            else:
                value["control"].height = (
                    self.page.height - self.margin_y
                    if (self.page.height - self.margin_y) <= value["control"].height
                    else value["control_height"]
                )
                await value["object"].update_async() if value[
                    "object"
                ] else await self.page.update_async()

    def __response(self, conteiner: list):
        """Function to be executed with the `on_resize` event, which will update the controllers added in the `add_control` method."""

        for value in conteiner:
            if value["min_height"]:
                print("height control:", value["control"].height)
                if self.page.height >= int(value["min_height"]):
                    value["control"].height = (
                        self.page.height - self.margin_y
                        if (self.page.height - self.margin_y) <= value["control"].height
                        else value["control_height"]
                    )
                    value["object"].update() if value["object"] else self.page.update()
                else:
                    print("pasado")
            else:
                value["control"].height = (
                    self.page.height - self.margin_y
                    if (self.page.height - self.margin_y) <= value["control"].height
                    else value["control_height"]
                )
                value["object"].update() if value["object"] else self.page.update()

    def add_controls_async(self):
        """Adding a list of controllers, using an anonymous function (lambda)"""
        self.__add_controls_f = lambda: self.__response_async(self.__add_control)

    def add_controls(self):
        """Adding a list of controllers, using an anonymous function (lambda)"""
        self.__add_controls_f = lambda: self.__response(self.__add_control)

    async def _run_async(self) -> object:
        """Execute `on_resize` in async controls"""
        return await self.__add_controls_f()

    def _run(self) -> object:
        """Execute `on_resize` in controls"""
        return self.__add_controls_f()


class Controllersy:
    """
    It is used to inherit in a class that is going to behave as a controller that is going to be linked in a model class and the view.

    It inherits the following attributes:
    * `_self: Control` -> The object of the class that inherits from `UserControl` (https://flet.dev/docs/guides/python/user-controls) is added.
    * `on_resize: Resizesy` = None -> Add the value obtained from the `data` parameter of the function that returns `View` from flet (optional).
    * `on_keyboard: Keyboardsy` = None -> Add the value obtained from the `data` parameter of the function returning  `View` from flet. (optional)
    """

    def __init__(
        self,
        _self: ConstrainedControl,
        on_resize: Resizesy = None,
        on_keyboard: Keyboardsy = None,
    ) -> None:
        self.__x: ConstrainedControl = _self
        self.__on_resize: Resizesy = on_resize
        self.__on_keyboard_event: Keyboardsy = on_keyboard

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new):
        self.__x = new

    @property
    def on_keyboard_event(self):
        return self.__on_keyboard_event

    @on_keyboard_event.setter
    def on_keyboard_event(self, on_keyboard_event):
        self.__on_keyboard_event = on_keyboard_event

    @property
    def on_resize(self):
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, on_resize):
        self.__on_resize = on_resize


@dataclass
class Msg:
    method: str
    key: str
    value: str = None


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
    * `on_keyboard_event` : get event values to use in the page.
    * `on_resize` : get event values to use in the page.
    * `logaut and logaut_async` : method to close sessions of all sections in the browser (client storage), requires as parameter the key or the control (the parameter key of the control must have the value to delete), this is to avoid creating an extra function.
    * `update_login and update_login_async` : method to create sessions of all sections in the browser (client storage), requires as parameters the key and the value, the same used in the `page.client_storage.set` method.
    * `go and go_async` : Method to change the path of the application, in order to reduce the code, you must assign the value of the `key` parameter of the `control` used, for example buttons.
    """

    def __init__(
        self, route_prefix: str = None, route_init: str = None, route_login: str = None
    ) -> None:
        self.__page: Page = None
        self.__url_params: list = None
        self.__view: View = None
        self.__route_prefix: str = route_prefix
        self.__route_init: str = route_init
        self.__route_login: str = route_login
        self.__on_keyboard_event: Keyboardsy = None
        self.__on_resize: Resizesy = None

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

    """ login authentication async"""

    async def logaut_async(self, e: ControlEvent | str):
        if isinstance(e, str):
            key = e
        else:
            key = e.control.key
        await self.page.pubsub.send_all_on_topic_async(
            self.page.client_ip, Msg("logaut", key)
        )

    async def __logaut_init_asyn(self, topic, msg: Msg):
        if msg.method == "login":
            await self.page.client_storage.set_async(msg.key, msg.value)
            await self.page.update_async()

        elif msg.method == "logaut":
            await self.page.client_storage.remove_async(msg.key)
            await self.page.go_async(self.route_login)
            await self.page.update_async()

    async def _create_login_async(self):
        await self.page.pubsub.subscribe_topic_async(
            self.page.client_ip, self.__logaut_init_asyn
        )

    async def update_login_async(self, key: str, value: Any):
        """Registering in the client's storage the key and value in all browser sessions."""
        await self.page.pubsub.send_all_on_topic_async(
            self.page.client_ip, Msg("login", key, value)
        )

    """ login authentication"""

    def logaut(self, e: ControlEvent | str):
        if isinstance(e, str):
            key = e
        else:
            key = e.control.key
        self.page.pubsub.send_all_on_topic(self.page.client_ip, Msg("logaut", key))

    def __logaut_init(self, topic, msg: Msg):
        if msg.method == "login":
            self.page.client_storage.set(msg.key, msg.value)
            self.page.update()

        elif msg.method == "logaut":
            self.page.client_storage.remove(msg.key)
            self.page.go(self.route_login)
            self.page.update()

    def _create_login(self):
        self.page.pubsub.subscribe_topic(self.page.client_ip, self.__logaut_init)

    def update_login(self, key: str, value: Any):
        """Registering in the client's storage the key and value in all browser sessions."""
        self.page.pubsub.send_all_on_topic(
            self.page.client_ip, Msg("login", key, value)
        )

    """ Page go  """

    def go(self, e: ControlEvent | str):
        """To change the path of the app, in order to reduce code, you must assign the value of the `key` parameter of the `control` used, for example buttons."""
        if isinstance(e, str):
            route = e
        else:
            route = e.control.key
        self.page.go(route)

    async def go_async(self, e: ControlEvent | str):
        """To change the path of the app, in order to reduce code, you must assign the value of the `key` parameter of the `control` used, for example buttons."""
        if isinstance(e, str):
            route = e
        else:
            route = e.control.key
        await self.page.go_async(route)


@dataclass
class Pagesy:
    """To add pages, it requires the following parameters:
    * route: text string of the url, for example(`'/task'`).
    * ``view``: Stores the page function.
    * ``clear``: Removes the pages from the `page.views` list of flet. (optional)
    * ``protected_route``: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
    * ``custom_params``: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.

    Example:
    ```python
    Pagesy('/test/{id:d}/user/{name:l}', test_page, protected_route=True)
    ```
    """

    route: str
    view: Callable
    clear: bool = False
    protected_route: bool = False
    custom_params: dict = None

    def __hash__(self):
        return hash((self.route, self.view, self.clear, self.protected_route))

    def __eq__(self, other):
        return (
            isinstance(other, Pagesy)
            and self.route == other.route
            and self.view == other.view
            and self.clear == other.clear
            and self.protected_route == other.protected_route
        )


@dataclass
class Viewsy:
    route: str | None = None
    controls: List[Control] | None = None
    appbar: AppBar | None = None
    bottom_appbar: BottomAppBar | None = None
    floating_action_button: FloatingActionButton | None = None
    floating_action_button_location: FloatingActionButtonLocation | None = None
    navigation_bar: NavigationBar | CupertinoNavigationBar | None = None
    drawer: NavigationDrawer | None = None
    end_drawer: NavigationDrawer | None = None
    vertical_alignment: MainAxisAlignment = MainAxisAlignment.NONE
    horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE
    spacing: OptionalNumber = None
    padding: PaddingValue = None
    bgcolor: str | None = None
    scroll: ScrollMode | None = None
    auto_scroll: bool | None = None
    fullscreen_dialog: bool | None = None
    on_scroll_interval: OptionalNumber = None
    on_scroll: Any = None


class AddPagesy:
    """Creates an object to then add to the list of the `add_routes` method of the `FletEasy` class.
    -> Requires the parameter:
    * route_prefix: text string that will bind to the url of the `page` decorator, example(`/users`) this will encompass all urls of this class. (optional)

    Example:
    ```python
    users = fs.AddPagesy(
        route_prefix='/user'
    )

    # -> Urls to be created:
    # * '/user/task'
    # * '/user/information'

    @users.page('/task')
    async def task_page(data: fs.Datasy):

        page = data.page

        page.title = 'Task'

        return ft.View(
            route='/users/task',
            controls=[
                ft.Text('Task'),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment

        )

    @users.page('/information')
    async def information_page(data: fs.Datasy):

        page = data.page

        page.title = 'Information'

        return ft.View(
            route='/users/information',
            controls=[
                ft.Text('Information'),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment

        )
    ```

    """

    def __init__(self, route_prefix: str = None):
        self.route_prefix = route_prefix
        self.__pages = set()

    def __decorator(self, data: dict = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            if self.route_prefix:
                route = (
                    self.route_prefix
                    if data.get("route") == "/"
                    else self.route_prefix + data.get("route")
                )
            else:
                route = data.get("route")

            self.__pages.add(
                Pagesy(
                    route,
                    func,
                    data.get("page_clear"),
                    data.get("proctect_route"),
                    custom_params=data.get("custom_params"),
                )
            )
            return wrapper

        return decorator

    def page(
        self,
        route: str,
        page_clear: bool = False,
        proctect_route: bool = False,
        custom_params: dict = None,
    ):
        """Decorator to add a new page to the app, you need the following parameters:
        * route: text string of the url, for example(`'/counter'`).
        * clear: Removes the pages from the `page.views` list of flet. (optional)
        * protected_route: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
        * custom_params: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.

        -> The decorated function must receive a parameter, for example `data:fs.Datasy`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        counter = fs.AddPagesy(
            route_prefix='/counter'
        )

        @counter.page('/')
        async def counter_page(data: fs.Datasy):

            view = data.view
            page = data.page

            page.title = 'Counter'
            view.appbar.title = ft.Text('Counter')

            return ft.View(
                route='/counter',
                controls=[
                    ft.Text('Counter'),
                ],
                appbar=view.appbar,
                vertical_alignment=view.vertical_alignment,
                horizontal_alignment=view.horizontal_alignment
            )
        ```
        """
        data = {
            "route": route,
            "page_clear": page_clear,
            "proctect_route": proctect_route,
            "custom_params": custom_params,
        }
        return self.__decorator(data)

    def _add_pages(self, route: str = None) -> set:
        if route:
            for page in self.__pages:
                if page.route == "/":
                    page.route = route
                else:
                    page.route = route + page.route
        return self.__pages


class ResponsiveControlsy(Canvas):
    """Allows the controls to adapt to the size of the app (responsive). It is suitable for use in applications, in web it is not recommended.

    ### Note: Avoid activating scroll outside `ResponseControl`.

    This class contains the following parameters:
    * `content: Control` -> Contains a control of flet.
    * `expand: int` -> To specify the space that will contain the `content` controller in the app, 1 equals the whole app.
    * `resize_interval: int` -> To specify the response time (optional).
    * `on_resize: callable` -> Custom function to be executed when the app is resized (optional).
    * `show_resize: bool` -> To observe the size of the controller (width x height). is disabled when sending an `on_resize` function. (optional)
    * `show_resize_terminal: bool` -> To see the size of the controller (width x height) in the terminal. (optional)

    Example:
    ```python
    import flet_easy as fs

    fs.ResponsiveControlsy(
        content=ft.Container(
            content=ft.Text("on_resize"),
            bgcolor=ft.colors.RED,
            alignment=ft.alignment.center,
            height=100
        ),
        expand=1,
        show_resize=True
    )
    ```

    """

    def __init__(
        self,
        content: Control,
        expand: int,
        resize_interval=1,
        on_resize: Callable = None,
        show_resize: bool = False,
        show_resize_terminal: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.content = content
        self.resize_interval = resize_interval
        self.resize_callback = on_resize
        self.expand = expand
        self.show_resize = show_resize
        self.show_resize_terminal = show_resize_terminal
        self.on_resize = self.__handle_canvas_resize

    async def __handle_canvas_resize(self, e):
        if self.resize_callback:
            await self.resize_callback(e)
        elif self.show_resize:
            if self.content.content:
                self.content.content.value = f"{e.width} x {e.height}"
                await self.update_async()
            else:
                self.content.alignment = alignment.center
                self.content.content = Text(f"{e.width} x {e.height}")
                await self.update_async()

        if self.show_resize_terminal:
            print(f"{e.width} x {e.height}")

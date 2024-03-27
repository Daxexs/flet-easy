from dataclasses import dataclass
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, List, TypeVar

from flet import (
    AppBar,
    BottomAppBar,
    ControlEvent,
    CrossAxisAlignment,
    CupertinoNavigationBar,
    FloatingActionButton,
    FloatingActionButtonLocation,
    KeyboardEvent,
    MainAxisAlignment,
    NavigationBar,
    NavigationDrawer,
    OptionalNumber,
    PaddingValue,
    Page,
    Ref,
    ScrollMode,
    Text,
    alignment,
)
from flet.canvas import Canvas
from flet_core import Control
from flet_core.session_storage import SessionStorage

T = TypeVar("T")


class SessionStorageEdit(SessionStorage):
    def __init__(self, page):
        super().__init__(page)

    def contains(self) -> bool:
        return len(self._SessionStorage__store) != 0

    def get_values(self) -> List[Any]:
        return list(self._SessionStorage__store.values())

    def get_all(self) -> dict[str, Any]:
        return self._SessionStorage__store


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
        return len(self.__controls) != 0

    def clear(self):
        self.__controls.clear()

    def add_control(self, function: Callable):
        """Method to add functions to be executed by pressing a key `(supports async, if the app is one)`."""
        self.__controls.append(function)

    async def _run_controls(self):
        for value in self.__controls:
            if iscoroutinefunction(value):
                await value()
            else:
                value()

    def key(self) -> str:
        return self.call.key

    def shift(self) -> bool:
        return self.call.shift

    def ctrl(self) -> bool:
        return self.call.ctrl

    def alt(self) -> bool:
        return self.call.alt

    def meta(self) -> bool:
        return self.call.meta

    def test(self):
        return f"Key: {self.call.key}, Shift: {self.call.shift}, Control: {self.call.ctrl}, Alt: {self.call.alt}, Meta: {self.call.meta}"


class Resizesy:
    """
    For the manipulation of the `on_resize` event of flet, it contains the following methods:

    ---
    * `e` : Returns `ControlEvent` event, each time the height and width changes.
    * `page` : Returns `ControlEvent` event, each time the height and width changes.
    * `height` : Returns its updated value.
    * `width` : Returns its updated value.
    * `heightX()` :This method allows to obtain the values of the height of the page, which requires as parameter to enter an integer value from 1 to 100 (100 = 100%).
    * `widthx()` : This method is similar to the previous one in terms of page width.

    ```

    """

    def __init__(self, page: Page = None) -> None:
        self.__page = page
        self.__height: float = page.height
        self.__width: float = page.width
        self.__margin_y: float | int = 0
        self.__margin_x: float | int = 0
        self.__e: ControlEvent = None

    @property
    def page(self) -> Page:
        return self.__page

    @property
    def e(self):
        return self.__e

    @e.setter
    def e(self, e: ControlEvent):
        self.__e = e
        self.__page = e.page
        self.__height = self.page.height - self.__margin_y
        self.__width = self.page.width - self.__margin_x

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
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    def heightX(self, height: int):
        """Function to calculate the percentage of high that will be used in the page, 100 means 100%, the values that can be entered is from (1-100)"""
        if height < 100:
            return (self.height - self.margin_y) * float("0." + str(height))
        else:
            return self.height - self.margin_y

    def widthX(self, width: int):
        """Function to calculate the percentage of width that will be used in the page, 100 means 100%, the values that can be entered is from (1-100)"""
        if width < 100:
            return (self.width - self.margin_x) * float("0." + str(width))
        else:
            return self.width - self.margin_x


@dataclass
class Pagesy:
    """To add pages, it requires the following parameters:
    * `route`: text string of the url, for example(`'/task'`).
    * `view`: Stores the page function.
    * `title` : Define the title of the page.
    * `clear`: Removes the pages from the `page.views` list of flet. (optional)
    * `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way.
    * `protected_route`: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
    * `custom_params`: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.

    Example:
    ```python
    Pagesy('/test/{id:d}/user/{name:l}', test_page, protected_route=True)
    ```
    """

    route: str
    view: Callable
    title: str = None
    clear: bool = False
    share_data: bool = False
    protected_route: bool = False
    custom_params: dict = None

    def __hash__(self):
        return hash((self.route, self.view, self.title, self.clear, self.protected_route))

    def __eq__(self, other):
        return isinstance(other, Pagesy) and self.route == other.route and self.view == other.view and self.tilte == other.title and self.clear == other.clear and self.protected_route == other.protected_route


# Add new attributes if flet adds in its updates.
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

            route = (self.route_prefix if data.get("route") == "/" else self.route_prefix + data.get("route")) if self.route_prefix else data.get("route")

            self.__pages.add(
                Pagesy(
                    route=route,
                    view=func,
                    title=data.get("title"),
                    clear=data.get("page_clear"),
                    share_data=data.get("share_data"),
                    protected_route=data.get("protected_route"),
                    custom_params=data.get("custom_params"),
                )
            )
            return wrapper

        return decorator

    def page(
        self,
        route: str,
        title: str = None,
        page_clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: dict = None,
    ):
        """Decorator to add a new page to the app, you need the following parameters:
        * route: text string of the url, for example(`'/counter'`).
        * `title` : Define the title of the page. (optional).
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

        @counter.page('/', title='Counter)
        async def counter_page(data: fs.Datasy):

            view = data.view

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
            "title": title,
            "page_clear": page_clear,
            "share_data": share_data,
            "protected_route": protected_route,
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


class Ref(Ref[T]):
    """Get the reference of the control used by flet, it is linked to the created component. It is similar to flet, but more reduced by getting the value of the control with (c)."""

    @property
    def c(self) -> T:
        return super().current

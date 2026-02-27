import base64
import pickle
from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, List, TypeVar, Union

from flet import (
    ControlEvent,
    KeyboardEvent,
    Page,
    Ref,
    Text,
    View,
)
from flet.canvas import Canvas

from flet_easy.exceptions import KeyBoardEventError, StorageSerializationError
from flet_easy.logger import get_logger
from flet_easy.migration import (
    NEW_FLET_VERSION,
    Control,
    SessionStorage,
    SharedPreferences,
    alignment,
)

T = TypeVar("T")
logger = get_logger("controls")


class SessionStorageEdit(SharedPreferences if NEW_FLET_VERSION else SessionStorage):
    def __init__(self, page):
        super().__init__(page)

    def contains(self) -> bool:
        return len(self._SessionStorage__store) != 0

    def get_values(self) -> List[Any]:
        return list(self._SessionStorage__store.values())

    def get_all(self) -> Dict[str, Any]:
        return self._SessionStorage__store


class SharedPreferencesEdit(SharedPreferences if NEW_FLET_VERSION else SessionStorage):
    def __init__(self, prefix: str = ""):
        super().__init__()
        self._prefix = prefix

    def _prefixed_key(self, key: str) -> str:
        """Add prefix to the key for namespace isolation."""
        return f"{self._prefix}{key}" if self._prefix else key

    def _strip_prefix(self, key: str) -> str:
        """Remove prefix from the key."""
        if self._prefix and key.startswith(self._prefix):
            return key[len(self._prefix) :]
        return key

    async def set(self, key: str, value: Any) -> None:
        prefixed = self._prefixed_key(key)
        if NEW_FLET_VERSION:
            if isinstance(value, (int, float, bool, str)) or (
                isinstance(value, list) and all(isinstance(i, str) for i in value)
            ):
                await super().set(prefixed, value)
            else:
                try:
                    serialized = base64.b64encode(pickle.dumps(value)).decode("utf-8")
                    await super().set(prefixed, f"fs-pickled:{serialized}")
                except Exception as e:
                    raise StorageSerializationError(
                        "Failed to serialize value for SharedPreferences storage.",
                        value_type=type(value).__name__,
                        detail=e,
                    )
        else:
            super().set(prefixed, value)

    async def get(self, key: str) -> Any:
        prefixed = self._prefixed_key(key)
        if NEW_FLET_VERSION:
            val = await super().get(prefixed)
            if isinstance(val, str) and val.startswith("fs-pickled:"):
                try:
                    return pickle.loads(base64.b64decode(val[11:]))
                except Exception:
                    return val
            return val
        else:
            return super().get(prefixed)

    async def remove(self, key: str) -> None:
        prefixed = self._prefixed_key(key)
        if NEW_FLET_VERSION:
            await super().remove(prefixed)
        else:
            super().remove(prefixed)

    async def contains(self) -> bool:
        keys = await self.get_keys("")
        return len(keys) != 0

    async def get_values(self) -> List[Any]:
        keys = await self.get_keys("")
        return [await self.get(k) for k in keys]

    async def get_all(self) -> Dict[str, Any]:
        keys = await self.get_keys("")
        result = {}
        for key in keys:
            value = await self.get(key)
            result[key] = value
        return result

    async def get_keys(self, key_prefix: str = "") -> List[str]:
        prefixed = self._prefixed_key(key_prefix)
        all_keys = await super().get_keys(prefixed)
        return [self._strip_prefix(k) for k in all_keys]

    async def clear(self) -> None:
        """Clear only keys in this namespace (prefix). Does NOT wipe all SharedPreferences."""
        if self._prefix:
            keys = await super().get_keys(self._prefix)
            for key in keys:
                await super().remove(key)
        else:
            await super().clear()


class Keyboardsy:
    """Class that manages keyboard input values.

    Methods:
        add_control(function) - Add functions to be executed on key press (supports async).
        key() - Returns the key value.
        shift() - Returns the shift state.
        ctrl() - Returns the ctrl state.
        alt() - Returns the alt state.
        meta() - Returns the meta state.
        test() - Returns a message of all keyboard input values.
    """

    __slots__ = ("__call", "__controls", "__current_route", "__current_controls")

    def __init__(self, call=None) -> None:
        self.__call: KeyboardEvent = call
        self.__controls: Dict[str, list] = {}
        self.__current_route: str = None
        self.__current_controls: list = []

    @property
    def current_route(self) -> str:
        return self.__current_route

    @current_route.setter
    def current_route(self, value: str):
        self.__current_route = value
        if value not in self.__controls:
            self.__controls[value] = []
        self.__current_controls = self.__controls[value]

    @property
    def call(self):
        return self.__call

    @call.setter
    def call(self, call: KeyboardEvent):
        self.__call = call

    def _controls(self) -> bool:
        return len(self.__current_controls) != 0

    def clear(self):
        self.__current_controls.clear()

    def add_control(self, function: Callable):
        """Method to add functions to be executed by pressing a key `(supports async, if the app is one)`."""
        self.__current_controls.append(function)

    async def _run_controls(self):
        """Execute all registered keyboard control functions."""
        if not self.__current_controls:
            return

        for control_func in self.__current_controls:
            try:
                if iscoroutinefunction(control_func):
                    await control_func()
                else:
                    control_func()
            except Exception as e:
                raise KeyBoardEventError(
                    f"Error executing keyboard control in function: {control_func} - {e}"
                )

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
    """For the manipulation of the `on_resize` event of flet.

    Attributes:
        e - Returns `ControlEvent` event, each time the height and width changes.
        page - Returns the `Page` instance.
        height - Returns the updated height value.
        width - Returns the updated width value.
        heightX(pct) - Calculate percentage of page height (1-100).
        widthX(pct) - Calculate percentage of page width (1-100).
        margin_y - Y-axis margin value.
        margin_x - X-axis margin value.
    """

    __slots__ = ("__page", "__height", "__width", "__margin_y", "__margin_x", "__e")

    def __init__(self, page: Page) -> None:
        self.__page = page
        self.__height: float = page.height
        self.__width: float = page.width
        self.__margin_y: Union[float, int] = 0
        self.__margin_x: Union[float, int] = 0
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
        """Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied."""
        self.__margin_y = value * 2

    @property
    def margin_x(self):
        return self.__margin_x

    @margin_x.setter
    def margin_x(self, value: int):
        """Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied."""
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


class Viewsy(View):
    pass


class ResponsiveControlsy(Canvas):
    """Allows the controls to adapt to the size of the app (responsive).

    Parameters:
        content (Control) - Contains a flet control.
        expand (int) - Space that will contain the `content` controller in the app.
        resize_interval (int) - Response time (optional).
        on_resize (callable) - Custom function executed on app resize (optional).
        show_resize (bool) - Observe the size of the controller (optional).
        show_resize_terminal (bool) - See the size in the terminal (optional).
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

    def __handle_canvas_resize(self, e):
        if self.resize_callback is not None:
            if iscoroutinefunction(self.resize_callback):
                self.page.run_task(self.resize_callback, e)
            else:
                self.resize_callback(e)

        elif self.show_resize:
            if self.content.content:
                self.content.content.value = f"{e.width} x {e.height}"
                self.update()
            else:
                self.content.alignment = alignment.center
                self.content.content = Text(f"{e.width} x {e.height}")
                self.update()

        if self.show_resize_terminal:
            print(f"{e.width} x {e.height}")


class Ref(Ref[T]):
    """Get the reference of the control used by flet, linked to the created component.
    Similar to flet, but more reduced by getting the value of the control with (c)."""

    @property
    def c(self) -> T:
        return super().current

import base64
import pickle
from inspect import iscoroutinefunction
from typing import Any, Callable, Optional, TypeVar, Union, cast
from warnings import warn

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
    SessionStorageEditBase,
    SharedPreferencesEditBase,
)

T = TypeVar("T")
logger = get_logger("controls")

# Maximum number of deserialized objects kept in the in-memory cache per SharedPreferencesEdit instance.
# Older entries are evicted FIFO when the limit is reached.
_CACHE_PIC_MAXSIZE = 256


class SessionStorageEdit(SessionStorageEditBase):
    """Provides backward compatibility support for SessionStorage on Flet < 0.80."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def contains(self) -> bool:
        return len(self._SessionStorage__store) != 0

    def get_values(self) -> list[Any]:
        return list(self._SessionStorage__store.values())

    def get_all(self) -> dict[str, Any]:
        return self._SessionStorage__store


class SharedPreferencesEdit(SharedPreferencesEditBase):
    """Provides enhanced object serialization support for SharedPreferences on Flet >= 0.80."""

    def __init__(self, prefix: str = "") -> None:
        super().__init__()
        self._prefix = prefix
        self._cache_pic: dict[str, Any] = {}

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
                cached = self._cache_pic.get(val)
                if cached is not None:
                    return cached
                try:
                    obj = pickle.loads(base64.b64decode(val[11:]))
                    if len(self._cache_pic) >= _CACHE_PIC_MAXSIZE:
                        # Evict oldest entry (FIFO — dict preserves insertion order)
                        self._cache_pic.pop(next(iter(self._cache_pic)))
                    self._cache_pic[val] = obj
                    return obj
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

    async def get_values(self) -> list[Any]:
        keys = await self.get_keys("")
        return [await self.get(k) for k in keys]

    async def get_all(self) -> dict[str, Any]:
        keys = await self.get_keys("")
        return {key: await self.get(key) for key in keys}

    async def get_keys(self, key_prefix: str = "") -> list[str]:
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
        add_control(function): Add functions to be executed on key press (supports async).
        key(): Returns the key value.
        shift(): Returns the shift state.
        ctrl(): Returns the ctrl state.
        alt(): Returns the alt state.
        meta(): Returns the meta state.
        test(): Returns a message of all keyboard input values.
    """

    __slots__ = ("__call", "__controls", "__current_route", "__current_controls")

    def __init__(self, call: Optional[KeyboardEvent] = None) -> None:
        self.__call: Optional[KeyboardEvent] = call
        self.__controls: dict[str, list[Any]] = {}
        self.__current_route: Optional[str] = None
        self.__current_controls: list[Any] = []

    @property
    def current_route(self) -> Optional[str]:
        return self.__current_route

    @current_route.setter
    def current_route(self, value: str) -> None:
        self.__current_route = value
        if value not in self.__controls:
            self.__controls[value] = []
        self.__current_controls = self.__controls[value]

    @property
    def call(self) -> Optional[KeyboardEvent]:
        return self.__call

    @call.setter
    def call(self, call: KeyboardEvent) -> None:
        self.__call = call

    def _controls(self) -> bool:
        return bool(self.__current_controls)

    def clear(self) -> None:
        self.__current_controls.clear()

    def add_control(self, function: Callable[..., Any]) -> None:
        """Method to add functions to be executed by pressing a key `(supports async, if the app is one)`."""
        self.__current_controls.append(function)

    async def _run_controls(self) -> None:
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
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        return self.__call.key

    def shift(self) -> bool:
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        return self.__call.shift

    def ctrl(self) -> bool:
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        return self.__call.ctrl

    def alt(self) -> bool:
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        return self.__call.alt

    def meta(self) -> bool:
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        return self.__call.meta

    def test(self) -> str:
        assert self.__call is not None, "call must be set before reading keyboard event properties"
        c = self.__call
        return f"Key: {c.key}, Shift: {c.shift}, Control: {c.ctrl}, Alt: {c.alt}, Meta: {c.meta}"


class Resizesy:
    """For the manipulation of the `on_resize` event of flet.

    Attributes:
        e: Returns `ControlEvent` event, each time the height and width changes.
        page: Returns the `Page` instance.
        height: Returns the updated height value.
        width: Returns the updated width value.
        heightX(pct): Calculate percentage of page height (1-100).
        widthX(pct): Calculate percentage of page width (1-100).
        margin_y: Y-axis margin value.
        margin_x: X-axis margin value.
    """

    __slots__ = ("__page", "__height", "__width", "__margin_y", "__margin_x", "__e")

    def __init__(self, page: Page) -> None:
        self.__page = page
        self.__height: Optional[Union[float, int]] = page.height
        self.__width: Optional[Union[float, int]] = page.width
        self.__margin_y: Union[float, int] = 0
        self.__margin_x: Union[float, int] = 0
        self.__e: Optional[ControlEvent] = None

    @property
    def page(self) -> Page:
        return cast(Page, self.__page)

    @property
    def e(self) -> Optional[ControlEvent]:
        return self.__e

    @e.setter
    def e(self, e: ControlEvent) -> None:
        self.__e = e
        self.__page = e.page
        self.__height = float(self.page.height or 0) - self.__margin_y
        self.__width = float(self.page.width or 0) - self.__margin_x

    @property
    def margin_y(self) -> Union[float, int]:
        return self.__margin_y

    @margin_y.setter
    def margin_y(self, value: int) -> None:
        """Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied."""
        self.__margin_y = value * 2

    @property
    def margin_x(self) -> Union[float, int]:
        return self.__margin_x

    @margin_x.setter
    def margin_x(self, value: int) -> None:
        """Enter a value that subtracts the margin of the page, so that 100% of the page can be occupied."""
        self.__margin_x = value * 2

    @property
    def height(self) -> Optional[Union[float, int]]:
        return self.__height

    @property
    def width(self) -> Optional[Union[float, int]]:
        return self.__width

    def height_x(self, height: int) -> float:
        """Function to calculate the percentage of high that will be used in the page (1-100)."""
        current_height = float(self.page.height or 0) - self.margin_y
        if height < 100:
            return current_height * (height / 100)
        return current_height

    def width_x(self, width: int) -> float:
        """Function to calculate the percentage of width that will be used in the page (1-100)."""
        current_width = float(self.page.width or 0) - self.margin_x
        if width < 100:
            return current_width * (width / 100)
        return current_width

    def heightX(self, height: int) -> float:  # noqa: N802
        """Deprecated: Use height_x instead."""
        warn("heightX is deprecated, use height_x instead", DeprecationWarning, stacklevel=2)
        return self.height_x(height)

    def widthX(self, width: int) -> float:  # noqa: N802
        """Deprecated: Use width_x instead."""
        warn("widthX is deprecated, use width_x instead", DeprecationWarning, stacklevel=2)
        return self.width_x(width)


class Viewsy(View):
    pass


class ResponsiveControlsy(Canvas):
    """Allows the controls to adapt to the size of the app (responsive).

    Parameters:
        content (Control): Contains a flet control.
        expand (int): Space that will contain the `content` controller in the app.
        resize_interval (int): Response time (optional).
        on_resize (callable): Custom function executed on app resize (optional).
        show_resize (bool): Observe the size of the controller (optional).
        show_resize_terminal (bool): See the size in the terminal (optional).
    """

    def __init__(
        self,
        content: Control,
        expand: int,
        resize_interval: int = 1,
        on_resize: Optional[Callable[..., Any]] = None,
        show_resize: bool = False,
        show_resize_terminal: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.content = content
        self.resize_interval = resize_interval
        self.resize_callback = on_resize
        self.expand = expand
        self.show_resize = show_resize
        self.show_resize_terminal = show_resize_terminal
        self.on_resize = self.__handle_canvas_resize

    def __handle_canvas_resize(self, e: Any) -> None:
        if self.resize_callback is not None:
            if iscoroutinefunction(self.resize_callback):
                getattr(self.page, "run_task", lambda *args: None)(self.resize_callback, e)
            else:
                self.resize_callback(e)

        elif self.show_resize:
            inner = getattr(self.content, "content", None)
            if inner:
                inner.value = f"{e.width} x {e.height}"
                self.update()
            else:
                cast(Any, self.content).content = Text(f"{e.width} x {e.height}")
                self.update()

        if self.show_resize_terminal:
            logger.debug("Canvas resize: %s x %s", e.width, e.height)


class Ref(Ref[T]):
    """Get the reference of the control used by flet, linked to the created component.
    Similar to flet, but more reduced by getting the value of the control with (c)."""

    @property
    def c(self) -> T:
        current = super().current
        assert current is not None, "Ref.c accessed before control was mounted"
        return current

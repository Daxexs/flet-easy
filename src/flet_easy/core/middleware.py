from collections import deque
from typing import Callable, Optional, Union

from flet import View

from flet_easy.core.context import current_data
from flet_easy.core.data import Datasy
from flet_easy.core.models import Redirect


class MiddlewareRequest:
    _data: Optional[Datasy] = None

    def __init__(self) -> None:
        self._local_data: Optional[Datasy] = None

    @property
    def data(self) -> Optional[Datasy]:
        """Retrieve the context-local Datasy instance if set, otherwise fallback to class default."""
        val = current_data.get()
        if val is not None:
            return val
        if self._local_data is not None:
            return self._local_data
        return MiddlewareRequest._data

    @data.setter
    def data(self, value: Optional[Datasy]) -> None:
        self._local_data = value
        if value is not None:
            current_data.set(value)

    def before_request(self) -> None:
        pass

    def after_request(self) -> None:
        pass


MiddlewareHandler = Callable[[Datasy], Optional[Redirect]]
MiddlewareItem = Union[MiddlewareHandler, MiddlewareRequest, type[MiddlewareRequest]]
Middleware = Optional[Union[list[MiddlewareItem], deque[MiddlewareItem], MiddlewareItem]]
ViewHandler = Callable[[Datasy], View]

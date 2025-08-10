from typing import Callable, List, Optional, Union

from flet import View

from flet_easy.datasy import Datasy
from flet_easy.extra import Redirect


class MiddlewareRequest:
    _data: Datasy = None

    def __init__(self):
        self.data = MiddlewareRequest._data

    def before_request(self):
        pass

    def after_request(self):
        pass


MiddlewareHandler = Callable[[Datasy], Optional[Redirect]]
Middleware = Optional[
    Union[List[Union[MiddlewareHandler, MiddlewareRequest]], MiddlewareHandler, MiddlewareRequest]
]
ViewHandler = Callable[[Datasy], View]

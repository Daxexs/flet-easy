from collections import deque
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from flet import View

from flet_easy.datasy import Datasy
from flet_easy.extra import Redirect

MiddlewareHandler = Callable[[Datasy], Optional[Redirect]]
Middleware = List[MiddlewareHandler]
ViewHandler = Callable[[Datasy], View]


@dataclass
class Pagesy:
    """To add pages, it requires the following parameters:
    * `route`: text string of the url, for example(`'/task'`).
    * `view`: Stores the page function.
    * `title` : Define the title of the page.
    * `clear`: Removes the pages from the `page.views` list of flet. (optional)
    * `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way. (optional)
    * `protected_route`: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
    * `custom_params`: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.
    * `middleware` : It acts as an intermediary between different software components, intercepting and processing requests and responses. They allow adding functionalities to an application in a flexible and modular way. (optional)

    Example:
    ```python
    Pagesy("/test/{id:d}/user/{name:l}", test_page, protected_route=True)
    ```
    """

    route: str
    view: ViewHandler
    title: str = None
    clear: bool = False
    share_data: bool = False
    protected_route: bool = False
    custom_params: Dict[str, Callable[[], bool]] = None
    middleware: Middleware = None


class AddPagesy:
    """Creates an object to then add to the list of the `add_routes` method of the `FletEasy` class.
    -> Requires the parameter:
    * route_prefix: text string that will bind to the url of the `page` decorator, example(`/users`) this will encompass all urls of this class. (optional)

    Example:
    ```python
    users = fs.AddPagesy(route_prefix="/user")

    # -> Urls to be created:
    # * '/user/task'
    # * '/user/information'


    @users.page("/task")
    async def task_page(data: fs.Datasy):
        page = data.page

        page.title = "Task"

        return ft.View(
            route="/users/task",
            controls=[
                ft.Text("Task"),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment,
        )


    @users.page("/information")
    async def information_page(data: fs.Datasy):
        page = data.page

        page.title = "Information"

        return ft.View(
            route="/users/information",
            controls=[
                ft.Text("Information"),
            ],
            vertical_alignment=view.vertical_alignment,
            horizontal_alignment=view.horizontal_alignment,
        )
    ```

    """

    def __init__(self, route_prefix: str = None):
        self.route_prefix = route_prefix
        self.__pages = deque()

    def __decorator(self, data: Dict = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            route = (
                (
                    self.route_prefix
                    if data.get("route") == "/"
                    else self.route_prefix + data.get("route")
                )
                if self.route_prefix
                else data.get("route")
            )

            self.__pages.append(
                Pagesy(
                    route=route,
                    view=func,
                    title=data.get("title"),
                    clear=data.get("page_clear"),
                    share_data=data.get("share_data"),
                    protected_route=data.get("protected_route"),
                    custom_params=data.get("custom_params"),
                    middleware=data.get("middleware"),
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
        custom_params: Dict[str, Any] = None,
        middleware: Middleware = None,
    ):
        """Decorator to add a new page to the app, you need the following parameters:
        * route: text string of the url, for example(`'/counter'`).
        * `title` : Define the title of the page. (optional).
        * clear: Removes the pages from the `page.views` list of flet. (optional)
        * `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way. (optional)
        * protected_route: Protects the route of the page, according to the configuration of the `login` decorator of the `FletEasy` class. (optional)
        * custom_params: To add validation of parameters in the custom url using a list, where the key is the name of the parameter validation and the value is the custom function that must report a boolean value.
        * `middleware` : It acts as an intermediary between different software components, intercepting and processing requests and responses. They allow adding functionalities to an application in a flexible and modular way. (optional)

        -> The decorated function must receive a parameter, for example `data:fs.Datasy`.

        Example:
        ```python
        import flet as ft
        import flet_easy as fs

        counter = fs.AddPagesy(route_prefix="/counter")


        @counter.page("/", title="Counter")
        async def counter_page(data: fs.Datasy):
            view = data.view

            view.appbar.title = ft.Text("Counter")

            return ft.View(
                route="/counter",
                controls=[
                    ft.Text("Counter"),
                ],
                appbar=view.appbar,
                vertical_alignment=view.vertical_alignment,
                horizontal_alignment=view.horizontal_alignment,
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
            "middleware": middleware,
        }
        return self.__decorator(data)

    def _add_pages(self, route: str = None) -> deque:
        if route:
            for page in self.__pages:
                if page.route == "/":
                    page.route = route
                else:
                    page.route = route + page.route
        return self.__pages

from dataclasses import dataclass, field
from re import Pattern, compile
from typing import Any, Callable, Optional, Union

from flet import RouteChangeEvent, ViewPopEvent

from flet_easy.migration import context, observable, unwrap_component


# 1. Context to share routing function
@dataclass(frozen=True)
class RoutingContextValue:
    views: Callable[[str], Any]


# Monotonic counter — ensures every `RouteState` instance is unique for use_state.
_route_state_counter: int = 0


@observable
@dataclass
class RouteState:
    route: str
    _version: int = field(default=0, compare=True)

    def __post_init__(self) -> None:
        global _route_state_counter
        _route_state_counter += 1
        object.__setattr__(self, "_version", _route_state_counter)

    def on_route_change(self, e: RouteChangeEvent) -> None:
        if self.route != e.route:
            self.route = e.route

    async def view_popped(self, e: ViewPopEvent):
        views = unwrap_component(context.page.views)
        if len(views) > 1:
            await context.page.push_route(views[-2].route)


@dataclass
class Msg:
    method: str
    key: Optional[str] = None
    value: Optional[Union[str, bool, dict[Any, Any]]] = None


@dataclass
class Redirect:
    route: Optional[str] = None


TYPE_PATTERNS: dict[str, tuple[Pattern[str], Callable[[str], Optional[Any]]]] = {
    "int": (compile(r"-?\d+"), int),
    "float": (compile(r"-?\d+\.\d+"), float),
    "str": (compile(r"[^/]+"), str),
    "bool": (compile(r"(true|True|false|False)"), lambda x: x in ["true", "True"]),
}

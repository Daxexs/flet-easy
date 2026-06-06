"""Flet event handlers mixin for FletEasyX.

Manages on_route_change, on_view_pop, keyboard, resize, and disconnect.
Exclusive to imperative mode — in declarative mode, these events
are managed within the app() component.
"""

from typing import Any

from flet import ControlEvent, KeyboardEvent, RouteChangeEvent, ViewPopEvent

from flet_easy.core.context import current_data
from flet_easy.core.models import Msg
from flet_easy.migration import go_page

from ._base import _RouterBase


class EventsMixin(_RouterBase):
    """Mixin for Flet page events (imperative mode)."""

    __slots__ = ()

    async def _route_change(self, e: RouteChangeEvent) -> None:
        """Imperative handler for on_route_change.

        If _pagesy is pre-loaded (programmatic navigation), it renders
        directly. Otherwise, it resolves the route from scratch.
        """
        current_data.set(self._data)
        self._logger.debug("Event triggered: on_route_change -> Route destination: '%s'", e.route)
        if self._pagesy is None:
            if e.route == "/" and self._route_init != "/":
                await go_page(self._page, self._route_init)
                return
            await self._go(e.route, True)
        else:
            await self._view_append(e.route, self._pagesy)
            self._pagesy = None

    def _view_pop(self, e: ViewPopEvent) -> None:
        """on_view_pop handler — delegates to data.go_back()."""
        self._logger.debug("Event triggered: on_view_pop -> Delegating to Datasy.go_back()")
        self._data.go_back()

    def _on_keyboard_event(self, e: KeyboardEvent) -> None:
        """Keyboard event handler."""
        self._page_on_keyboard.call = e
        if self._page_on_keyboard._controls():
            self._check_async(self._page_on_keyboard._run_controls)

    def _page_resize(self, e: ControlEvent) -> None:
        """Page resize handler."""
        self._page_on_resize.e = e

    def _disconnect(self, e: Any) -> None:
        """Notifies other web sessions when an authenticated user disconnects."""
        if self._data._login_done and self._page.web:
            client_ip = getattr(self._page, "client_ip", None)
            if client_ip:
                self._page.pubsub.send_others_on_topic(
                    client_ip,
                    Msg("updateLoginSessions", value=self._data._login_done),
                )

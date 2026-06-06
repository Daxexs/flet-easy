"""Flet version compatibility layer.

Centralizes version detection and conditional imports for supporting
both Flet 0.28.* (old API) and Flet >= 0.80.* (new API).
"""

__all__ = [
    "NEW_FLET_VERSION",
    "Control",
    "SessionStorageEditBase",
    "SharedPreferencesEditBase",
    "context",
    "observable",
    "unwrap_component",
]

from typing import TYPE_CHECKING

from flet import Page

if TYPE_CHECKING:
    from typing import Any

    NEW_FLET_VERSION = True
    from flet.controls.control import Control

    SessionStorageEditBase = Any
    SharedPreferencesEditBase = Any

    context: Any = None
    observable: Any = None
    unwrap_component: Any = None

else:
    try:
        # Flet < 0.80 (old API: flet.core.*)
        NEW_FLET_VERSION = False
        from flet.core.control import Control
        from flet.core.session_storage import SessionStorage as SessionStorageEditBase
        from flet.core.session_storage import SessionStorage as SharedPreferencesEditBase

        def observable(cls):
            return cls

        def unwrap_component(c):
            return c

        class _DummyContext:
            class _DummyPage:
                views = []

                async def push_route(self, route: str) -> None:
                    pass

            page = _DummyPage()

        context = _DummyContext()

    except ImportError:
        # Flet >= 0.80 (new API: flet.controls.*)
        NEW_FLET_VERSION = True
        from flet import context, observable, unwrap_component
        from flet.controls.control import Control
        from flet.controls.services.shared_preferences import (
            SharedPreferences as SessionStorageEditBase,
        )
        from flet.controls.services.shared_preferences import (
            SharedPreferences as SharedPreferencesEditBase,
        )


async def go_page(page: Page, route: str) -> None:
    """Navigate to a route using the appropriate method based on Flet version. `page.go()` deprecated in Flet 0.90 replaced by `page.push_route()`."""
    if hasattr(page, "go"):
        page.go(route)
    else:
        await page.push_route(route)

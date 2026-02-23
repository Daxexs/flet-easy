"""Flet version compatibility layer.

Centralizes version detection and conditional imports for supporting
both Flet 0.28.* (old API) and Flet >= 0.80.* (new API).
"""

__all__ = [
    "NEW_FLET_VERSION",
    "alignment",
    "Control",
    "SessionStorage",
    "SharedPreferences",
]

from flet import Page

try:
    # Flet < 0.80 (old API: flet.core.*)
    NEW_FLET_VERSION = False
    from flet.core import alignment  # type: ignore
    from flet.core.control import Control  # type: ignore
    from flet.core.session_storage import SessionStorage  # type: ignore

    SharedPreferences = None  # Not available in old Flet

except ImportError:
    # Flet >= 0.80 (new API: flet.controls.*)
    NEW_FLET_VERSION = True
    from flet.controls import alignment
    from flet.controls.control import Control
    from flet.controls.services.shared_preferences import SharedPreferences

    SessionStorage = None  # Not available in new Flet


def go_page(page: Page, route: str) -> None:
    """Navigate to a route using the appropriate method based on Flet version. `page.go()` deprecated in Flet 0.90 replaced by `page.push_route()`."""
    if hasattr(page, "go"):
        page.go(route)
    else:
        page.push_route(route)

"""Compatibility layer with Flet's declarative API (>= 0.80).

Centralizes conditional imports so the rest of the package
does not have to repeat try/except blocks.
"""

from typing import Any

from flet_easy.core.models import RoutingContextValue

# Declare module-level variables with Any to prevent redefinition type-checker errors
ft_component: Any
Routingctx: Any
use_state: Any

try:
    from flet import component as _ft_component
    from flet import create_context
    from flet import use_state as _use_state_impl
    from flet.components.component import Component

    _DECLARATIVE_API_AVAILABLE: bool = True
    Routingctx = create_context(RoutingContextValue(lambda _r: None))
    use_state = _use_state_impl
    ft_component = _ft_component

    _original_before_update = Component.before_update

    def _patched_before_update(self):
        """Patch before update method to catch rendering errors in Flet components."""
        try:
            _original_before_update(self)
        except Exception as e:
            page = self.page
            fsx = getattr(page, "_flet_easy_router", None) if page else None

            # If error boundary is disabled, re-raise the exception
            if fsx and not fsx._use_error_boundary:
                raise

            import traceback

            from flet_easy.logger import get_logger
            from flet_easy.ui.view_error import page_error_fs

            logger = get_logger("FletEasy")
            component_name = getattr(self.fn, "__name__", "unknown")
            logger.exception("Error rendering component '%s': %s", component_name, e)

            if page:
                error_msg = (
                    f"Component '{component_name}' rendering failed:\n\n{traceback.format_exc()}"
                )
                if fsx and getattr(fsx, "_declarative_mode", False):
                    # Declarative mode
                    fsx._resolved_views[page.route] = page_error_fs(page.route, error_msg)
                    if fsx._declarative_set_route_state:
                        from flet_easy.core.models import RouteState

                        fsx._declarative_set_route_state(RouteState(page.route))
                else:
                    # Imperative mode
                    if hasattr(page.views, "clear"):
                        page.views.clear()
                        page.views.append(page_error_fs(page.route, error_msg))
                        page.update()

    setattr(Component, "before_update", _patched_before_update)  # noqa: B010

except ImportError:
    # Flet < 0.80: Declarative API not available.
    def _ft_component_fallback(fn: Any) -> Any:
        """No-op fallback — marks the function as a component."""
        fn.__is_component__ = True
        return fn

    ft_component = _ft_component_fallback
    _DECLARATIVE_API_AVAILABLE = False
    Routingctx = None
    use_state = None


__all__ = [
    "ft_component",
    "use_state",
    "Routingctx",
    "_DECLARATIVE_API_AVAILABLE",
]

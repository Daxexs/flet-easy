import functools
import inspect
import warnings
from typing import Any, Callable, Optional


def normalize_route(prefix: Optional[str], route: str) -> str:
    """
    Normalizes and builds a complete route by combining a prefix and a route.
    """
    if not prefix:
        return route
    if route == "/":
        return prefix
    return prefix + route


def deprecated(
    message: str, version: str = "0.4.0"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to mark a function as deprecated.
    It will emit a warning when the function is called.
    """

    def decorator(func: Any) -> Callable[..., Any]:
        _warn_msg = (
            f"{func.__name__} is deprecated and will be removed in version {version}. {message}"
        )

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(_warn_msg, category=FutureWarning, stacklevel=2)
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(_warn_msg, category=FutureWarning, stacklevel=2)
            return await func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator

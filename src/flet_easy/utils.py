import functools
import inspect
import warnings


def deprecated(message: str, version: str = "0.4.0"):
    """
    Decorator to mark a function as deprecated.
    It will emit a warning when the function is called.
    """

    def decorator(func):
        _warn_msg = (
            f"{func.__name__} is deprecated and will be removed in version {version}. {message}"
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(_warn_msg, category=FutureWarning, stacklevel=2)
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            warnings.warn(_warn_msg, category=FutureWarning, stacklevel=2)
            return await func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator

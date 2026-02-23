class FletEasyError(Exception):
    """Base exception for all FletEasy errors.

    All FletEasy-specific exceptions inherit from this class,
    making it easy to catch any library error with a single except clause.
    """

    pass


class LoginError(FletEasyError):
    """Raised when a login operation fails.

    Common causes:
    - Timeout when storing credentials in client storage (use `login_async()` instead)
    - Storage write failure during login
    """

    def __init__(self, message: str = "", detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[LoginError] {message}{detail_str}")


class LoginRequiredError(FletEasyError):
    """Raised when accessing a protected route without authentication.

    This occurs when:
    - A page decorated with `protected_route=True` is accessed without valid login
    - The `@app.login` decorator function raises an error
    """

    def __init__(self, message: str = "", detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[LoginRequiredError] {message}{detail_str}")


class LogoutError(FletEasyError):
    """Raised when a logout operation fails.

    Common causes:
    - JWT decode error (double use of storage key, invalid secret key)
    - Storage removal failure
    """

    def __init__(self, message: str = "", detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[LogoutError] {message}{detail_str}")


class RouteError(FletEasyError):
    """Raised when route processing fails during navigation.

    Common causes:
    - Error in page function execution
    - Middleware or login check failure during route resolution
    """

    def __init__(self, detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[RouteError] Route processing failed.{detail_str}")


class AlgorithmJwtError(FletEasyError):
    """Raised when an unsupported JWT algorithm is used.

    Supported algorithms: HS256, RS256.
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[AlgorithmJwtError] {message}")


class SecretKeyError(FletEasyError):
    """Raised when `secret_key` is missing or misconfigured.

    Common causes:
    - `secret_key` not set in `FletEasy(secret_key=...)` but JWT features are used
    - Algorithm mismatch: HS256 requires `secret`, RS256 requires `pem_key`
    - `secret_key.algorithm` is None

    Fix: Ensure `FletEasy(secret_key=SecretKey(algorithm='HS256', secret='...'))` is set.
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[SecretKeyError] {message}")


class ConfigurationError(FletEasyError):
    """Raised when a required configuration is missing or invalid.

    Common causes:
    - Missing `route_login` in `FletEasy(route_login='...')` when using protected routes
    - Invalid `time_expiry` usage without a dict value in `login()`
    - Empty `add_views` in `add_routes()`
    - Invalid middleware configuration
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[ConfigurationError] {message}")


class ViewError(FletEasyError):
    """Raised when a view is not a valid callable or class.

    The `view` parameter in `Pagesy` must be either:
    - A function (sync or async) that returns `ft.View`
    - A class with a `build()` method that returns `ft.View`
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[ViewError] {message}")


class CustomParamsError(FletEasyError, ValueError):
    """Raised when custom URL parameter types are invalid or unrecognized.

    Common causes:
    - Using a type in route like `{id:x}` where `x` is not registered
    - Declaring `custom_params` but not using any custom type in the route

    Built-in types: `d` (int), `l` (str), `f` (float), `str` (string).
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[CustomParamsError] {message}")


class MiddlewareError(FletEasyError):
    """Raised when middleware processing fails.

    Common causes:
    - Middleware class does not inherit from `MiddlewareRequest`
    - Middleware function raised an unhandled exception
    - Failed to instantiate middleware class
    """

    def __init__(self, message: object = "", detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[MiddlewareError] {message}{detail_str}")


class AddPagesError(FletEasyError):
    """Raised when adding pages via `add_pages()` fails.

    Common causes:
    - Invalid `AddPagesy` object
    - Route conflict or malformed route string
    """

    def __init__(self, message: str = "", detail: object = None):
        detail_str = f" | Detail: {detail}" if detail else ""
        super().__init__(f"[AddPagesError] {message}{detail_str}")


class FunctionError(FletEasyError):
    """Raised when an expected function is not callable."""

    def __init__(self, message: str = ""):
        super().__init__(f"[FunctionError] {message}")


class KeyBoardEventError(FletEasyError):
    """Raised when a keyboard event handler fails.

    This occurs when a function registered via `on_keyboard_event.add_control()`
    raises an exception during execution.
    """

    def __init__(self, message: str = ""):
        super().__init__(f"[KeyBoardEventError] {message}")


class StorageSerializationError(FletEasyError):
    """Raised when a value cannot be serialized for SharedPreferences storage.

    Common causes:
    - The value contains objects that cannot be pickled (e.g., lambdas, open file handles)
    - Circular references in the data structure
    - Custom objects without proper __reduce__ or __getstate__ methods

    Fix: Use only serializable types (int, float, bool, str, list, dict)
    or ensure custom objects implement pickle support.
    """

    def __init__(self, message: str = "", value_type: str = "", detail: object = None):
        parts = [f"[StorageSerializationError] {message}"]
        if value_type:
            parts.append(f"Type: {value_type}")
        if detail:
            parts.append(f"Detail: {detail}")
        super().__init__(" | ".join(parts))

class FletEasyError(Exception):
    """FletEasy error captured"""

    pass


class LoginError(FletEasyError):
    """Login error captured"""

    pass


class LoginRequiredError(FletEasyError):
    """Login required - used in route FletEasyX"""

    pass


class RouteError(FletEasyError):
    """Route error"""

    pass


class AlgorithmJwtError(FletEasyError):
    """Algorithm error"""

    pass


class LogoutError(FletEasyError):
    """Logout error"""

    pass


class MidlewareError(FletEasyError):
    """Middleware error"""

    pass


class AddPagesError(FletEasyError):
    """Add pages error in route"""

    pass

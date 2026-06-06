from contextvars import ContextVar
from typing import Any, Optional

# A context variable to store the Datasy object for the current async task execution.
# This prevents race conditions and cross-session data leakages in multi-user/concurrent environments.
# Isolated in this module to prevent circular dependency loops during top-level imports.
current_data: ContextVar[Optional[Any]] = ContextVar("flet_easy_middleware_data", default=None)

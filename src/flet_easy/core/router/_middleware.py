"""Middleware execution mixin for FletEasyX.

Full pipeline: instance verification, before/after request execution,
and results handling (Redirect or block).
"""

from collections import deque
from typing import Any, Optional, Union, cast

from flet_easy.core.context import current_data
from flet_easy.core.middleware import MiddlewareHandler, MiddlewareRequest
from flet_easy.core.models import Redirect
from flet_easy.core.pages import Pagesy
from flet_easy.exceptions import MiddlewareError

from ._base import _RouterBase


class MiddlewareMixin(_RouterBase):
    """Mixin for the execution of the middleware pipeline."""

    __slots__ = ()

    def _verify_instance_middleware(
        self,
        middlewares: deque[MiddlewareRequest],
        middleware: Union[type[MiddlewareRequest], MiddlewareRequest],
        index: int,
    ) -> None:
        """Instantiates a class-based middleware if it has not been already."""
        try:
            if isinstance(middleware, type):
                m_instance = middleware()
                middlewares[index] = m_instance
                self._logger.debug("Middleware instantiated: %s", m_instance)
        except Exception as e:
            raise MiddlewareError(
                f"Failed to instantiate middleware class '{type(middleware).__name__}' at index {index}.",
                detail=e,
            )

    async def _execute_middleware(
        self,
        pagesy: Pagesy,
        url_params: dict[str, Any],
        middleware_list: Union[
            list[Union[MiddlewareRequest, MiddlewareHandler, type[MiddlewareRequest]]],
            deque[Union[MiddlewareRequest, MiddlewareHandler, type[MiddlewareRequest]]],
        ],
    ) -> bool:
        """Executes a list of middlewares in order.

        Returns True if navigation should stop (redirect or block).
        """
        if not middleware_list:
            return False

        current_data.set(self._data)

        try:
            for i, middleware in enumerate(middleware_list):
                # Instantiate class-based middleware at request time
                # (MiddlewareRequest._data is only available after __init__)
                if isinstance(middleware, type) and issubclass(middleware, MiddlewareRequest):
                    m_instance = middleware()
                    middleware_list[i] = m_instance
                    middleware = m_instance

                self._logger.debug("Execute middleware: %s", middleware)

                if isinstance(middleware, MiddlewareRequest):
                    res = await self._await_func(middleware.before_request)
                else:
                    res = await self._await_func(middleware, self._data)

                if await self._handle_middleware_result(res):
                    return True

            return False

        except Exception as e:
            raise MiddlewareError(
                f"Middleware execution failed for route '{pagesy.route}'. "
                f"Check that all middlewares return None, False, or Redirect.",
                detail=e,
            )

    async def _handle_middleware_result(self, result: Optional[Union[bool, Redirect]]) -> bool:
        """Processes the return value of a middleware."""
        if not result:
            return False

        if isinstance(result, Redirect):
            self._logger.debug("Middleware Action: Redirecting to '%s'", result.route)
            if result.route is not None:
                await self._go(result.route)
            return True

        self._logger.debug("Middleware Action: Navigation completely blocked by Middleware.")
        return False

    async def _run_after_request_middlewares(self, pagesy: Pagesy) -> None:
        """Executes all after-request middlewares for the page."""
        if pagesy._valid_middlewares_request():
            self._logger.debug(
                "Executing %d after_request middleware(s) for route: %s",
                len(pagesy._middlewares_request),
                pagesy.route,
            )
            current_data.set(self._data)
            for i, middleware in enumerate(pagesy._middlewares_request):
                self._verify_instance_middleware(pagesy._middlewares_request, middleware, i)
                await self._await_func(pagesy._middlewares_request[i].after_request)

    async def _run_middlewares_optimized(
        self,
        route: str,
        route_match: dict[str, Any],
        pagesy: Pagesy,
        use_route_change: bool,
        page_reload: bool = False,
    ) -> None:
        """Executes global + page middlewares, then navigates.

        Calls _reload_datasy() once before executing any middleware,
        ensuring that data.route and url_params are available.
        """
        self._logger.debug("Middlewares: %s | Pagesy: %s", self._middlewares, pagesy.middleware)

        await self._reload_datasy(pagesy, route_match)

        if pagesy.middleware and await self._execute_middleware(
            pagesy,
            route_match,
            cast(Any, pagesy.middleware),
        ):
            return

        await self._navigate(route, pagesy, use_route_change, page_reload)

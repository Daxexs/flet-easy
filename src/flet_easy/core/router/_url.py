"""URL matching mixin for FletEasyX.

Provides dynamic route resolution with typed parameters
(e.g., /user/{id:int}) using compiled and cached regular expressions.
"""

from re import Pattern, compile, escape
from typing import Any, Callable, Optional

from flet_easy.core.models import TYPE_PATTERNS
from flet_easy.exceptions import CustomParamsError
from flet_easy.logger import get_logger

from ._base import _RouterBase

_url_logger = get_logger("UrlMixin")


class UrlMixin(_RouterBase):
    """Mixin with URL matching classmethods — no instance state."""

    __slots__ = ()

    # Compiled pattern cache shared across all instances.
    _compiled_patterns_cache: dict[str, tuple[Pattern[str], list[tuple[str, Callable]]]] = {}

    @classmethod
    def _get_compiled_pattern_and_segments(
        cls,
        url_pattern: str,
        custom_types: Optional[dict[str, Callable[[str], Any]]] = None,
    ) -> tuple[Pattern[str], list[tuple[str, Callable[[str], Any]]]]:
        """Compiles and caches the regex pattern + segments for a dynamic route."""
        if url_pattern in cls._compiled_patterns_cache:
            _url_logger.debug("UrlMixin: Cache hit for pattern '%s'", url_pattern)
            return cls._compiled_patterns_cache[url_pattern]

        _url_logger.debug("UrlMixin: Compiling new pattern for '%s'", url_pattern)
        combined_patterns = {
            **TYPE_PATTERNS,
            **{k: (compile(r"[^/]+"), v) for k, v in (custom_types or {}).items()},
        }

        segments: list[tuple[str, Callable[[str], Any]]] = []
        pattern_parts: list[str] = []
        used_custom_types: set[str] = set()

        for segment in url_pattern.strip("/").split("/"):
            if segment == "":
                continue

            if segment[0] in "<{" and segment[-1] in ">}":
                name, type_ = (
                    segment[1:-1].split(":", 1) if ":" in segment else (segment[1:-1], "str")
                )
                try:
                    regex_part, parser = combined_patterns[type_]
                except KeyError:
                    raise CustomParamsError(
                        f"Unrecognized URL parameter type '{type_}' in route '{url_pattern}'. "
                        f"Built-in types: int, float, str, bool. "
                        f"Register custom types via 'custom_params' parameter."
                    ) from None

                if custom_types and type_ in custom_types:
                    used_custom_types.add(type_)

                pattern_parts.append(f"(?P<{name}>{regex_part.pattern})")
                segments.append((name, parser))
            else:
                pattern_parts.append(escape(segment))

        if custom_types:
            for type_ in custom_types:
                if type_ not in used_custom_types:
                    raise CustomParamsError(
                        f"Route '{url_pattern}' declares custom_params {list(custom_types.keys())} "
                        f"but none are used in the route pattern. "
                        f"Remove custom_params or add them to the route pattern."
                    )

        pattern = compile("^/" + "/".join(pattern_parts) + "/?$")
        cls._compiled_patterns_cache[url_pattern] = (pattern, segments)
        return pattern, segments

    @classmethod
    def _verify_url(
        cls,
        url_pattern: str,
        url: str,
        custom_types: Optional[dict[str, Callable[[str], Any]]] = None,
    ) -> Optional[dict[str, Any]]:
        """Checks if the URL matches the pattern and returns the extracted parameters."""
        pattern, segments = cls._get_compiled_pattern_and_segments(url_pattern, custom_types)
        match = pattern.match(url)

        if not match:
            return None

        params: dict[str, Any] = {}
        for name, parser in segments:
            val = match.group(name)
            try:
                parsed_val = parser(val)
                if parsed_val is None:
                    return None
                params[name] = parsed_val
            except (ValueError, TypeError):
                return None

        _url_logger.debug(
            "UrlMixin: Matched URL '%s' with pattern '%s' -> Derived Params: %s",
            url,
            url_pattern,
            params,
        )
        return params

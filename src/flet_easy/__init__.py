from flet_easy.core.data import Datasy
from flet_easy.core.models import Redirect
from flet_easy.security.config import Algorithm, PemKey, SecretKey, encode_HS256, encode_RS256
from flet_easy.core.app import FletEasy
from flet_easy.ui.controls import (
    Keyboardsy,
    Ref,
    Resizesy,
    ResponsiveControlsy,
    Viewsy,
)
from flet_easy.security.jwt import EasyKey, decode, decode_async
from flet_easy.core.pages import AddPagesy, Pagesy
from flet_easy.core.middleware import MiddlewareRequest

page = FletEasy.page

from importlib.metadata import version

__version__ = version("flet-easy")

__all__ = [
    "Datasy",
    "Redirect",
    "Algorithm",
    "PemKey",
    "SecretKey",
    "encode_HS256",
    "encode_RS256",
    "FletEasy",
    "Keyboardsy",
    "Ref",
    "Resizesy",
    "ResponsiveControlsy",
    "Viewsy",
    "EasyKey",
    "decode",
    "decode_async",
    "AddPagesy",
    "Pagesy",
    "MiddlewareRequest",
    "page",
    "__version__",
]

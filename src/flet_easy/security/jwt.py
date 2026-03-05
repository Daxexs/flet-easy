from __future__ import annotations

from secrets import token_bytes
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from flet_easy.core.data import Datasy
from flet_easy.exceptions import RsaMissingError
from flet_easy.utils import deprecated

try:
    from jwt import DecodeError, ExpiredSignatureError, InvalidKeyError
except ImportError:

    class DecodeError(Exception):
        pass

    class ExpiredSignatureError(Exception):
        pass

    class InvalidKeyError(Exception):
        pass


try:
    from rsa import newkeys
except ImportError:

    def newkeys(*args, **kwargs):
        raise RsaMissingError()


class EasyKey:
    """To obtain a `secret_key` more easily, support algorithms [ HS256, RS256 ]

    ### Example:
    ```python
    import flet_easy as fs

    key = fs.EasyKey()

    # --- HS256
    SECRET_KEY = key.secret_key()

    # --- RS256
    PRIVATE_KEY = key.private_key()
    PUBLIC_KEY = key.public_key()
    ```
    """

    def __init__(self):
        (public_key, private_key) = newkeys(2048)
        self.public = public_key
        self.private = private_key

    def private_key(self) -> str:
        return self.private.save_pkcs1().decode("utf-8")

    def public_key(self) -> str:
        return self.public.save_pkcs1().decode("utf-8")

    def secret_key(self) -> str:
        return token_bytes(64).hex().encode("utf-8")


@deprecated("Use the 'data.decode_jwt' method instead.", version="0.4.0")
def decode(key_login: str, data: Datasy) -> Union[dict[str, Any], bool]:  # noqa: UP007
    """decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    return data.decode_jwt(key_login)


@deprecated("Use the 'data.decode_jwt_async' method instead.", version="0.4.0")
async def decode_async(key_login: str, data: Datasy) -> Union[dict[str, Any], bool]:  # noqa: UP007
    """ "decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    return await data.decode_jwt_async(key_login)

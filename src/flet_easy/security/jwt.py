from secrets import token_bytes
from typing import Any, Dict, Union

from flet_easy.core.data import Datasy, evaluate_secret_key
from flet_easy.core.models import Msg
from flet_easy.exceptions import (
    FletEasyError,
    LoginError,
    LogoutError,
    RsaMissingError,
    SecretKeyError,
)
from flet_easy.security.config import _decode_payload

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


def _handle_decode_errors(jwt: str, data: Datasy, key_login: str) -> Union[Dict[str, Any], bool]:
    """decodes the jwt and updates the browser sessions."""
    try:
        data._key_login = key_login
        evaluate_secret_key(data)

        if jwt is None:
            return False

        if data.auto_logout and not data._login_done:
            data.page.pubsub.send_others_on_topic(
                data.page.client_ip, Msg("updateLogin", value=data._login_done)
            )

        decode = _decode_payload(
            jwt=jwt,
            secret_key=(
                data.secret_key.secret
                if data.secret_key.secret is not None
                else data.secret_key.pem_key.public
            ),
            algorithms=data.secret_key.algorithm,
        )
        """ It checks if there is a logout time, if there is a logout task running and finally if the user wants to create a logout task. """
        if decode.get("exp") and not data._login_done and data.auto_logout:
            data._create_task_login_update(decode)
        return decode

    except ExpiredSignatureError:
        data.logout(key_login)
        return False
    except InvalidKeyError:
        data.logout(key_login)
        return False
    except DecodeError as e:
        data.logout(key_login)
        raise LogoutError(
            "Decoding error, possibly there is a double use of the storage 'key', Secret key invalid! or ",
            e,
        )
    except FletEasyError:
        raise
    except Exception as e:
        data.logout(key_login)
        raise LogoutError("Login error:", e)


def decode(key_login: str, data: Datasy) -> Union[Dict[str, Any], bool]:
    """decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    if data.secret_key is None:
        raise SecretKeyError(
            "decode() requires 'secret_key' in FletEasy(). "
            "Example: FletEasy(secret_key=SecretKey(secret='your-secret', algorithm='HS256'))"
        )
    try:
        return _handle_decode_errors(
            jwt=data._storage_get(key_login), data=data, key_login=key_login
        )
    except TimeoutError as e:
        raise LoginError("Use the 'decode_async' method instead of 'decode'. | More details:", e)


async def decode_async(key_login: str, data: Datasy) -> Union[Dict[str, Any], bool]:
    """decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    if data.secret_key is None:
        raise SecretKeyError(
            "decode_async() requires 'secret_key' in FletEasy(). "
            "Example: FletEasy(secret_key=SecretKey(secret='your-secret', algorithm='HS256'))"
        )

    try:
        x = _handle_decode_errors(
            jwt=await data._storage_get_async(key_login), data=data, key_login=key_login
        )
        return x
    except TimeoutError as e:
        raise LoginError("Use the 'decode' method instead of 'decode_async'. | More details:", e)

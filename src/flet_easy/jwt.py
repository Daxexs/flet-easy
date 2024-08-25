import contextlib
from secrets import token_bytes
from typing import Any, Dict, Union

with contextlib.suppress(ImportError):
    from jwt import DecodeError, ExpiredSignatureError, InvalidKeyError

with contextlib.suppress(ImportError):
    from rsa import newkeys

from flet_easy.datasy import Datasy, evaluate_secret_key
from flet_easy.extra import Msg
from flet_easy.extrasJwt import _decode_payload_async


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


async def _handle_decode_errors(data: Datasy, key_login: str) -> Union[Dict[str, Any], bool]:
    """decodes the jwt and updates the browser sessions."""
    try:
        data._key_login = key_login
        evaluate_secret_key(data)

        if not await data.page.client_storage.contains_key_async(key_login):
            return False

        if data.auto_logout and not data._login_done:
            data.page.pubsub.send_others_on_topic(
                data.page.client_ip, Msg("updateLogin", value=data._login_done)
            )

        decode = await _decode_payload_async(
            page=data.page,
            key_login=key_login,
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
        data.logout(key_login)()
        return False
    except InvalidKeyError:
        data.logout(key_login)()
        return False
    except DecodeError as e:
        data.logout(key_login)()
        Exception(
            "Decoding error, possibly there is a double use of the 'client_storage' 'key', Secret key invalid! or ",
            e,
        )
        return False
    except Exception as e:
        data.logout(key_login)()
        raise Exception("Login error:", e)


def decode(key_login: str, data: Datasy) -> Dict[str, Any] | bool:
    """decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    assert not data._login_async, "Use the 'decode_async' method instead of 'decode'."
    assert data.secret_key is not None, "set the 'secret_key' in the class parameter (FletEasy)."

    return data.page.run_task(_handle_decode_errors, data, key_login).result()


async def decode_async(key_login: str, data: Datasy) -> Dict[str, Any] | bool:
    """decodes the jwt and updates the browser sessions.

    ### Parameters to use:
    * `key_login` : key used to store data in the client, also used in the `login` method of `Datasy`.
    * `data` : Instance object of the `Datasy` class.
    """
    assert data._login_async, "Use the 'decode' method instead of 'decode_async'."
    assert data.secret_key is not None, "set the 'secret_key' in the class parameter (FletEasy)."

    return await _handle_decode_errors(data, key_login)

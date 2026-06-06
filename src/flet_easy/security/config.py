from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Optional, Union

from flet_easy.exceptions import AlgorithmJwtError, JwtMissingError, SecretKeyError

DecodeError: type[Exception]
ExpiredSignatureError: type[Exception]
InvalidKeyError: type[Exception]

try:
    from jwt import DecodeError as _DecodeError
    from jwt import ExpiredSignatureError as _ExpiredSignatureError
    from jwt import InvalidKeyError as _InvalidKeyError
    from jwt import decode, encode

    DecodeError = _DecodeError
    ExpiredSignatureError = _ExpiredSignatureError
    InvalidKeyError = _InvalidKeyError
except ImportError:

    def decode(*args: Any, **kwargs: Any) -> Any:
        raise JwtMissingError()

    def encode(*args: Any, **kwargs: Any) -> Any:
        raise JwtMissingError()

    class _DecodeFallbackError(Exception):
        pass

    class _ExpiredSignatureFallbackError(Exception):
        pass

    class _InvalidKeyFallbackError(Exception):
        pass

    DecodeError = _DecodeFallbackError
    ExpiredSignatureError = _ExpiredSignatureFallbackError
    InvalidKeyError = _InvalidKeyFallbackError


@dataclass
class Algorithm:
    HS256 = "HS256"
    RS256 = "RS256"


@dataclass
class PemKey:
    private: str
    public: str


@dataclass
class SecretKey:
    """Correctly add the secret key in the `FletEasy` class parameter."""

    algorithm: str = "HS256"
    secret: Optional[str] = None
    pem_key: Optional[PemKey] = None
    Jwt: bool = False


def _time_exp(time_expiry: Optional[timedelta], payload: dict[str, Any]) -> dict[str, Any]:
    if time_expiry is not None:
        payload["exp"] = datetime.now(tz=timezone.utc) + time_expiry
    return payload


def encode_RS256(  # noqa: N802
    payload: dict[str, Any], private: str, time_expiry: Optional[timedelta] = None
) -> str:
    payload = _time_exp(time_expiry, payload)
    return encode(
        payload=payload,
        key=private,
        algorithm="RS256",
    )


def encode_HS256(  # noqa: N802
    payload: dict[str, Any], secret_key: str, time_expiry: Optional[timedelta] = None
) -> str:
    payload = _time_exp(time_expiry, payload)
    return encode(
        payload=payload,
        key=secret_key,
        algorithm="HS256",
    )


# Dispatch table for encode_verified — O(1) algorithm lookup
def _dispatch_rs256(
    secret_key: "SecretKey", value: dict[str, Any], time_expiry: Optional[timedelta]
) -> str:
    if secret_key.pem_key is None:
        raise SecretKeyError("RS256 requires pem_key in SecretKey.")
    return encode_RS256(payload=value, private=secret_key.pem_key.private, time_expiry=time_expiry)


def _dispatch_hs256(
    secret_key: "SecretKey", value: dict[str, Any], time_expiry: Optional[timedelta]
) -> str:
    if secret_key.secret is None:
        raise SecretKeyError("HS256 requires secret in SecretKey.")
    return encode_HS256(payload=value, secret_key=secret_key.secret, time_expiry=time_expiry)


_ENCODE_DISPATCH: dict[str, Callable[["SecretKey", dict[str, Any], Optional[timedelta]], str]] = {
    "RS256": _dispatch_rs256,
    "HS256": _dispatch_hs256,
}


def encode_verified(
    secret_key: SecretKey, value: dict[str, Any], time_expiration: Optional[timedelta]
) -> str:
    """Verify the possible encryption of the value sent."""
    if secret_key.algorithm is None:
        raise SecretKeyError(
            "secret_key.algorithm is None. Set algorithm='HS256' or algorithm='RS256' in SecretKey()."
        )

    handler = _ENCODE_DISPATCH.get(secret_key.algorithm)
    if handler is None:
        raise AlgorithmJwtError("Algorithm not implemented in encode_verified method.")

    return handler(secret_key, value, time_expiration)


def _decode_payload(
    jwt: str, secret_key: Optional[Union[str, Any]], algorithms: str
) -> dict[str, Any]:
    """Decodes the payload stored in the client storage."""
    if secret_key is None:
        raise SecretKeyError(
            "Cannot decode JWT: secret_key is None. "
            "Ensure FletEasy(secret_key=SecretKey(...)) is configured."
        )

    return decode(
        jwt=jwt,
        key=secret_key,
        algorithms=[algorithms],
    )

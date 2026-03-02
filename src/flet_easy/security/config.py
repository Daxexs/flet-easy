from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Union

from flet_easy.exceptions import AlgorithmJwtError, JwtMissingError, SecretKeyError

try:
    from jwt import decode, encode
except ImportError:

    def decode(*args, **kwargs):
        raise JwtMissingError()

    def encode(*args, **kwargs):
        raise JwtMissingError()


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
    secret: str = None
    pem_key: PemKey = None
    Jwt: bool = False


def _time_exp(time_expiry: timezone, payload: Dict[str, Any]) -> dict[str, Any]:
    if time_expiry is not None:
        payload["exp"] = datetime.now(tz=timezone.utc) + time_expiry
    return payload


def encode_RS256(payload: Dict[str, Any], private: str, time_expiry: timezone = None) -> str:
    payload = _time_exp(time_expiry, payload)
    return encode(
        payload=payload,
        key=private,
        algorithm="RS256",
    )


def encode_HS256(payload: Dict[str, Any], secret_key: str, time_expiry: timezone = None) -> str:
    payload = _time_exp(time_expiry, payload)
    return encode(
        payload=payload,
        key=secret_key,
        algorithm="HS256",
    )


def encode_verified(secret_key: SecretKey, value: str, time_expiration) -> Union[str, None]:
    """Verify the possible encryption of the value sent."""
    if secret_key.algorithm is None:
        raise SecretKeyError(
            "secret_key.algorithm is None. Set algorithm='HS256' or algorithm='RS256' in SecretKey()."
        )

    if secret_key.algorithm == "RS256":
        return encode_RS256(
            payload=value,
            private=secret_key.pem_key.private,
            time_expiry=time_expiration,
        )
    elif secret_key.algorithm == "HS256":
        return encode_HS256(
            payload=value,
            secret_key=secret_key.secret,
            time_expiry=time_expiration,
        )
    else:
        raise AlgorithmJwtError("Algorithm not implemented in encode_verified method.")


def _decode_payload(jwt: str, secret_key: str, algorithms: str) -> Dict[str, Any]:
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

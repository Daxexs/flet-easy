import contextlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict

from flet_easy.exceptions import AlgorithmJwtError

with contextlib.suppress(ImportError):
    from jwt import decode, encode


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


def encode_verified(secret_key: SecretKey, value: str, time_expiration) -> str | None:
    """Verify the possible encryption of the value sent."""
    assert (
        secret_key.algorithm is not None
    ), "The secret_key algorithm is not supported, only (RS256, HS256) is accepted."

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
    assert (
        secret_key is not None
    ), "The secret_key algorithm is not supported, only (RS256, HS256) is accepted."

    return decode(
        jwt=jwt,
        key=secret_key,
        algorithms=[algorithms],
    )

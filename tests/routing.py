from typing import Any, Dict, Optional
from uuid import UUID

import pytest

from flet_easy.route import FletEasyX


def custom_bool(value: str) -> Optional[bool]:
    """Return the value if it is equal to "true" or "false", otherwise return None."""
    return value.lower() == "true" if value.lower() in ["true", "false"] else None


def custom_code(value: str) -> Optional[str]:
    """Return the value if it is equal to "code5", otherwise return None."""
    if value == "code5":
        return value
    return None


def verify_uuid(value: str) -> Optional[UUID]:
    """Return the UUID object if the value is a valid UUID, otherwise return None."""
    try:
        return UUID(value)
    except ValueError:
        return None


@pytest.fixture
def setup() -> tuple[Dict[str, Any], Any]:
    custom_types = {"t": custom_bool}
    verify_url = FletEasyX._verify_url
    return custom_types, verify_url


def test_valid_cases(setup: tuple[Dict[str, Any], Any]) -> None:
    custom_types, verify_url = setup
    assert verify_url("/home/{id}", "/home/15") == {"id": "15"}
    assert verify_url("/home/<id>", "/home/15/") == {"id": "15"}
    assert verify_url("/home/{id:int}/<flag:bool>", "/home/1/True/") == {"id": 1, "flag": True}
    assert verify_url("/home/<id:int>/<flag:bool>", "/home/1/false/") == {"id": 1, "flag": False}
    assert verify_url("/home/<id:int>/<flag:bool>", "/home/1/False/") == {"id": 1, "flag": False}
    assert verify_url("/home/{id:int}/<flag:str>", "/home/1/true/") == {"id": 1, "flag": "true"}
    assert verify_url("/product/{price:float}", "/product/12.99/") == {"price": 12.99}
    assert verify_url("/product/{name}", "/product/Jvz/") == {"name": "Jvz"}
    assert verify_url("/home/<flag:code>", "/home/code5/", {"code": custom_code}) == {
        "flag": "code5"
    }
    assert verify_url("/", "/") == {}
    assert verify_url("/home", "/home/") == {}
    assert verify_url("/home/data", "/home/data") == {}
    assert verify_url("{id:int}", "/5") == {"id": 5}
    assert verify_url("/{id:int}/user", "/5/user") == {"id": 5}


def test_invalid_cases(setup: tuple[Dict[str, Any], Any]) -> None:
    custom_types, verify_url = setup
    assert verify_url("/home/{id:int}/<flag:bool>", "/home/abc/True/") is None
    assert verify_url("/home/{id:int}/<flag:bool>", "/home/1/invalid/") is None
    assert verify_url("/product/{price:int}", "/product/12.99/") is None
    assert verify_url("/home/<id:int>/<flag:code>", "/home/1/code1/", {"code": custom_code}) is None


def test_custom_type_usage(setup: tuple[Dict[str, Any], Any]) -> None:
    custom_types, verify_url = setup
    assert verify_url("/home/{id:int}/<flag:t>", "/home/1/true/", custom_types) == {
        "id": 1,
        "flag": True,
    }
    assert verify_url("/home/{id:int}/<flag:t>", "/home/1/false/", custom_types) == {
        "id": 1,
        "flag": False,
    }
    assert verify_url("/home/user", "/home/user") == {}
    assert verify_url(
        "user/{uuid:uuid_custom}",
        "/user/2c33e9a7-8d71-43b8-b959-b2eae113b5f8",
        custom_types={"uuid_custom": verify_uuid},
    ) == {"uuid": UUID("2c33e9a7-8d71-43b8-b959-b2eae113b5f8")}


def test_invalid_custom_type(setup: tuple[Dict[str, Any], Any]) -> None:
    custom_types, verify_url = setup
    with pytest.raises(ValueError):
        verify_url("/home/{id:int}/<flag:invalid>", "/home/1/true/", custom_types)
        verify_url("/home/{id:int}/<flag:count>", "/home/1/true/")
        verify_url("/home/{id}/{flag:int}", "/home/1/123", custom_types)
        verify_url("/home/{id:int}/<flag:str>", "/home/1/code5/")
        verify_url(
            "/home/{id:int}/<flag:codex>", "/home/1/code5/", custom_types={"code": custom_code}
        )
        verify_url("/home/{id:int}/<flag:codex>", "/home/1/code5/")
        verify_url("/home/{id}", "/home/15", custom_types={"code": custom_code})


def test_none_cases(setup: tuple[Dict[str, Any], Any]) -> None:
    custom_types, verify_url = setup
    assert verify_url("/home/{id:int}/<flag:bool>", "/home/1/") is None
    assert verify_url("/home/{id:int}/<flag:bool>", "/home/") is None
    assert verify_url("/home/{name:str}/ok", "/home/jr/okk") is None
    assert verify_url("/home/user", "/home/users") is None
    assert (
        verify_url(
            "user/{uuid:uuid_custom}",
            "/user/2c33e9a7-8d71-43b8-b959-b2eae113b5f8x",
            custom_types={"uuid_custom": verify_uuid},
        )
        is None
    )
    assert verify_url("{id:int}", "/home") is None
    assert verify_url("/{id:int}/user", "/5x/user") is None

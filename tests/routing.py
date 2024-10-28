import unittest
from uuid import UUID

from flet_easy.route import FletEasyX


def custom_bool(value: str):
    """Return the value if it is equal to "true" or "false", otherwise return None."""
    return value.lower() == "true" if value.lower() in ["true", "false"] else None


def custom_code(value: str):
    """Return the value if it is equal to "code5", otherwise return None."""
    if value == "code5":
        return value
    return


def verify_uuid(value: str):
    """Return the UUID object if the value is a valid UUID, otherwise return None."""
    try:
        return UUID(value)
    except ValueError:
        return


class TestVerifyURL(unittest.TestCase):
    def setUp(self):
        self.custom_types = {"t": custom_bool}
        self.verify_url = FletEasyX._verify_url

    def test_valid_cases(self):
        self.assertEqual(self.verify_url("/home/{id}", "/home/15"), {"id": "15"})
        self.assertEqual(self.verify_url("/home/<id>", "/home/15/"), {"id": "15"})
        self.assertEqual(
            self.verify_url("/home/{id:int}/<flag:bool>", "/home/1/True/"), {"id": 1, "flag": True}
        )
        self.assertEqual(
            self.verify_url("/home/<id:int>/<flag:bool>", "/home/1/false/"),
            {"id": 1, "flag": False},
        )
        self.assertEqual(
            self.verify_url("/home/<id:int>/<flag:bool>", "/home/1/False/"),
            {"id": 1, "flag": False},
        )
        self.assertEqual(
            self.verify_url("/home/{id:int}/<flag:str>", "/home/1/true/"), {"id": 1, "flag": "true"}
        )
        self.assertEqual(
            self.verify_url("/product/{price:float}", "/product/12.99/"), {"price": 12.99}
        )
        self.assertEqual(self.verify_url("/product/{name}", "/product/Jvz/"), {"name": "Jvz"})
        self.assertEqual(
            self.verify_url("/home/<flag:code>", "/home/code5/", {"code": custom_code}),
            {"flag": "code5"},
        )
        self.assertEqual(self.verify_url("/", "/"), {})
        self.assertEqual(self.verify_url("/home", "/home/"), {})
        self.assertEqual(self.verify_url("/home/data", "/home/data"), {})
        self.assertEqual(self.verify_url("{id:int}", "/5"), {"id": 5})
        self.assertEqual(self.verify_url("/{id:int}/user", "/5/user"), {"id": 5})

    def test_invalid_cases(self):
        self.assertIsNone(self.verify_url("/home/{id:int}/<flag:bool>", "/home/abc/True/"))
        self.assertIsNone(self.verify_url("/home/{id:int}/<flag:bool>", "/home/1/invalid/"))
        self.assertIsNone(self.verify_url("/product/{price:int}", "/product/12.99/"))
        self.assertIsNone(
            self.verify_url("/home/<id:int>/<flag:code>", "/home/1/code1/", {"code": custom_code})
        )

    def test_custom_type_usage(self):
        self.assertEqual(
            self.verify_url("/home/{id:int}/<flag:t>", "/home/1/true/", self.custom_types),
            {"id": 1, "flag": True},
        )
        self.assertEqual(
            self.verify_url("/home/{id:int}/<flag:t>", "/home/1/false/", self.custom_types),
            {"id": 1, "flag": False},
        )
        self.assertEqual(self.verify_url("/home/user", "/home/user"), {})
        self.assertEqual(
            self.verify_url(
                "user/{uuid:uuid_custom}",
                "/user/2c33e9a7-8d71-43b8-b959-b2eae113b5f8",
                custom_types={"uuid_custom": verify_uuid},
            ),
            {"uuid": UUID("2c33e9a7-8d71-43b8-b959-b2eae113b5f8")},
        )

    def test_invalid_custom_type(self):
        with self.assertRaises(ValueError):
            self.verify_url("/home/{id:int}/<flag:invalid>", "/home/1/true/", self.custom_types)
            self.verify_url("/home/{id:int}/<flag:count>", "/home/1/true/")
            self.verify_url("/home/{id}/{flag:int}", "/home/1/123", self.custom_types)
            self.verify_url("/home/{id:int}/<flag:str>", "/home/1/code5/")
            self.verify_url(
                "/home/{id:int}/<flag:codex>", "/home/1/code5/", custom_types={"code": custom_code}
            )
            self.verify_url("/home/{id:int}/<flag:codex>", "/home/1/code5/")
            self.verify_url("/home/{id}", "/home/15", custom_types={"code": custom_code})

    def test_none_cases(self):
        self.assertIsNone(self.verify_url("/home/{id:int}/<flag:bool>", "/home/1/"))
        self.assertIsNone(self.verify_url("/home/{id:int}/<flag:bool>", "/home/"))
        self.assertIsNone(self.verify_url("/home/{name:str}/ok", "/home/jr/okk"))
        self.assertIsNone(self.verify_url("/home/user", "/home/users"))
        self.assertIsNone(
            self.verify_url(
                "user/{uuid:uuid_custom}",
                "/user/2c33e9a7-8d71-43b8-b959-b2eae113b5f8x",
                custom_types={"uuid_custom": verify_uuid},
            )
        )
        self.assertIsNone(self.verify_url("{id:int}", "/home"))
        self.assertIsNone(self.verify_url("/{id:int}/user", "/5x/user"))


if __name__ == "__main__":
    unittest.main()

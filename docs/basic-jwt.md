# Basic JWT

JWT is a standard for securely transmitting data between parties in JSON format. It is composed of three parts: the header, the payload and the signature. It is commonly used for authentication and authorization in web applications and API services. JWTs are compact, self-contained and easy to use in distributed environments.

Flet-Easy contains a basic integration to use JWT in a simple and fast way, by integrating JWT in the app you can configure user session time, as well as an automatic session expiration. In order to add JWT we will need the following configurations.

In the [`FletEasy`](/flet-easy/0.2.0/how-to-use/#fleteasy) class we must configure the following parameters:

* The value of `auto_logout` is false by default (closes session automatically).
* To configure the `secret_key` it is necessary to use the `SecretKey` class of `FletEasy`.

## Configuration

### Algorithm HS256

```python title="main.py" hl_lines="6-9"
import flet_easy  as fs

app = fs.FletEasy(
    route_init="/login",
    route_login="/login",
    secret_key=fs.SecretKey(
        algorithm=fs.Algorithm.HS256,
        secret=SECRET_KEY
        ),
    auto_logout=True,  # Activates the automatic closing of the session.
)
```

### Algorithm RS256

!!! info
    To use the `RS256` algorithm You must have the [`cryptographic`](https://github.com/pyca/cryptography){:target="_blank"} library installed.

```python title="main.py" hl_lines="6-9"
import flet_easy  as fs

app = fs.FletEasy(
    route_init="/login",
    route_login="/login",
    secret_key=fs.SecretKey(
       algorithm=fs.Algorithm.RS256,
       pem_key=fs.PemKey(private=PRIVATE_KEY, public=PUBLIC_KEY)
    ),
    auto_logout=True,  # Activates the automatic closing of the session.
)
```

## Get `secret_key`

FletEasy provides a class called `EasyKey` to easily get a secret_key to use, then we can copy it to a file or use it as environment variables.

```python
import flet_easy as fs

key = fs.EasyKey()

# --- HS256
SECRET_KEY = key.secret_key()

# --- RS256
PRIVATE_KEY = key.private_key()
PUBLIC_KEY = key.public_key()
```

---

## How to use it

After having configured the `secret_key`, we can start configuring the use of JWT. For this we are going to require the use of the [`login`](/flet-easy/0.2.0/customized-app/route-protection/) method of `Datasy` (data), it will be used as normally we would use it without using JWT, but we will use the `time_expiry` and `value` parameter that will have to be a dictionary obligatorily.

* [More details of the `login` method](/flet-easy/0.2.0/customized-app/route-protection/#login)
* [More details of the `logout` method](/flet-easy/0.2.0/customized-app/route-protection/#logout)

### Example

```python title="sensitive.py"
SECRET_KEY = "7dbd00fd8ba528257c641b7c5c411cb5abdca774d348d36a3af86f644b132382a3f3f71361fd4e19d2d2dcbcee6f2769af84cbe372a3a5b9db35d3d2707e1d0a"

PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAmSNxQBBYOJEJD+XIDDBXK1qxUTpSsiybrtdvZH30f6G1o1MNsj17
Jjexf2ub7GO0J3TbDz4+dkEtVciG5cOG+bJ2RR2+09yIm3MC5xdRB12DaexU6EGd
EzbrZFiOxurzL3SSXzaABo/5DoLjk+eEF9YHhnnmoCjuAaV195PQ1Bkrn6h6kTpP
MtpJ5UIMVAFrtNNXPcii4P6ESn00kxcL55daVoKpyuC2hOiZFn9uQHoUrrtNGJGi
il6JjJPWWr/PU3RKdf++/QNsoJ2Erkob1FWz16+lIhJ2fsK6Qai6K0mXUqTPF5Hl
/Pi7zyw81fAgLE3bOdzVJAbBkMqKRvR9nQIDAQAB
-----END RSA PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEqQIBAAKCAQEAmSNxQBBYOJEJD+XIDDBXK1qxUTpSsiybrtdvZH30f6G1o1MN
sj17Jjexf2ub7GO0J3TbDz4+dkEtVciG5cOG+bJ2RR2+09yIm3MC5xdRB12DaexU
6EGdEzbrZFiOxurzL3SSXzaABo/5DoLjk+eEF9YHhnnmoCjuAaV195PQ1Bkrn6h6
kTpPMtpJ5UIMVAFrtNNXPcii4P6ESn00kxcL55daVoKpyuC2hOiZFn9uQHoUrrtN
GJGiil6JjJPWWr/PU3RKdf++/QNsoJ2Erkob1FWz16+lIhJ2fsK6Qai6K0mXUqTP
F5Hl/Pi7zyw81fAgLE3bOdzVJAbBkMqKRvR9nQIDAQABAoIBAQCCRZNGw2C5JjBG
VNvb+pd86xbimbHVnnsFvoElRLzkgmUpPjLtiL2lYkVdtuYaryqHUjI0AmhSYtm1
GvQeqzm8WqOf4lD+m6GeU7WJbt1gXZ24UvJb7c04lkSixW8YKrCbkxgdZRh9/KYL
QS9mF9HYERuvuy2E26wXWIwBJjQoB9BJpM6LA2+Pwb6Bygc6e/UOq981+BAY3bbq
PvRxfLk60xWLmtrS/O9HdGB0vNEvznG6X0+/v0a7Qv8AGd/sSU6cgowF+gyCwG9u
9uj7X6mEfNw5ZDUvJnH6wWRWfu+zeW4e18lA4GYiQwwXyciDey5T+RI/d4HgNyLn
h2SHLFmlAoGJALkDoPdvIUyuKkfe6zl2w1FV2uYF4RLdU9O632zI7Ts4dYnhJxkT
QOdjJaBFSEBwz7YdgMP8ZAWhOEfB582Bkt99mn7Q4YtARMnx44/Ex2CKN6jXr6OS
p8jxIuOfCd/rpMFVz0+SiqS7yWcTPdSbLPWFAu6KeYvfLMEHzi+Ah7r1UEk2k4HW
L+MCeQDT5O5460PFcZP+hSIsGT/mW5ChRmZS/7/ZB0zJQ9nB/SGtgD/AwAgusHRb
9+DherSehCHWcahRzDONy+UDXxuVzwSSweD4HJCG7tPykGDxEQmhSY56pShaAp1t
+u0UWD+Sn6jpEEsZzNsjaxCyzCMwem2Xrt5HFH8CgYgPRohsxYUnUp31Dye2t+KK
fZ80LLoXl6SLL7uwvKoxoIi72JYk0N0j/aCmqfG8OFQ+AhOWmukbOeNusUjVQ+R/
hVxTKiXlHGpRjiIuxZ18kAzmaOB8jehCg/5Qctoa3dbdi5sxQ7UkwshvNTx+qE0+
/DtwvIgqj0OfsGhKrb8HJaf6U4I8TxXnAnhVh/VSzfR/QIdyl57hmheXDqLk1pv7
KMzx9+Zg34iIq3rqo/gX/+vNnOB7NyWJHpTF36QhAaPl0L2GoSUCJWPnJrc73hLH
VBBqxwC6yti2th/jAOQIUZ5mJuQRPtZv/ec7ckMmQLNv6KcUNuV4proVmXWfYrDK
lFUCgYg62k/vLCnHlnl7PwMb9BJAVyxuWPjihhfKJx3i371/iQn+bHD86PnsfRUO
BfJI9TjPn2k1r+R4AxSzFOr0ZwmusjfyklzJS77wAaAaH9xvfEFLCqtbfZv+w3oh
Kzuz8LYM/PJmIWIBTo2mqDwp/Iv2EbMKw0Jjn0cgnZINs9UciQqhxX4R49I3
-----END RSA PRIVATE KEY-----"""
```

In this example we are going to do very similar with the [`Route-protection`](/flet-easy/0.2.0/customized-app/route-protection/#example) example, we have only configured the `secret_key`, used the [`login`](/flet-easy/0.2.0/customized-app/route-protection/#login) method `time_expiry` parameter and used the [`decode`](/flet-easy/0.2.0/basic-jwt/#decode) function of `FletEasy` to get the payload stored in the decoded client storage.

```python title="main.py"  hl_lines="12-15 22 42 65-70 78"
from datetime import timedelta

import flet as ft
import flet_easy as fs
from sensitive import SECRET_KEY

db = []

app = fs.FletEasy(
    route_init="/login",
    route_login="/login",
    secret_key=fs.SecretKey(
        algorithm=fs.Algorithm.HS256,
        secret=SECRET_KEY
        ),
    auto_logout=True,  # Activates the automatic closing of the session.
)

@app.login
def login_x(data: fs.Datasy):
    # decode payload
    value = fs.decode(key_login="login", data=data)

    print("value:", value)

    """ We verify if the username that is stored in the browser is in the
    simulated database. """
    if not value:
        return False
    elif value.get("user") in db:
        return True


@app.page(route="/dashboard", title="Dashboard", protected_route=True)
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton(
                "Logaut",
                on_click=data.logout("login")
                ),
            ft.ElevatedButton(
                "Home",
                on_click=data.go("/login")
                ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username", width=200)

    def store_login(e):
        db.append(username.value)  # We add to the simulated database

        """First the values must be stored in the browser, then in the
        login decorator the value must be retrieved through the key used
        and then validations must be used."""
        data.login(
            key="login",
            value={"user": username.value},
            next_route="/dashboard",
            time_expiry=timedelta(seconds=10),
        )

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton(
                "store login in browser",
                on_click=store_login
                ),
            ft.ElevatedButton(
                "go Dasboard",
                on_click=data.go("/dashboard")
                ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

### 🎬 **Demo**

**APP**
![alt video](assets/gifs/jwt-app.gif "jwt")

**WEB**
![alt video](assets/gifs/jwt-web.gif "jwt")

## decode

Decode the jwt and update the browser sessions.

**Parameters to use:**

* `key_login` : key used to store the data in the client, also used in the [`login`](/flet-easy/0.2.0/customized-app/route-protection/#login) method of [`Datasy`](/flet-easy/0.2.0/how-to-use/#datasy-data).
* `data` : Object instance of the [`Datasy`](/flet-easy/0.2.0/how-to-use/#datasy-data) class.

!!! info
    *Support async, example: `decode_async`.
    * If the function to use is async it is recommended to use `decode_async` to avoid errors.

!!! note
    The `decode` and `decode_async` functions can be used in other parts of the code, for example: [Middleware](/flet-easy/0.2.0/middleware/)

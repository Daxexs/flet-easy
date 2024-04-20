In order to configure the protection of routes, the `login` decorator of the created object of the app is used. The utility of this decorator is to obtain the values that we have previously registered in the `page.client_storage` [(more details here)](https://flet.dev/docs/guides/python/client-storage), then you can perform validations with a database or any data manager used.

Decorator to add a login configuration to the app (`protected_route`):

* The decorator function must receive a mandatory parameter, for example: `data:fs.Datasy`. Which can be used to get information and perform universal settings of the app.
* The decorator function must return a boolean.
  
### Example
!!! example ""
    In this case it is a basic example, with a test on a fictitious database.

```python hl_lines="11 13 19 25 32 41"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(
    route_init="/login",
    route_login="/login"
    )

db = []  # Database

@app.login
def login_x(data: fs.Datasy):
    username = data.page.client_storage.get("login")
    if username is not None and username in db:  # We check if a value exists with the key login
        # We verify if the username that is stored in the browser is in the simulated database.
        return True
    return False

@app.page(route="/dashboard", title="Dashboard", protected_route=True)
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=data.logout("login")),
            ft.ElevatedButton("Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username")

    def store_login(e):
        db.append(username.value)  # We add to the simulated database

        """First the values must be stored in the browser, then in the login decorator the value must be retrieved through the key used and then validations must be used."""
        data.login(key="login", value=username.value, next_route="/dashboard")

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton("store login in browser", on_click=store_login),
            ft.ElevatedButton("go Dasboard", on_click=data.go("/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```
### 🎬 **Mode**
![alt video](../assets/gifs/protected-route.gif "protected route")

## login
Registering in the client's storage the key and value in all browser sessions.

**Parameters `data.login`:**

* `key` : It is the identifier to store the value in the client storage.
* `value` : Recommend to use a dict if you use JWT.
* `next_route` : Redirect to next route after creating login.
* `time_expiry` : Time to expire the session, use the `timedelta` class  to configure. (Optional) (JWT usage required)
* `sleep` : Time to do login checks, default is 1s. (Optional) (JWT usage required)

## logout
Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method.

**Parameters `data.logout`:**

* `key` : It is the identifier to store the value in the client storage.

# Middleware

It acts as an intermediary between different software components, intercepting and processing requests and responses. Allows adding functionalities before reloading each page in a flexible and modular way. It adds common functionalities, such as authentication, logging, data compression, caching, error handling, data transformation, etc.

The function that will act as middleware will receive as a single mandatory parameter [`data: Datasy`](/flet-easy/0.2.0/how-to-use/#datasy-data) and its structure or content may vary depending on the context and specific requirements of the middleware.

## **Method and attribute to use** [[`See more`](/flet-easy/0.2.0/how-to-use/#datasy-data)]

* `data.route` : to know the route that is loading.
* `data.redirect()` : route to redirect.

!!! note
    If the function returns None, it will not prevent the page from loading that the route is accessing.

!!! info
    Several functions can be used at the same time in the Middleware, since a list of functions is entered.

## General Application

Another alternative to protected-route

```python hl_lines="4 12 15 20 24 34 56"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/login", route_login="/login")

db = []  # Database

# -------------------------------------------------------------------------------


# Customized middleware
async def login_middleware(data: fs.Datasy):
    """ If the path is '/login', it will return the None function,
    which will not prevent access to the page. """
    if data.route == "/login":
        return

    username = await data.page.client_storage.get_async("login")
    if username is None or username not in db:
        return data.redirect("/login")


# Middleware that runs in general, i.e. every time you load a page.
app.add_middleware([login_middleware])
# -------------------------------------------------------------------------------


@app.page(route="/dashboard", title="Dashboard")
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=data.logout("login")),
            ft.ElevatedButton("go Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# -------------------------------------------------------------------------------


@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username")

    def store_login(e):
        db.append(username.value)  # We add to the simulated databas

        """First the values must be stored in the browser, then in the
        login decorator the value must be retrieved through the key used
        and then validations must be used."""
        data.login(key="login", value=username.value, next_route="/dashboard")

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton("store login in browser", on_click=store_login),
            ft.ElevatedButton("go Dashboard", on_click=data.go("/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


app.run()
```

## 🎬 **Demo**

![alt video](../assets/gifs/protected-route.gif "Middleware")

## For each page

Another alternative to protected-route

```python hl_lines="4 12 14 18 24 44"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/login", route_login="/login")

db = []  # Database

# -------------------------------------------------------------------------------

# Customized middleware
async def login_middleware(data: fs.Datasy):
    username = await data.page.client_storage.get_async("login")
    if username is None or username not in db:
        return data.redirect("/login")

# -------------------------------------------------------------------------------
# Middleware used to load this page
@app.page(route="/dashboard", title="Dashboard", middleware=[login_middleware])
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=data.logout("login")),
            ft.ElevatedButton("go Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# -------------------------------------------------------------------------------

@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username")

    def store_login(e):
        db.append(username.value)  # We add to the simulated databas

        """First the values must be stored in the browser, then in the
        login decorator the value must be retrieved through the key used
        and then validations must be used."""
        data.login(key="login", value=username.value, next_route="/dashboard")

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton("store login in browser", on_click=store_login),
            ft.ElevatedButton("go Dashboard", on_click=data.go("/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

## 🎬 **Demo**

![alt video](../assets/gifs/protected-route.gif "Middleware")

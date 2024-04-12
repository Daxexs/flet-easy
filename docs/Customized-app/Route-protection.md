In order to configure the protection of routes, the `login` decorator of the created object of the app is used. The utility of this decorator is to obtain the values that we have previously registered in the `page.client_storage` [(more details here)](https://flet.dev/docs/guides/python/client-storage), then you can perform validations with a database or any data manager used.

Decorator to add a login configuration to the app (protected_route):

* The decorator function must receive a mandatory parameter, for example: `page:ft.Page`. Which can be used to get information and perform universal settings of the app.
* The decorator function must return a boolean.
  
### Example
!!! example ""
    In this case it is a basic example, with a test on a fictitious database.

```python hl_lines="12 14 29 53"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(
    route_init="/login",
    route_login="/login"
)

db = [] # Database


@app.login
def login_x(page: ft.Page):
    username = page.client_storage.get("login")
    if username is not None:  # We check if a value exists with the key login
        # We verify if the username that is stored in the browser is in the simulated database.
        if username in db:
            return True
    return False


@app.page(route="/dashboard", protected_route=True)
def dashboard_page(data: fs.Datasy):
    page = data.page
    page.title = "Dashboard"

    def logaut(e):
        # We delete the key that we have previously registered
        page.client_storage.remove('login')
        page.go('/login')

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Text("Dash", size=30),
            ft.ElevatedButton('Logaut', on_click=logaut)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@app.page(route="/login")
def login_page(data: fs.Datasy):
    page = data.page
    page.title = "Login"

    # create login stored user
    username = ft.TextField(label='Username')

    def store_login(e):
        """ First the values must be stored in the browser, then in the login decorator the value must be retrieved through the key used and then validations must be used. """
        page.client_storage.set(key='login', value=username.value)

        db.append(username.value)  # We add to the simulated database

    return ft.View(
        route="/login",
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton('store login in browser', on_click=store_login),
            ft.ElevatedButton("go", on_click=lambda _: page.go("/dashboard"))
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


app.run()
```

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
        ]
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
        ]
    )


app.run()

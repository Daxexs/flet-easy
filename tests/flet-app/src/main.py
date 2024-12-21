from pathlib import Path

from core.config import ConfigApp

# from core.sensitive import PRIVATE_KEY, PUBLIC_KEY
from core.sensitive import SECRET_KEY

import flet_easy as fs

app = fs.FletEasy(
    route_init="/home",
    route_login="/login",
    secret_key=fs.SecretKey(algorithm=fs.Algorithm.HS256, secret=SECRET_KEY),
    auto_logout=True,
    path_views=Path(__file__).parent / "views",
    on_Keyboard=True,
)


def starting_page(data: fs.Datasy):
    """Remove [print()] from Python if build Windows"""
    pass
    # print(f"\n⚡[MIDDLEWARES RUNNING]\n-> Route:{data.route}\n1. Loading the page")


async def starting_page_two(data: fs.Datasy):
    """Remove [print()] from Python if build Windows"""
    # ("2. Loading the page")

    # We allow the following paths, otherwise it redirects to the path ('/login').
    # Note: To check the urls you should use (data.route) and not (data.page.route), as this will cause an infinite loop.
    routes = [
        "/login",
        "/register",
        "/home",
        "/share/send-data",
        "/dashboard",
        "/counter/test/{id:int}",
        "/counter/use-keyboard/{id:int}",
        "/counter/ts",
    ]
    if data.route not in routes:
        print("-> Redirection to path (/login)")
        return data.redirect("/login")


""" [If you have any problem - build Windows]
Remove [print()] from Python if used in 'add_middleware' functions. """
app.add_middleware([starting_page, starting_page_two])

ConfigApp(app)

# We run the application web
# run =app.run(export_asgi_app=True)

""" [If you have any problem - build web]
Use ft.app(target=app.get_app()) when compiling web statica. """
app.run()

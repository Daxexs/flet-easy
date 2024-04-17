from pathlib import Path

import flet_easy as fs
from core.config import ConfigApp

# from core.sensitive import PRIVATE_KEY, PUBLIC_KEY
from core.sensitive import SECRET_KEY
from models import create_tables

create_tables()
app = fs.FletEasy(
    route_init="/home",
    route_login="/login",
    secret_key=fs.SecretKey(algorithm=fs.Algorithm.HS256, secret=SECRET_KEY),
    auto_logout=True,
    path_views=Path(__file__).parent / "views",
)


def starting_page(data: fs.Datasy):
    print(f"\n⚡[MIDLEWARE RUNNING]\n-> Route:{data.route}\n1. Loading the page")


async def starting_page_two(data: fs.Datasy):
    print("2. Loading the page")
    # We allow the following paths, otherwise it redirects to the path ('/login').
    # Note: To check the urls you should use (data.route) and not (data.page.route), as this will cause an infinite loop.
    routes = ["/login", "/register", "/home", "/share/send-data", "/dashboard"]
    if data.route not in routes:
        print("-> Redirection to path (/login)")
        return data.redirect("/login")


app.add_middleware([starting_page, starting_page_two])
ConfigApp(app)

# We run the application
# run =app.run(export_asgi_app=True)
app.run()

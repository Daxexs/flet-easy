import flet_easy as fs
import flet_fastapi
from view import counter, index, login, markdown, keyboard, response, task, test, pbs

from core.config import ConfigApp
from pathlib import Path

# from view import (
#    index_page,
#    test_page,
#    counter_page,
#    login_page,
#    task_page,
#    markdown_page,
#    response_page,
#    keyboard_page
# )

ROUTE = "/tools"

""" we create the app object, in it you can configure:
* The path that is different from '/'.
* The initial path when initializing the app
* The path that will be redirected when the app has path protection configured.
"""
app = fs.FletEasy(
    route_prefix=ROUTE,
    route_init=f"{ROUTE}/index",
    route_login=f"{ROUTE}/login/user",
    on_Keyboard=True,
    on_resize=True,
)

"""" Add pages from other archives:
* In the list you enter objects of class `AddPagesy` from other .py files.
"""
app.add_pages([index, counter, login, markdown, keyboard, response, task, test, pbs])

""" -> Add routes without the use of decorators.""" ""
# app.add_routes(add_views=[
#    fs.Pagesy('/hi', index_page, True),
#    fs.Pagesy('/test/{id:d}/user/{name:l}', test_page, protected_route=True),
#    fs.Pagesy('/counter', counter_page),
#    fs.Pagesy('/task', task_page),
#    fs.Pagesy('/login/user', login_page),
#    fs.Pagesy('/markdown', markdown_page),
#    fs.Pagesy('/response', response_page),
#    fs.Pagesy('/keyboard', keyboard_page),
# ])

""" Add app configuration:
* If you want to add the general configuration of the app, in a more orderly way, this is an alternative, we just pass the `app` object to the class where the configurations are going to be made.
"""
ConfigApp(app)

assets = Path(__file__).resolve().parent / "assets"
""" Execute the app through flet_fastapi (async)"""
run = flet_fastapi.app(
    app.fastapi(),
    app_name="Flet Easy",
    app_short_name="Easy app",
    app_description="test Flet-Easy",
    assets_dir=assets,
    use_color_emoji=True,
)
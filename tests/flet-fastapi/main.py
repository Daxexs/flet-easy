from pathlib import Path

from core.config import ConfigApp
from flet import fastapi

import flet_easy as fs

ROUTE = "/tools"

app = fs.FletEasy(
    route_prefix=ROUTE,
    route_init=f"{ROUTE}/index",
    route_login=f"{ROUTE}/login/user",
    on_Keyboard=True,
    on_resize=True,
    path_views=Path(__file__).parent / "views",
)

""" Add app configuration:
* If you want to add the general configuration of the app, in a more orderly way, this is an alternative, we just pass the `app` object to the class where the configurations are going to be made.
"""
ConfigApp(app)

assets = Path(__file__).resolve().parent / "assets"
""" Execute the app through flet_fastapi (async)"""
run = fastapi.app(
    session_handler=app.get_app(),
    app_short_name="Easy app",
    app_description="test Flet-Easy",
    assets_dir=assets,
    use_color_emoji=True,
)

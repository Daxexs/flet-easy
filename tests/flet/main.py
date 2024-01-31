import flet_easy as fs
import flet as ft
from views.index import index
from views.counter import counter
from views.share import share
from core.config import ConfigApp

app = fs.FletEasy(
    route_init="/home"
)

app.add_pages([index, counter, share])
ConfigApp(app)

# We run the application
app.run(view=ft.AppView.WEB_BROWSER)

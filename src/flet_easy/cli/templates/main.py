import flet as ft
import flet_easy as fs
from core.config import ConfigApp
from views import counter, index

app = fs.FletEasy(route_init="/home")

app.add_pages(
    [
        index,
        counter,
    ]
)
ConfigApp(app)

# We run the application
app.run(view=ft.AppView.WEB_BROWSER)

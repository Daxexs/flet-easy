import flet as ft
import flet_easy as fs
from components import Drawer

index = fs.AddPagesy()


# We add a page


@index.page(route="/home", title="Flet-Easy")
async def index_page(data: fs.Datasy):
    view = data.view
    return ft.View(
        controls=[
            ft.Text("Home page"),
            Drawer(text="Show_drawer", drawer=view.drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
    )

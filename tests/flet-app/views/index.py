import flet as ft
from components import Drawer

import flet_easy as fs


# We add a page
@fs.page(route="/home", title="Flet-Easy")
async def index_page(data: fs.Datasy):
    view = data.view
    return ft.View(
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go keyboard", on_click=data.go("/counter/use-keyboard/10")),
            Drawer(text="Show_drawer", drawer=view.drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
        appbar=view.appbar,
    )

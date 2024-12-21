import flet as ft
from components import Drawer

import flet_easy as fs

dashboard = fs.AddPagesy(
    route_prefix="/dashboard",
)


# We add a second page
@dashboard.page(route="/", title="Dashboard", protected_route=True)
async def dasboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("DASHBOARD", size=30),
            Drawer(text="Show_drawer", drawer=data.view.drawer),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        drawer=data.view.drawer,
        appbar=data.view.appbar,
    )

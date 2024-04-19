import flet as ft
import flet_easy as fs
from components import Counter, Drawer

counter = fs.AddPagesy(
    route_prefix="/counter",
)


async def check_params(data: fs.Datasy):
    print("+ Params Counter id:", data.url_params.get("id"))
    if data.url_params.get("id") == 10:
        return data.redirect("/share/send-data")


# We add a second page
@counter.page(route="/test/{id:d}", title="Counter", middleware=[check_params])
async def counter_page(data: fs.Datasy, id: str):
    view = data.view

    return ft.View(
        controls=[
            Counter(data.on_resize, id=id),
            Drawer(text="Show_drawer", drawer=view.drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
    )

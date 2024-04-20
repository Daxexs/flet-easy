import flet as ft
import flet_easy as fs
from components import Counter, SwoDrawer

counter = fs.AddPagesy(
    route_prefix="/counter",
)


# We add a second page
@counter.page(route="/test/{id}", title="Counter")
def counter_page(data: fs.Datasy, id: str):
    page = data.page
    view = data.view

    return ft.View(
        controls=[Counter(page=page, id=id, width=250), SwoDrawer("Show_drawer", view.drawer)],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
    )

import flet as ft
import flet_easy as fs

counter = fs.AddPagesy(
    route_prefix='/counter',
)

# We add a second page
@counter.page(route='/test/{id}')
async def counter_page(data: fs.Datasy, id: str):
    page = data.page
    view = data.view

    page.title = "Counter"

    txt_number = ft.TextField(value=id, text_align="right", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def show_drawer(e):
        view.drawer.open = True
        page.update()

    return ft.View(
        route="/counter",
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment="center",
            ),
            ft.FilledButton(
                "Go to Home",
                key=data.route_init,
                on_click=data.go
            ),
            ft.FilledButton("Show_drawer", on_click=show_drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer
    )

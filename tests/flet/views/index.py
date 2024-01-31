import flet as ft
import flet_easy as fs

index = fs.AddPagesy()

# We add a page


@index.page(route="/home")
def index_page(data: fs.Datasy):
    page = data.page
    view = data.view

    page.title = "Flet-Easy"

    def show_drawer(e):
        view.drawer.open = True
        page.update()

    return ft.View(
        route="/",
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter",
                            key='/counter/test/15', on_click=data.go),
            ft.FilledButton("Show_drawer", on_click=show_drawer),
            ft.FilledButton("Share data", key='/send-data', on_click=data.go),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
    )

import flet as ft
import flet_easy as fs

index = fs.AddPagesy()

# We add a page
@index.page(route="/home")
def index_page(data: fs.Datasy):
    page = data.page
    view = data.view

    page.title = "Flet-Easy"

    def go_counter(e):
        page.go(f"{data.route_prefix}/counter/test/15")
    
    def show_drawer(e):
        view.drawer.open = True
        page.update()

    return ft.View(
        route="/",
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter", on_click=go_counter),
            ft.FilledButton("Show_drawer", on_click=show_drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
    )
import flet as ft
import flet_easy as fs

index = fs.AddPagesy()

# We add a page
@index.page(route="/home")
async def index_page(data: fs.Datasy):
    page = data.page

    page.title = "Flet-Easy"

    async def go_counter(e):
        await page.go_async(f"{data.route_prefix}/counter/test/15")

    return ft.View(
        route="/",
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter", on_click=go_counter),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
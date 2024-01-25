import flet_easy as fs
import flet as ft
from uuid import UUID

ROUTE = "/index"

test = fs.AddPagesy(route_prefix="/test")


@test.page("/{id:d}/user/{name:l}", proctect_route=True)
async def test_page(data: fs.Datasy, id: int, name: str):
    page = data.page
    view = data.view

    page.title = "Test"
    view.appbar.title = ft.Text("test")

    async def go_index(e):
        await page.go_async(f"{ROUTE}/hi")

    return ft.View(
        "/test",
        controls=[
            ft.Text(f"Test {data.url_params}"),
            ft.Text(f"Test Id is: {id}"),
            ft.ElevatedButton("Go to Home", on_click=go_index),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def is_uuid(value):
    try:
        UUID(value)
        return value
    except ValueError:
        return False


@test.page("/get-params/{time:%Y/%m/%d}/{uuid:Uuid}", custom_params={"Uuid": is_uuid})
def get_params_page(data: fs.Datasy, time: str, uuid: UUID):
    page = data.page
    view = data.view
    on_resize = data.on_resize

    page.title = "Get params"
    view.appbar.title = ft.Text("Get params")

    return ft.View(
        route=f"{data.route_prefix}/test/get-params",
        controls=[
            ft.Container(
                content=ft.Text(
                    f"Date:\n{time}\n\nUuid:\n{uuid}",
                    size=30,
                    text_align=ft.TextAlign.CENTER,
                ),
                height=on_resize.heightX(50),
                width=on_resize.widthX(50),
                bgcolor=ft.colors.BROWN_500,
                alignment=ft.alignment.center,
                border_radius=10,
            )
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

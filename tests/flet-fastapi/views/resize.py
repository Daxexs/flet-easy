import flet as ft

import flet_easy as fs

markdown = fs.AddPagesy()


@markdown.page("/resize", title="On-resize")
async def markdown_page(data: fs.Datasy):
    view = data.view
    on_resize = data.on_resize

    view.appbar.title = ft.Text("On-resize")

    on_resize.margin_y = 28

    return ft.View(
        controls=[
            ft.Container(bgcolor=ft.Colors.GREEN_600, height=on_resize.heightX(50)),
            ft.Container(
                bgcolor=ft.Colors.BLUE_600,
                height=on_resize.heightX(50),
                width=on_resize.widthX(50),
            ),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        spacing=0,
    )

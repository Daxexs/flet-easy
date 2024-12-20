import flet as ft

import flet_easy as fs

index = fs.AddPagesy()


@index.page("/index", title="Home", page_clear=True)
async def index_page(data: fs.Datasy):
    view = data.view

    view.appbar.title = ft.Text("Home - Test [Flet-Easy]")

    return ft.View(
        controls=[
            ft.Text("Menú", size=40),
            ft.ElevatedButton(
                "Go to Test",
                on_click=data.go(f"{data.route_prefix}/test/10/user/junior"),
            ),
            ft.ElevatedButton(
                "Go to Test (get-params)",
                on_click=data.go(
                    f"{data.route_prefix}/test/get-params/25-11-2024/550e8400-e29b-41d4-a716-446655440000"
                ),
            ),
            ft.ElevatedButton(
                "Go to Contador",
                on_click=data.go(
                    f"{data.route_prefix}/counter",
                ),
            ),
            ft.ElevatedButton("Go to Task", on_click=data.go(f"{data.route_prefix}/task")),
            ft.ElevatedButton(
                "Go to Resize",
                on_click=data.go(f"{data.route_prefix}/resize"),
            ),
            ft.ElevatedButton(
                "Go to Response",
                on_click=data.go(f"{data.route_prefix}/response"),
            ),
            ft.ElevatedButton(
                "Go to keyboard Test",
                on_click=data.go(f"{data.route_prefix}/keyboard"),
            ),
            ft.ElevatedButton(
                "Go to Chat",
                on_click=data.go(f"{data.route_prefix}/chat"),
            ),
            ft.ElevatedButton("Go to Login", on_click=data.go(data.route_login)),
            ft.ElevatedButton(
                "Go to send-data",
                on_click=data.go(f"{data.route_prefix}/test/send-data"),
            ),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

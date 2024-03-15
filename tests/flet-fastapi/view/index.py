import flet_easy as fs
import flet as ft

index = fs.AddPagesy()


@index.page("/index", title="Home", page_clear=True)
async def index_page(data: fs.Datasy):
    view = data.view

    view.appbar.title = ft.Text("Home - Test [Flet-Easy]")

    return ft.View(
        "/tools/index",
        controls=[
            ft.Text("Menú", size=40),
            ft.ElevatedButton(
                "Go to Test",
                key=f"{data.route_prefix}/test/10/user/junior",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to Test (get-params)",
                key=f"{data.route_prefix}/test/get-params/2023/11/25/550e8400-e29b-41d4-a716-446655440000",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to Contador",
                key=f"{data.route_prefix}/counter",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to Task", key=f"{data.route_prefix}/task", on_click=data.go
            ),
            ft.ElevatedButton(
                "Go to Resize",
                key=f"{data.route_prefix}/markdown",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to Response",
                key=f"{data.route_prefix}/response",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to keyboard Test",
                key=f"{data.route_prefix}/keyboard",
                on_click=data.go,
            ),
            ft.ElevatedButton(
                "Go to Chat",
                key=f"{data.route_prefix}/chat",
                on_click=data.go,
            ),
            ft.ElevatedButton("Go to Login", key=data.route_login, on_click=data.go),
            ft.ElevatedButton(
                "Go to send-data",
                key=f"{data.route_prefix}/test/send-data",
                on_click=data.go,
            ),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

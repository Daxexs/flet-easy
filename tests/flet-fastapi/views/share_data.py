from dataclasses import dataclass

import flet as ft

import flet_easy as fs

data = fs.AddPagesy(route_prefix="/data")


@dataclass
class Test:
    name: int
    version: str


@data.page("/", title="Data", share_data=True)
async def get_data_page(data: fs.Datasy):
    view = data.view

    view.appbar.title = ft.Text("Data")

    # It is checked if there is data stored in the dictionary (data.share.set).
    if data.share.contains():
        x: Test = data.share.get("test")
        y: str = data.share.get("owner")
        res = ft.Text(f"Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}")
    else:
        res = ft.Text("No value passed on the page!.")

    return ft.View(
        controls=[
            ft.Container(content=res, padding=20, border_radius=20, bgcolor=ft.Colors.BLACK26),
            ft.ElevatedButton(
                "Check the following page for matched data",
                on_click=data.go(f"{data.route_prefix}/data/info"),
            ),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@data.page("/info", title="Information")
async def info_page(data: fs.Datasy):
    view = data.view

    view.appbar.title = ft.Text("Information")

    # It is checked if there is data stored in the dictionary (data.share.set).
    if data.share.contains():
        x: Test = data.share.get("test")
        y: str = data.share.get("owner")
        res = ft.Text(f"Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}")
    else:
        res = ft.Text("No value passed on the page!.")

    return ft.View(
        controls=[
            ft.Text("Access to shared data?"),
            ft.Container(content=res, padding=20, border_radius=20, bgcolor=ft.Colors.BLACK26),
        ],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

from dataclasses import dataclass

import flet as ft
from components import Drawer

import flet_easy as fs

share = fs.AddPagesy(route_prefix="/share")


@dataclass
class Test:
    name: int
    version: str


def is_shared_preference():
    return hasattr(ft, "SharedPreferences")


@share.page("/send-data", title="Send Data", share_data=True)
async def send_data_page(data: fs.Datasy):

    if is_shared_preference():
        # support shared_preferences flet >= 0.80.*
        await data.share.set("test", Test("Flet-Easy", "0.1"))
        await data.share.set("owner", "Daxexs")
    else:
        # support shared_preferences flet < 0.80.*
        data.share.set("test", Test("Flet-Easy", "0.1"))
        data.share.set("owner", "Daxexs")

    def go_data(e):
        data.go_route("/share/data")

    if is_shared_preference():
        # support shared_preferences flet >= 0.80.*
        keys = await data.share.get_keys()
        values = await data.share.get_values()
        all_data = await data.share.get_all()
    else:
        # support shared_preferences flet < 0.80.*
        keys = data.share.get_keys()
        values = data.share.get_values()
        all_data = data.share.get_all()

    return ft.View(
        controls=[
            ft.Text(f"data keys: {keys}"),
            ft.Text(f"data values: {values}"),
            ft.Text(f"data dict: {all_data}"),
            ft.ElevatedButton("View shared data", on_click=go_data),
            Drawer("Show_drawer", drawer=data.view.drawer),
        ],
        drawer=data.view.drawer,
        appbar=data.view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@share.page("/data", title="Data", share_data=True)
async def get_data_page(data: fs.Datasy):
    # It is checked if there is data stored in the dictionary (data.share.set).
    if is_shared_preference():
        # support shared_preferences flet >= 0.80.*
        has_data = await data.share.contains()
    else:
        # support shared_preferences flet < 0.80.*
        has_data = data.share.contains()

    if has_data:
        if is_shared_preference():
            # support shared_preferences flet >= 0.80.*
            x: Test = await data.share.get("test")
            y: str = await data.share.get("owner")
        else:
            # support shared_preferences flet < 0.80.*
            x: Test = data.share.get("test")
            y: str = data.share.get("owner")
        res = ft.Text(f"Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}")
    else:
        res = ft.Text("No value passed on the page!.")

    return ft.View(
        controls=[
            ft.Container(content=res, padding=20, border_radius=20, bgcolor=ft.Colors.BLACK26),
            ft.ElevatedButton(
                "Check the following page for matched data", on_click=data.go("/share/info")
            ),
            Drawer("Show_drawer", drawer=data.view.drawer),
        ],
        drawer=data.view.drawer,
        appbar=data.view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@share.page("/info", title="Information")
async def info_page(data: fs.Datasy):
    # It is checked if there is data stored in the dictionary (data.share.set).
    if is_shared_preference():
        # support shared_preferences flet >= 0.80.*
        has_data = await data.share.contains()
    else:
        # support shared_preferences flet < 0.80.*
        has_data = data.share.contains()

    if has_data:
        if is_shared_preference():
            # support shared_preferences flet >= 0.80.*
            x: Test = await data.share.get("test")
            y: str = await data.share.get("owner")
        else:
            # support shared_preferences flet < 0.80.*
            x: Test = data.share.get("test")
            y: str = data.share.get("owner")
        res = ft.Text(f"Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}")
    else:
        res = ft.Text("No value passed on the page!.")

    return ft.View(
        controls=[
            ft.Text("Access to shared data?"),
            ft.Container(content=res, padding=20, border_radius=20, bgcolor=ft.Colors.BLACK26),
            Drawer("Show_drawer", drawer=data.view.drawer),
        ],
        drawer=data.view.drawer,
        appbar=data.view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

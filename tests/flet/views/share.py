import flet as ft
import flet_easy as fs
from dataclasses import dataclass

share = fs.AddPagesy()


@dataclass
class Test:
    name: int
    version: str

# 1


@share.page('/send-data', share_data=True)
def send_data_page(data: fs.Datasy):
    page = data.page
    page.title = 'send data'

    data.share.set('test', Test('Flet-Easy', '0.1'))
    data.share.set('owner', 'Daxexs')

    return ft.View(
        route='/send-data',
        controls=[
            ft.Text(f'data keys: {data.share.get_keys()}'),
            ft.Text(f'data values: {data.share.get_values()}'),
            ft.Text(f'data dict: {data.share.get_all()}'),
            ft.ElevatedButton(
                'View shared data',
                key='/data',
                on_click=data.go)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# 2


@share.page('/data', share_data=True)
def get_data_page(data: fs.Datasy):
    page = data.page
    page.title = 'data'

    # It is checked if there is data stored in the dictionary (data.share.set).
    if data.share.contains():
        x: Test = data.share.get('test')
        y: str = data.share.get('owner')
        res = ft.Text(
            f'Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}')
    else:
        res = ft.Text('No value passed on the page!.')

    return ft.View(
        route='/data',
        controls=[
            ft.Container(
                content=res,
                padding=20,
                border_radius=20,
                bgcolor=ft.colors.BLACK26
            ),
            ft.ElevatedButton(
                'Check the following page for matched data',
                key='/info',
                on_click=data.go
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

# 3


@share.page('/info')
def info_page(data: fs.Datasy):
    page = data.page

    page.title = "Information"

    # It is checked if there is data stored in the dictionary (data.share.set).
    if data.share.contains():
        x: Test = data.share.get('test')
        y: str = data.share.get('owner')
        res = ft.Text(
            f'Name: {x.name}\nVersion: {x.version}\n-----\nOwner: {y}')
    else:
        res = ft.Text('No value passed on the page!.')

    return ft.View(
        route='/info',
        controls=[
            ft.Text('Access to shared data?'),
            ft.Container(
                content=res,
                padding=20,
                border_radius=20,
                bgcolor=ft.colors.BLACK26
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

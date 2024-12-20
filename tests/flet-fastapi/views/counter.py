import flet as ft
from controllers.contador import ContadorC

import flet_easy as fs

""" We create an object of the AddPagesy class to add to the list of the add_routes method of the FletEasy class."""
counter = fs.AddPagesy(route_prefix="/counter")


class Contador(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.new_control = ContadorC(
            self
        )  # # We create an object of the controller class of this class, to be able to use its methods.

    def build(self):
        self.test = "test inicio"
        self.numero = ft.TextButton("0", style=ft.ButtonStyle(bgcolor=ft.Colors.BLACK12))
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        ft.Icons.REMOVE,
                        on_click=self.new_control.min,  # Al enviar self estamos enviando la clase
                        bgcolor=ft.Colors.RED_400,
                    ),
                    self.numero,
                    ft.IconButton(
                        ft.Icons.ADD,
                        on_click=self.new_control.max,
                        bgcolor=ft.Colors.GREEN_400,
                    ),
                ],
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLACK26,
            border_radius=10,
            padding=20,
            width=200,
            alignment=ft.alignment.center,
        )


@counter.page("/", title="Counter", protected_route=True)
async def counter_page(data: fs.Datasy):
    view = data.view

    counter = Contador()
    counter2 = Contador()

    view.appbar.title = ft.Text("Counter")

    return ft.View(
        controls=[
            counter,
            counter2,
        ],
        appbar=view.appbar,
        vertical_alignment=view.vertical_alignment,
        horizontal_alignment=view.horizontal_alignment,
    )

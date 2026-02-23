import flet as ft
from components import Drawer

import flet_easy as fs


# add class to middleware custom
class CustomMiddleware(fs.MiddlewareRequest):
    def __init__(self):
        super().__init__()
        self.route = self.data.page.route

    def before_request(self):
        print(f"*|{self.route}| Before request", self.data.history_routes)
        print("* Before request")

    def after_request(self):
        print(f"*|{self.route}| After request")


# add function to middleware custom
async def use_middleware(data: fs.Datasy):
    print(f"**|{data.page.route}| Use middleware before request")


# add middlewares to pages decorator
index = fs.AddPagesy(
    middleware=[use_middleware, CustomMiddleware],
)


# We add a page
@index.page(route="/home", title="Flet-Easy")
async def index_page(data: fs.Datasy):
    view = data.view
    return ft.View(
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go keyboard", on_click=data.go("/counter/use-keyboard/10")),
            Drawer("Show_drawer", drawer=view.drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
        appbar=view.appbar,
    )

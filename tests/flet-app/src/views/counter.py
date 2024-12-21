import flet as ft
from components import Counter, Custom, Drawer

import flet_easy as fs

counter = fs.AddPagesy(
    route_prefix="/counter",
)


async def check_params(data: fs.Datasy):
    print("+ Params Counter id:", data.url_params.get("id"))
    if data.url_params.get("id") == 10 and not await fs.decode_async("login", data):
        return data.redirect("/share/send-data")


# We add a one page
@counter.page(route="/test/{id:int}", title="Counter", middleware=[check_params])
async def counter_page(data: fs.Datasy, id: str):
    view = data.view

    return ft.View(
        controls=[
            Counter(data.on_resize, id=id),
            Drawer(text="Show_drawer", drawer=view.drawer),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        drawer=view.drawer,
        appbar=view.appbar,
    )


# We add a second page - Using a class
@counter.page(route="/ts", title="Page2 - Use Class")
class PageTs(Custom):
    def __init__(self, data: fs.Datasy):
        self.data = data

    def build(self):
        return ft.View(
            controls=[ft.Text("Page 2", size=50)],
            appbar=self.custom_appbar(),
            vertical_alignment="center",
            horizontal_alignment="center",
        )


# add a third page - Using a class
@counter.page("/use-keyboard/{id:int}", title="Use Keyboard - Use Class")
class PageUseKeyboard(Custom):
    def __init__(self, data: fs.Datasy, id: int):
        self.data = data
        self.on_keyboard = data.on_keyboard_event
        self.number = ft.TextField(id)
        self.keyboard = ft.Row(
            wrap=True,
            alignment="center",
            scroll="auto",
        )

        self.on_keyboard.add_control(self.on_key_down)

    def on_key_down(self):
        if int(self.number.value) > 0:
            self.keyboard.controls.append(
                ft.Chip(
                    label=ft.Text(self.on_keyboard.test()),
                    color=ft.Colors.GREEN_900,
                )
            )

            self.number.value = int(self.number.value) - 1
        self.data.page.update()

    def reset(self, e):
        self.number.value = str(self.data.url_params.get("id"))
        self.number.update()

    async def build(self):
        return ft.View(
            controls=[
                ft.Text("Use keyboard", size=30),
                ft.Row(
                    controls=[
                        self.number,
                        ft.FilledButton("reset", on_click=self.reset),
                    ],
                    alignment="center",
                ),
                ft.Container(
                    content=self.keyboard,
                    border_radius=5,
                    border=ft.border.all(1),
                    padding=10,
                    width=self.data.on_resize.widthX(100),
                    height=self.data.on_resize.heightX(69),
                ),
            ],
            horizontal_alignment="center",
            scroll="auto",
            appbar=self.custom_appbar(),
        )

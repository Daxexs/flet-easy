import flet as ft
import flet_easy as fs

counter = fs.AddPagesy(
    route_prefix="/counter",
)


class Counter(ft.UserControl):
    def __init__(self, id: int, color: str, size: int, on_resize: fs.Resizesy):
        super().__init__()
        self.id = id
        self.color = color
        self.size = size
        self.on_resize = on_resize
        self.txt_number = ft.TextField(value=id, text_align="right", width=100)

    async def minus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) - 1)
        await self.update_async()

    async def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        await self.update_async()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=self.minus_click),
                    self.txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=self.plus_click),
                ],
                alignment="center",
            ),
            bgcolor=self.color,
            height=self.on_resize.heightX(40),
        )


# We add a second page
@counter.page(route="/test/{id}")
async def counter_page(data: fs.Datasy, id: str):
    page = data.page
    on_resize = data.on_resize

    page.title = "Counter"

    async def go_home(e):
        await page.go_async(data.route_init)

    return ft.View(
        route="/counter",
        controls=[
            Counter(id=id, color=ft.colors.BLUE_500, size=40, on_resize=on_resize),
            Counter(id=0, color=ft.colors.ORANGE_500, size=40, on_resize=on_resize),
            ft.FilledButton("Go to Home", on_click=go_home),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

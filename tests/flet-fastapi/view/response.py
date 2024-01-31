import flet as ft
import flet_easy as fs
from flet.canvas import CanvasResizeEvent

response = fs.AddPagesy()

class ResponseTest(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Row(
            controls=[
                fs.ResponsiveControlsy(
                    ft.Container(
                        content=ft.Text("W x H"),
                        bgcolor=ft.colors.GREEN_400,
                        alignment=ft.alignment.center
                    ),
                    expand=1,
                    show_resize=True
                ),
                fs.ResponsiveControlsy(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                fs.ResponsiveControlsy(
                                    content=ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    bgcolor=ft.colors.DEEP_ORANGE_50,
                                                    height=170,
                                                    margin=5
                                                ),
                                                ft.Container(
                                                    bgcolor=ft.colors.BLACK87,
                                                    height=170,
                                                    margin=5
                                                )
                                            ],
                                            scroll=ft.ScrollMode.HIDDEN,
                                            spacing=0
                                        ),
                                        bgcolor=ft.colors.BROWN_500,
                                        expand=True,
                                        margin=ft.Margin(5, 5, 0, 5)
                                    ),
                                    expand=1,
                                    show_resize=True
                                ),
                                fs.ResponsiveControlsy(
                                    content=ft.Container(
                                        content=ft.Text(
                                            'ok',
                                        ),
                                        bgcolor=ft.colors.CYAN_500,
                                        alignment=ft.alignment.center,
                                        margin=ft.Margin(0, 5, 5, 5),
                                    ),
                                    expand=1,
                                    show_resize=True,

                                ),
                            ],
                            expand=1,
                            spacing=0,

                        ),
                        bgcolor=ft.colors.AMBER_600,
                        alignment=ft.alignment.center
                    ),
                    show_resize=True,
                    expand=3
                )
            ],
            expand=2
        )

@response.page('/response')
async def response_page(data: fs.Datasy):
    page = data.page
    view = data.view
    
    page.title = 'response'
    view.appbar.title = ft.Text('Response')

    async def handle_resize(e: CanvasResizeEvent):
        c = e.control.content
        t = c.content
        t.value = f"{e.width} x {e.height}"
        await page.update_async()

    return ft.View(
        f'{data.route_prefix}/response',
        controls=[
            fs.ResponsiveControlsy(
                content=ft.Container(
                    content=ft.Text("W x H"),
                    bgcolor=ft.colors.RED,
                    alignment=ft.alignment.center,
                    height=100
                ),
                expand=1,
                show_resize=True
            ),
            fs.ResponsiveControlsy(
                ft.Container(
                    content=ft.Text("W x H"),
                    bgcolor=ft.colors.BLUE,
                    alignment=ft.alignment.center
                ),
                on_resize=handle_resize,
                expand=1
            ),
            fs.ResponsiveControlsy(
                content=ResponseTest(),
                expand=2
            ),
        ],
        appbar=view.appbar
    )

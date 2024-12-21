import asyncio
from dataclasses import dataclass

import flet as ft

import flet_easy as fs

pbs = fs.AddPagesy(route_prefix="/chat")


@dataclass
class ChatMsg:
    user: str
    msg: str


class Chat(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        asyncio.create_task(self.pubsub_init())
        self.username = ft.TextField(
            col={"xs": 5, "sm": 5, "md": 5, "lg": 5, "xl": 3},
            prefix_icon=ft.Icons.ACCOUNT_CIRCLE,
            on_change=self.time_alert,
        )
        self.message = ft.TextField(col=10, multiline=True, on_change=self.time_alert)
        self.messages = ft.Column(col=12, scroll=ft.ScrollMode.ALWAYS)

    async def pubsub_init(self):
        await self.page.pubsub.subscribe_async(self.chat_users)

    def build(self):
        self.container = ft.Container(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.ResponsiveRow(
                            controls=[self.messages],
                        ),
                        expand=True,
                        border_radius=10,
                        border=ft.border.all(1),
                        padding=10,
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            self.message,
                            ft.IconButton(
                                col=2,
                                icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED,
                                icon_color=ft.Colors.BLUE_500,
                                on_click=self.on_message,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
            ),
            bgcolor=ft.Colors.BLACK12,
            border_radius=10,
            border=ft.border.all(2),
            padding=10,
            expand=True,
        )

        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[self.username],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.container,
            ],
            expand=True,
        )

    async def time_alert(self, e):
        try:
            control = e.control
        except Exception:
            control = e

        control.label = None
        control.border_color = None
        await self.update_async()

    async def on_message(self, e):
        if len(self.username.value) == 0:
            self.username.label = "Enter your username"
            self.username.border_color = ft.Colors.RED_700
            await self.update_async()
            await asyncio.sleep(3)
            asyncio.create_task(self.time_alert(self.username))
        elif len(self.message.value) == 0:
            self.message.label = "Enter your message"
            self.message.border_color = ft.Colors.RED_700
            await self.update_async()
            await asyncio.sleep(3)
            asyncio.create_task(self.time_alert(self.message))
        else:
            chat_msg = ChatMsg(self.username.value, self.message.value)
            container_message = ft.Container(
                content=ft.Container(
                    content=ft.Text(f"{self.username.value}:\n{self.message.value}"),
                    bgcolor=ft.Colors.BLUE_500,
                    padding=ft.padding.only(10, 5, 10, 5),
                    border_radius=ft.border_radius.only(10, 10, 10, 0),
                ),
                padding=10,
                border_radius=10,
                alignment=ft.alignment.top_right,
                margin=ft.margin.symmetric(0, 10),
            )
            self.messages.controls.append(container_message)
            self.message.value = ""
            await self.update_async()
            await self.messages.scroll_to_async(
                offset=-1, duration=1000, curve=ft.AnimationCurve.EASE_OUT_CUBIC
            )
            await self.page.pubsub.send_others_async(chat_msg)

    async def chat_users(self, msg: ChatMsg):
        container_message = ft.Container(
            content=ft.Container(
                content=ft.Text(f"{msg.user}:\n{msg.msg}"),
                bgcolor=ft.Colors.ORANGE_500,
                padding=ft.padding.only(10, 5, 10, 5),
                border_radius=ft.border_radius.only(0, 10, 10, 10),
            ),
            padding=10,
            border_radius=10,
            alignment=ft.alignment.top_left,
            margin=ft.margin.symmetric(0, 10),
        )
        self.messages.controls.append(container_message)
        self.message.value = ""
        await self.update_async()
        await self.messages.scroll_to_async(
            offset=-1, duration=1000, curve=ft.AnimationCurve.EASE_OUT_CUBIC
        )


@pbs.page("/", title="Chat Users")
async def pubsub_page(data: fs.Datasy):
    page = data.page
    view = data.view
    on_resize = data.on_resize

    on_resize.margin_y = 28

    view.appbar.title = ft.Text("Chat Users")

    return ft.View(
        controls=[
            fs.ResponsiveControlsy(content=Chat(page), expand=1),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=view.appbar,
    )

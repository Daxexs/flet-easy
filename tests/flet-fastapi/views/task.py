import flet as ft

import flet_easy as fs

task = fs.AddPagesy(route_prefix="/task")


class Task(ft.UserControl):
    def __init__(self, page: ft.Page, on_resize: fs.Resizesy):
        super().__init__()
        self.page = page
        self.on_resize = on_resize
        self.input = ft.TextField(col=11, height=40, text_align=ft.TextAlign.CENTER, expand=True)

        self.input_dialog = ft.TextField(
            multiline=True,
            expand=True,
        )

        self.column = ft.Column()

        self.add = ft.FloatingActionButton(
            content=ft.Row(
                [
                    ft.IconButton(ft.Icons.ADD, on_click=self.open_dlg_modal),
                    ft.Text("Add"),
                ],
                alignment="center",
                spacing=5,
            ),
            bgcolor=ft.Colors.BLUE_700,
            shape=ft.RoundedRectangleBorder(radius=5),
            width=100,
            mini=True,
        )

        self.add_task = ft.AlertDialog(
            modal=True,
            title=ft.Text("Enter Task"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.input_dialog,
                        ft.Row(
                            controls=[
                                ft.TextButton("Yes", on_click=self.add_tasks),
                                ft.TextButton("No", on_click=self.close_dlg),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    # expand=True
                ),
                bgcolor=ft.Colors.BLACK12,
                # expand=True,
                height=self.on_resize.heightX(50),
                width=self.on_resize.widthX(50),
                padding=5,
            ),
            content_padding=10,
            # adaptive=True
        )

    def build(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Text("Create new task in database"),
                    ft.ResponsiveRow(
                        controls=[self.column],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ]
            ),
            bgcolor=ft.Colors.BLACK12,
            border_radius=10,
            border=ft.border.all(2, ft.Colors.BLACK26),
            padding=20,
        )

    async def open_dlg_modal(self, e):
        self.page.dialog = self.add_task
        self.add_task.open = True
        await self.page.update_async()

    async def close_dlg(self, e):
        self.add_task.open = False
        await self.page.update_async()

    async def add_tasks(self, e):
        self.column.controls.append(ft.TextField(value=self.input_dialog.value, multiline=True))
        self.add_task.open = False
        self.input_dialog.value = ""
        await self.page.update_async()
        await self.update_async()


@task.page("/", title="Task")
async def task_page(data: fs.Datasy):
    page = data.page
    view = data.view
    on_resize = data.on_resize

    view.appbar.title = ft.Text("Task")

    task = Task(page, on_resize)

    return ft.View(
        controls=[task],
        appbar=view.appbar,
        floating_action_button=task.add,
        scroll=ft.ScrollMode.AUTO,
    )

import flet as ft

import flet_easy as fs

keyboard = fs.AddPagesy()


@keyboard.page("/keyboard", title="Use Keyboard")
async def keyboard_page(data: fs.Datasy):
    page = data.page
    on_keyboard = data.on_keyboard_event
    view = data.view

    view.appbar.title = ft.Text("Use Keyboard")

    use_keyboard = ft.Column(scroll=ft.ScrollMode.AUTO)

    async def show_event():
        use_keyboard.controls.append(ft.Text(on_keyboard.test()))

        await page.update_async()

    # Add function to be executed by pressing the keyboard.
    on_keyboard.add_control(show_event)

    return ft.View(
        controls=[ft.Text("Use Keyboard", size=30), use_keyboard],
        appbar=view.appbar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

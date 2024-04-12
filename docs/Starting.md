# Flet-Easy
`Flet-Easy` is a package built as an add-on for [`Flet`](https://github.com/flet-dev/flet), designed for beginners what it does is to make `Flet` easier when building your apps, with a tidier and simpler code. Some functions:

* Facilitates the handling of `flet` events.
* Page building using decorators, which allows you to make numerous custom configurations to flet for desktop, mobile and website application.
* Designed to work with numerous pages of your created application.
* Provides better MVC construction of your code, which can be scalable and easy to read.
* Not only limits the MVC model but you can customize it according to your preferences.
* Customized URLs for more precision in sending data.
* Controlled data sharing between pages.
* Support asynchronous.
* Supports Application Packaging for distribution.

and more extra features.....

## Flet events it handles

- `on_route_change` :  Dynamic routing
- `on_view_pop`
- [`on_keyboard_event`](/flet-easy/Events/keyboard-event/)
- [`on_resize`](/flet-easy/Events/On-resize/)
- `on_error`


## Installation

Requires installation for use:

* `Flet` (Installed automatically)
* `Flet-fastapi` (Optional)
* `uvicorn` (Optional)
  
```bash
  pip install flet-easy
```

## Update

```bash
  pip install flet-easy --upgrade
```

## Flet-Easy app example
Here is an example of an application with 2 pages, "Home" and "Counter":

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/flet-easy")

# We add a page
@app.page(route="/flet-easy")
def index_page(data: fs.Datasy):
    page = data.page

    page.title = "Flet-Easy"

    def go_counter(e):
        page.go("/counter")

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter", on_click=go_counter),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

# We add a second page
@app.page(route="/counter")
def counter_page(data: fs.Datasy):
    page = data.page

    page.title = "Counter"

    txt_number = ft.TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def go_home(e):
        page.go("/flet-easy")

    return ft.View(
        route="/counter",
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment="center",
            ),
            ft.FilledButton("Go to Home", on_click=go_home),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

# We run the application
app.run()
```
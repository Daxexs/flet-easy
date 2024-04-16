# Flet-Easy
`Flet-Easy` is a package built as an add-on for [`Flet`](https://github.com/flet-dev/flet), designed for beginners, what it does is to facilitate the use of `Flet` when building your applications, with a tidier and simpler code.

## Features
* Easy to use (**hence the name**).
* Facilitates `flet` event handling.
* Simple page routing (There are three ways) for whichever one suits you best. [`view`](/flet-easy/dynamic-routes/)
* App construction with numerous pages and custom flet configurations for desktop, mobile and web sites.
* Provides a better construction of your code, which can be scalable and easy to read (it adapts to your preferences, there are no limitations).
* Dynamic routing, customization in the routes for greater accuracy in sending data. [`view`](/flet-easy/dynamic-routes/#custom-validation)
* Routing protection [`view`](/flet-easy/Customized-app/Route-protection/)
* Custom Page 404 [`view`](/flet-easy/Customized-app/Page-404/)
* Controlled data sharing between pages. [`view`](/flet-easy/Data-sharing-between-pages/)
* Asynchronous support.
* Middleware Support (in the app in general and in each of the pages). [`view`](/flet-easy/Midleware/)
* JWT support for authentication sessions in the data parameter. (useful to control the time of sessions) [`view`](/flet-easy/Basic-JWT/)
* Working with other applications. [`view`](/flet-easy/Data-sharing-between-pages/)
* CLI to create app structure `FletEasy` (`fs init`) [`view`](/flet-easy/CLI-to-create-app/)
* Easy integration of `on_keyboard_event` in each of the pages. [`view`](/flet-easy/Events/keyboard-event/)
* Use the percentage of the page width and height of the page with `on_resize`. [`view`](/flet-easy/Events/On-resize/)
* `ResponsiveControlsy` control to make the app responsive, useful for desktop applications. [`view`](/flet-easy/ResponsiveControlsy/)
* Soporta Application Packaging para su distribución. [view](https://flet.dev/docs/publish)

## Flet events it handles

- `on_route_change` :  Dynamic routing
- `on_view_pop`
- [`on_keyboard_event`](/flet-easy/Events/keyboard-event/)
- [`on_resize`](/flet-easy/Events/On-resize/)
- `on_error`


## Installation

Requires installation for use:

* `Flet`
  
```bash
  pip install flet
```
```bash
  pip install flet-easy
```

## Update

```bash
  pip install flet-easy --upgrade
```

## Flet-Easy app example
Here is an example of an application with 2 pages, "Home" and "Counter":

```python hl_lines="4 7 19 50"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/flet-easy")

# We add a page
@app.page(route="/flet-easy", title="Flet-Easy")
def index_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Home page"),
            ft.FilledButton("Go to Counter", on_click=data.go("/counter")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# We add a second page
@app.page(route="/counter", title="Counter")
def counter_page(data: fs.Datasy):
    page = data.page

    txt_number = ft.TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    return ft.View(
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment="center",
            ),
            ft.FilledButton("Go to Home", on_click=data.go("/flet-easy")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# We run the application
app.run()
```

### 🎬 **Mode**
![app example](assets/gifs/app-example.gif "app example")
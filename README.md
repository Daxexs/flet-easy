[![github](https://img.shields.io/badge/my_profile-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Daxexs)[![pypi](https://img.shields.io/badge/Pypi-0A66C2?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/flet-easy)

[![image](https://img.shields.io/pypi/pyversions/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy) [![image](https://img.shields.io/pypi/v/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy) [![image](https://img.shields.io/pypi/l/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy)

[![Downloads](https://static.pepy.tech/badge/flet-easy)](https://pepy.tech/project/flet-easy) [![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)

<div align="center">
    <img src="https://github.com/Daxexs/flet-easy/blob/main/media/logo.png?raw=true" alt="logo" width="250">
</div>


# 🔥Flet-Easy
`Flet-Easy` is a package built as an add-on for [`Flet`](https://github.com/flet-dev/flet), designed for beginners what it does is to make `Flet` easier when building your apps, with a tidier and simpler code.

## Features
* Easy to use (**hence the name**).
* Facilitates `flet` event handling.
* Simple page routing (There are three ways) for whichever one suits you best. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/dynamic-routes/))
* App construction with numerous pages and custom flet configurations for desktop, mobile and web sites.
* Provides a better construction of your code, which can be scalable and easy to read (it adapts to your preferences, there are no limitations).
* Dynamic routing, customization in the routes for greater accuracy in sending data. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/dynamic-routes/#custom-validation))
* Routing protection ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Customized-app/Route-protection/))
* Custom Page 404 ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Customized-app/Page-404/))
* Controlled data sharing between pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Data-sharing-between-pages/))
* Asynchronous support.
* Middleware Support (in the app in general and in each of the pages). ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Midleware/))
* JWT support for authentication sessions in the data parameter. (useful to control the time of sessions) ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Basic-JWT/))
* Working with other applications. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Data-sharing-between-pages/))
* CLI to create app structure `FletEasy` (`fs init`) ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/CLI-to-create-app/))
* Easy integration of `on_keyboard_event` in each of the pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Events/keyboard-event/))
* Use the percentage of the page width and height of the page with `on_resize`. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/Events/On-resize/))
* `ResponsiveControlsy` control to make the app responsive, useful for desktop applications. ([**`Docs`**](https://daxexs.github.io/flet-easy/latest/flet-easy/ResponsiveControlsy/))
* Soporta Application Packaging para su distribución. [view](https://flet.dev/docs/publish)

## 📌Flet events it handles

- `on_route_change` :  Dynamic routing
- `on_view_pop`
- `on_keyboard_event`
- `on_resize`
- `on_error`

## 💻Installation:

Requires installation [`Flet`](https://github.com/flet-dev/flet) for use:
```bash
  pip install flet --upgrade
```
```bash
  pip install flet-easy
```

## 💻Update:
```bash
  pip install flet-easy --upgrade
```

## 🔥Flet-Easy app example
Here is an example of an application with 2 pages, "Home" and "Counter":

```python
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

## 🎬 **Mode**
![app example](https://github.com/Daxexs/flet-easy/blob/main/media/app-example.gif?raw=true "app example")

## 🚀 How to use `Flet-Easy`?
> [!IMPORTANT]
Documentation: https://daxexs.github.io/flet-easy/latest/

## 👀 Code examples
> [!NOTE]
https://github.com/Daxexs/flet-easy/tree/main/tests

## 🔎 Contribute to this project
Read the [CONTRIBUTING.md](https://github.com/Daxexs/flet-easy/blob/main/CONTRIBUTING.md) file

# 🧾 License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
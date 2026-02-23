# 🔥Flet-Easy

<div align="center">

[![github](https://img.shields.io/badge/my_profile-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Daxexs)[![pypi](https://img.shields.io/badge/Pypi-0A66C2?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/flet-easy)

[![image](https://img.shields.io/pypi/pyversions/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy) [![image](https://img.shields.io/pypi/v/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy) [![image](https://img.shields.io/pypi/l/flet-easy.svg)](https://pypi.python.org/pypi/flet-easy) [![socket](https://socket.dev/api/badge/pypi/package/flet-easy)](https://socket.dev/pypi/package/flet-easy) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) ![Linters](https://github.com/Daxexs/flet-easy/actions/workflows/linters.yml/badge.svg) ![Tests](https://github.com/Daxexs/flet-easy/actions/workflows/tests.yml/badge.svg) [![Downloads](https://static.pepy.tech/badge/flet-easy)](https://pepy.tech/project/flet-easy)

<img src="https://github.com/Daxexs/flet-easy/blob/main/media/logo.png?raw=true" alt="logo" width="250">

`Flet-Easy` is a comprehensive package built as an add-on for [`Flet`](https://github.com/flet-dev/flet). It provides a clean, intuitive API with advanced routing, authentication, middleware, page caching, and responsive design capabilities for building modern desktop, web, and mobile applications.
</div>

## ✨ Features (v0.3.0)

* **Page Caching System**: Optional state preservation across navigation for seamless user experience. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/page-caching/))
* **NavigationBar Integration**: Built-in support for `ft.NavigationBar` with automatic routing. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/guide/routing/navigation/#go_navigation_bar))
* **Enhanced Middleware**: Class-based middleware with page-specific application support. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/middleware/))
* Simple page routing (Various ways to add pages). ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/guide/add-pages/through-decorators/))
* Dynamic routing, customization in the routes for greater accuracy in sending data. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/guide/routing/dynamic-routes/#custom-validation))
* Routing protection ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/route-protection/))
* Custom Page 404 ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/configuration/page-404/))
* Controlled data sharing between pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/data-sharing-between-pages/))
* Asynchronous support.
* JWT support for authentication sessions. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/basic-jwt/))
* Working with other applications. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/integration/working-with-other-apps/))
* CLI to create app structure `FletEasy` (`fs init`). ([**`Docs`**](https://daxexs.github.io/flet-easy/cli/create-app/))
* Easy integration of `on_keyboard_event` in each of the pages. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/events/keyboard-event/))
* Use the percentage of the page width and height of the page with `on_resize`. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/events/on-resize/))
* `ResponsiveControlsy` control to make the app responsive. ([**`Docs`**](https://daxexs.github.io/flet-easy/dev/advanced/responsiveControlsy/))
* Supports Application Packaging for its distribution. ([view](https://flet.dev/docs/publish))

## 📌 Flet events it handles

* `on_route_change` : Dynamic routing
* `on_view_pop`
* `on_keyboard_event`
* `on_resize`
* `on_error`
  
## 💻 Ways to install

### Install Flet-Easy Complete

> [!NOTE]
> If you use the [`fs`](https://daxexs.github.io/flet-easy/dev/cli/create-app/) cli, it is important to have [`git`](https://git-scm.com/downloads) installed.

Installs all the dependencies to use, you can use all the functionalities provided by FletEasy

```bash
pip install flet-easy[all]
```

---

### Install clean Flet-Easy

> [!TIP]
> [Recommended for `Flet` Packaging Application](https://flet.dev/docs/publish).

Requires installation of [Flet >= 0.28.0](https://github.com/flet-dev/flet).

```bash
pip install flet[all]
```

#### If you do not use: [CLI-to-create-app](https://daxexs.github.io/flet-easy/dev/cli/create-app/)

```bash
pip install flet-easy
```

---

#### Install FletEasy if you need to use [Basic-JWT](https://daxexs.github.io/flet-easy/dev/advanced/basic-jwt/)

```bash
pip install flet-easy[JWT]
```

---

## 💻 Update

```bash
pip install flet-easy[all] --upgrade
```

## 🔥 Flet-Easy app example

Here is an example showcasing the new NavigationBar layout and routing features:

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/home")

# 1. Define a Global View
# This layout (AppBar, NavigationBar, etc.) will be shared across pages
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("My Flet-Easy App"),
            bgcolor=ft.Colors.BLUE,
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.INFO, label="About"),
            ],
            on_change=data.go_navigation_bar, # Handles automatic routing via index
        ),
        bgcolor=ft.Colors.GREY_50,
    )

# 2. Create the Home Page
@app.page("/home", title="Home", index=0) # index=0 matches the first Nav interface
def home_page(data: fs.Datasy):
    data.view.appbar.title = ft.Text("Welcome Home! 🏠")

    return ft.View(
        controls=[
            ft.Text("Welcome to Flet-Easy! 🎉", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Now with page caching and NavigationBar support!", size=16),
            ft.ElevatedButton(
                "Go to About",
                on_click=lambda _: data.go_route("/about"), # Direct navigation
            ),
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 3. Create the About Page
@app.page("/about", title="About", index=1)
def about_page(data: fs.Datasy):
    data.view.appbar.title = ft.Text("About Flet-Easy")

    return ft.View(
        controls=[
            ft.Text("About Flet-Easy", size=24),
            ft.Text("Build amazing apps with Python and new caching features!"),
            ft.ElevatedButton("← Back Home", on_click=lambda _: data.go_back()),
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 4. Run the application
if __name__ == "__main__":
    app.run()
```

## 🎬 **Demo**

![app example](https://github.com/Daxexs/flet-easy/blob/main/media/app-example.gif?raw=true "app example")

## 🚀 How to use `Flet-Easy`?

> [!IMPORTANT]
> 📑 Documentation: <https://daxexs.github.io/flet-easy/>

## 👀 Code examples

> [!TIP]
> <https://github.com/Daxexs/flet-easy/tree/main/tests>

## 🔎 Contribute to this project

Read the [CONTRIBUTING.md](https://github.com/Daxexs/flet-easy/blob/main/CONTRIBUTING.md) file

## 🧾 License

[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)

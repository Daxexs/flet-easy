# Navigation Methods

Flet-Easy provides powerful navigation capabilities that go beyond simple routing. This guide covers all navigation methods, patterns, and best practices for creating smooth user experiences.

## Overview

Navigation in Flet-Easy includes:

- **Route Navigation**: Direct path navigation with parameters
- **History Management**: Back/forward navigation with history tracking
- **Navigation Bar Integration**: Seamless tab-based navigation
- **Programmatic Navigation**: Dynamic routing based on conditions
- **Redirect Handling**: Middleware-based route redirections

## Core Navigation Methods

### `data.go(route)`

The primary navigation method for moving between pages.

**Basic Usage:**

```python hl_lines="7 11"
@app.page("/home")
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.ElevatedButton(
                "Go to Profile",
                on_click=data.go("/profile")
            ),
            ft.ElevatedButton(
                "Go to Settings (Clear History)",
                on_click=data.go("/settings")
            )
        ]
    )
```

### `data.go_back()`

Navigate to the previous page in the navigation history.

```python hl_lines="13"
@app.page("/product/{id:int}")
def product_detail_page(data: fs.Datasy, id: int):
    product = get_product(id)
    
    return ft.View(
        controls=[
            ft.Text(product.name, size=24),
            ft.Text(f"Price: ${product.price}"),
            ft.Text(product.description),
            ft.Row([
                ft.ElevatedButton(
                    "← Back",
                    on_click=lambda e: data.go_back()
                )
            ])
        ]
    )
```

**Smart Back Navigation:**

```python hl_lines="6"
@app.page("/search/results")
def search_results_page(data: fs.Datasy):
    def smart_back(_):
        # Check if there's history to go back to
        if len(data.history_routes) > 1:
            data.go_back()
        else:
            # Default fallback route
            data.go_route("/home")
    
    return ft.View(
        controls=[
            ft.Text("Search Results"),
            ft.ElevatedButton("← Back", on_click=smart_back),
            # ... search results
        ]
    )
```

### `data.go_navigation_bar`

Manage changes in the navigation bar for tab-based interfaces. This method is used in the `on_change` parameter of the `ft.NavigationBar` class. In addition, you must configure the routes, which in this case would be the `index` parameter of the `@app.page()` decorator.

```python hl_lines="27 33 38 43 48"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/home")


@app.view
def view_config(data: fs.Datasy):
    return ft.View(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME, selected_icon=ft.Icons.HOME_FILLED, label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SEARCH, selected_icon=ft.Icons.SEARCH, label="Search"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.FAVORITE_BORDER,
                    selected_icon=ft.Icons.FAVORITE,
                    label="Favorites",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Profile"
                ),
            ],
            on_change=data.go_navigation_bar,
        ),
    )


# Register navigation pages with indices
@app.page("/home", title="Home", index=0)
def home_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Home Page")], navigation_bar=data.view.navigation_bar)


@app.page("/search", title="Search", index=1)
def search_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Search Page")], navigation_bar=data.view.navigation_bar)


@app.page("/favorites", title="Favorites", index=2)
def favorites_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Favorites Page")], navigation_bar=data.view.navigation_bar)


@app.page("/profile", title="Profile", index=3)
def profile_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Profile Page")], navigation_bar=data.view.navigation_bar)

app.run()
```

#### Demo

<video controls>
  <source src="../../../assets/guide/routing/go_navigation_bar.webm" type="video/webm" alt="Flet-Easy - go_navigation_bar">
</video>

Navigation is a critical aspect of user experience in Flet-Easy applications. Use these patterns and methods to create intuitive, responsive navigation systems that enhance your application's usability and performance.

### `data.page_reload()`

Use this method to reload the page, restores the default values of the page.

```python hl_lines="20"
import flet as ft
import flet_easy as fs
import time

app = fs.FletEasy(route_init="/counter")

@app.page(route="/counter", title="Counter")
def counter_page(data: fs.Datasy):
    page = data.page
    txt_number = ft.TextField(value="0", text_align="right", width=100)
    play = False

    def add_numbers(e):
        nonlocal play

        if not play:
            # Long running process
            play = True
            for i in range(100):
                txt_number.value = str(int(txt_number.value) + 1)
                time.sleep(1)
                page.update()

    def reload_page(e):
        # Reset everything to default state
        data.page_reload()

    return ft.View(
        controls=[
            ft.Row([
                ft.IconButton(
                    ft.Icons.REPLAY_OUTLINED, 
                    on_click=reload_page,
                    tooltip="Reset Page"
                ),
                txt_number,
                ft.IconButton(
                    ft.Icons.ADD, 
                    on_click=add_numbers,
                    tooltip="Start Counter"
                ),
            ], alignment="center"),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

### Demo

<video controls>
  <source src="../../../assets/guide/core/Datasy-page_reload.webm" type="video/webm" alt="Flet-Easy - page_reload">
</video>

## `data.redirect(route)`

Useful if you do not want to access a route that has already been sent.

```python
def middleware(data: fs.Datasy):
    if data.route == "/dashboard":
        data.redirect("/login")

app.middleware(middleware)
```

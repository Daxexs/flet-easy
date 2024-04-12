## Add settings of the `View` controller of [Flet](https://flet.dev/docs/controls/view)
Which can be reused in each of the pages through the `data:fs.Datasy` parameter in the `page` decorator function of the app.

Decorator `view` to add custom controls to the app, the decorator function will return the Viewsy class from FletEasy. Which will be obtained in functions with parameter `data:fs.Datasy` and can be added to the page view decorated with `page` of the FletEasy class.

* The decorator function must receive a mandatory parameter, for example: `data:fs.Datasy`.
* Add universal controls to use in more than one page in a simple way.

### Example
!!! example ""
    We create an `AppBar` control of `Flet`, to be able to be reused in the other pages.
  
```python hl_lines="25-37"
import flet as ft
import flet_easy as fs

@app.view
def view(data: fs.Datasy):
    page = data.page
    
    def modify_theme():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK

    def theme(e):
        if page.theme_mode == ft.ThemeMode.SYSTEM:
            modify_theme()

        modify_theme()
        page.update()

    def go_home(e):
        page.go(data.route_init)

    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=theme),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="🔥 Home", on_click=go_home),
                    ]
                ),
            ],
        ),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```
Now we can reuse it in a page.
```python hl_lines="7 9 16"
@app.page(route="/home")
def home_page(data: fs.Datasy):
    page = data.page
    page.title = "Flet-Easy"
    
    # we obtain the values
    view = data.view
    # We can change the values of the appBar object, for example in title.
    view.appbar.title = ft.Text('Home')

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text("Home page"),
        ],
        appbar=view.appbar, # We reuse control
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

[page-404]: page-404

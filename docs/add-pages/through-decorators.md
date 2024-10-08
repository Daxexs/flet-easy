# Through decorators

## Add pages from other files to the main application

In order to create a page in a `file.py` different from the `main.py` file of the app, you need to use the `AddPagesy` class.

### `AddPagesy`

Requires the parameter:

* `route_prefix`: text string that will bind to the url of the page decorator, example(/users) this will encompass all urls of this class. (optional)

Methods:

* `page()` : Decorator to add a new page to the app. This decorator method acts similarly to the `Pagesy` class and contains the same required parameters. ([`See more`](/flet-easy/0.1.0/add-pages/by-means-of-functions/#pagesy))

!!! note "Soporta async"

## App structure

![FletEasy](../assets/images/struct-views.png "App structure")

???+ example "Urls to be created:"

    * `'/user/task'`
    * `'/user/information'`
    * `'/user/test'`

### **Example using functions**

```python title="user.py" hl_lines="4-6 13 14 30-31"
import flet_easy as fs
import flet as ft

users = fs.AddPagesy(
    route_prefix='/user'
)

# -> Urls to be created:
# * '/user/task'
# * '/user/information'
# * '/user/test'

@users.page("/task")
def task_page(data: fs.Datasy):
    data.page.title = "Task"

    return ft.View(
        controls=[
            ft.Text("Task"),
            ft.FilledButton(
                            "Go Information",
                            key="/user/information",
                            on_click=data.go_async,
                        ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"

    )

@users.page("/information")
async def information_page(data: fs.Datasy):
    data.page.title = "Information"

    return ft.View(
        controls=[
            ft.Text('Information'),
            ft.FilledButton(
                            "Go Test",
                            key="/user/test",
                            on_click=data.go_async,
                        ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"

    )

@users.page("/test")
async def page_test(data: fs.Datasy):
    data.page.title = "Test"
    return ft.View(
        controls=[
            ft.Text("Test"),
            ft.FilledButton(
                "Go Task",
                key="/user/task",
                on_click=data.go_async,
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )

```

### Adding pages

Now how to add to the main app the `main.py` file. For this we use the [`add_pages`](/flet-easy/0.1.0/how-to-use/#methods) method that requires as parameter a list of all the pages of other files that we want to add.

```Python title="main.py" hl_lines="2 8"
import flet_easy as fs
from views.user import users

app = fs.FletEasy(
    route_init='/user/task',
)

app.add_pages([users])

app.run_async()
```

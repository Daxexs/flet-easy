# By means of functions

## Adding pages to the main app without using decorators

For this we will require the [`add_routes`](/flet-easy/0.2.0/how-to-use/#methods) method of the object created by the [`FletEasy`](/flet-easy/0.2.0/how-to-use/#fleteasy) class.

!!! note "Soporta async"

## App structure

![FletEasy](../assets/images/funtion_add_page.png "App structure")

### **Example using functions**

```python title="index.py" hl_lines="4"
import flet_easy as fs
import flet as ft

def page_index(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text('Index'),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"

    )
```

### **Example using classes**

!!! warning "Available since version 0.2.4"

???+ info "More information"
    Create new pages (`View`) by using classes, you don't need to inherit from any other class to add the page, you just need to:

    - The constructor must have as mandatory parameter [`data:fs.Datasy`](/flet-easy/0.2.0/how-to-use/   #datasy-data) and if it receives a parameter bymeans of the url it must be used as parameter.
    - That the class to use must have a mandatory method called `build` that will return [`View`](https://flet.dev/docs/controls/view/) from flet, itcan     be async if necessary. This `build` method does not receive any    parameter.

    🤔 **why use a class?**

    The class can have several benefits, such as inheritance which is useful to avoid repeating code, among others.

```python title="test.py" hl_lines="4 10"
import flet_easy as fs
import flet as ft

class PageTest:
    def __init__(self, data:fs.Datasy, id:int, name:str):
        self.data = data
        self.id = id
        self.name = name
    
    def build(self):
        return ft.View(
            controls=[
                ft.Text('Text'),
                ft.Text(f'Id: {self.id}'),
                ft.Text(f'Name: {self.name}'),
                ft.FilledButton(
                            "Go index",
                            on_click=self.data.go("/index"),
                        ),
            ],
            vertical_alignment="center",
            horizontal_alignment="center"
    )
```

### Add routes

We import the functions or classes from the `views` folder, then we use the [`add_routes`](/flet-easy/0.2.0/how-to-use/#methods) method of the [FletEasy](/flet-easy/0.2.0/how-to-use/#fleteasy) instance, in which we will add a list of [`Pagesy`](/flet-easy/0.2.0/add-pages/by-means-of-functions/#pagesy) classes where we will configure the routes and the functions or classes to be used in addition to others.

```python title="main.py"
# Import functions from a `views` folder
from views.user import users
from views.index import page_index
from views.test import PageTest
import flet_easy as fs

# Add routes without the use of decorators
app.add_routes(add_views=[
    fs.Pagesy('/index', page_index, tilte='index'),
    fs.Pagesy('/user/task', users, tilte='users'),
    fs.Pagesy(
              '/test/{id:d}/user/{name:l}',
              PageTest,
              title='test counter',
              protected_route=True
            ),
])
```

## Pagesy

📑 The class `Pagesy`, it requires the following parameters:

* `route`: text string of the url, for example(`'/index'`).
* `view`: Stores the page function.
* `title` : Define the title of the page.
* `clear`: Removes the pages from the `page.views` list of flet. (optional)
* `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a morerestricted way. (optional) [[`See more`](/flet-easy/0.2.0/data-sharing-between-pages/)]
* `protected_route`: Protects the route of the page, according to the configuration of the `login` decoratorof the `FletEasy` class. (optional) [[`See more`](/flet-easy/0.2.0/customized-app/route-protection/)]
* `custom_params`: To add validation of parameters in the custom url using a dictionary, where the key is the nameof the parameter validation and the value is the custom function that must report a boolean value. [[`See more`](/flet-easy/0.2.0/dynamic-routes/#custom-validation)]
* `middleware` : It acts as an intermediary between different software components, intercepting andprocessing requests and responses. They allow adding functionalities to an application in a flexible andmodular way. (optional) [[`See more`](/flet-easy/0.2.0/middleware/#for-each-page)]

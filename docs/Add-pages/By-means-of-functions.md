## Adding pages to the main app without using decorators
For this we will require the `add_routes` method of the object created by the `FletEasy` class:

!!! note
    The application is faster when using automatic routing.

### App structure
![FletEasy](../assets/images/funtion_add_page.png "App structure")

### **Example**
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
```python title="main.py"
# Import functions from a `views` folder
from views.user import users
from views.index import page_index
from views.test import test_page
import flet_easy as fs

# Add routes without the use of decorators
app.add_routes(add_views=[
    fs.Pagesy('/index', page_index, tilte='index', clear=True),
    fs.Pagesy('/user/task', users, tilte='users', clear=True),
    fs.Pagesy('/test/{id:d}/user/{name:l}', test_page, title='test counter', protected_route=True),
])
```
## Pagesy
📑 The class `Pagesy`, it requires the following parameters:

* `route`: text string of the url, for example(`'/index'`).
* `view`: Stores the page function.
* `title` : Define the title of the page.
* `clear`: Removes the pages from the `page.views` list of flet. (optional)
* `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a morerestricted way. (optional)
* `protected_route`: Protects the route of the page, according to the configuration of the `login` decoratorof the `FletEasy` class. (optional)
* `custom_params`: To add validation of parameters in the custom url using a list, where the key is the nameof the parameter validation and the value is the custom function that must report a boolean value.
* `middleware` : It acts as an intermediary between different software components, intercepting andprocessing requests and responses. They allow adding functionalities to an application in a flexible andmodular way. (optional)

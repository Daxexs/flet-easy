## Adding pages to the main app without using decorators
For this we will require the `add_routes` method of the object created by the `FletEasy` class:

!!! note
    The app is faster when using decorators.

**Example:**
```python title="main.py"
# Import functions from a `view` folder
from view import (
    index_page,
    test_page,
    counter_page,
    login_page,
    task_page,
    markdown_page,
    response_page
)
import flet_easy as fs

# Add routes without the use of decorators
app.add_routes(add_views=[
    fs.Pagesy('/hi', index_page, True),
    fs.Pagesy('/test/{id:d}/user/{name:l}', test_page, protected_route=True),
    fs.Pagesy('/counter', counter_page),
    fs.Pagesy('/task', task_page),
    fs.Pagesy('/login/user', login_page),
    fs.Pagesy('/markdown', markdown_page),
    fs.Pagesy('/response', response_page),
])
```
📑 The class `Pagesy`, it requires the following parameters:

* `route` : text string of the url, for example('/task').
* `view` : Stores the page function.
* `clear` : Removes the pages from the page.views list of flet. (optional)
* `share_data` : It is a boolean value, which is useful if you want to share data between pages, in a more restricted way. [More information](/flet-easy/Data-sharing-between-pages/)
* `protected_route` : Protects the route of the page, according to the configuration of the login decorator of the FletEasy class. (optional)
* `custom_params` : To add parameter validation in the custom url using a dictionary, where the key is the name of the parameter validation and the value is the custom function that should return a value (boolean if false).

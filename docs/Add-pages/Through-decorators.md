## Add pages from other files to the main application.
In order to create a page in a `file.py` different from the `main.py` file of the app, you need to use the `AddPagesy` class. Requires the parameter:

* `route_prefix`: text string that will bind to the url of the page decorator, example(/users) this will encompass all urls of this class. (optional)

### App structure
![FletEasy](../assets/images/struct-views.png "App structure")

### **Example**

```python title="user.py" hl_lines="4-6 12 24"
import flet_easy as fs
import flet as ft

users = fs.AddPagesy(
    route_prefix='/user'
)

# -> Urls to be created:
# * '/user/task'
# * '/user/information'

@users.page('/task', title='Task')
def task_page(data: fs.Datasy):

    return ft.View(
        controls=[
            ft.Text('Task'),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"

    )

@users.page('/information', title='Information')
async def information_page(data: fs.Datasy):

    return ft.View(
        controls=[
            ft.Text('Information'),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"

    )
```
Now how to add to the main app the `main.py` file. For this we use the `add_pages` method that requires as parameter a list of all the pages of other files that we want to add.

```Python title="main.py" hl_lines="2 8"
import flet_easy as fs
from views.user import users

app = fs.FletEasy(
    route_init='/user/task',
)

app.add_pages([users])

app.run()
```

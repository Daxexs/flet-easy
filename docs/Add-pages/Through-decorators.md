## Add pages from other files to the main application.
* In order to create a page in a `file.py` different from the `main.py` file of the app, you need to use the `AddPagesy` class. Requires the parameter:
  * `route_prefix`: text string that will bind to the url of the page decorator, example(/users) this will encompass all urls of this class. (optional)

### **Example**

```python title="file.py" hl_lines="4-6 12 29"
import flet_easy as fs
import flet as ft

users = fs.AddPagesy(
    route_prefix='/user'
)

# -> Urls to be created:
# * '/user/task'
# * '/user/information'

@users.page('/task')
def task_page(data: fs.Datasy):

    page = data.page

    page.title = 'Task'

    return ft.View(
        route='/users/task',
        controls=[
            ft.Text('Task'),
        ],
        vertical_alignment=view.vertical_alignment,
        horizontal_alignment=view.horizontal_alignment

    )

@users.page('/information')
def information_page(data: fs.Datasy):

    page = data.page

    page.title = 'Information'

    return ft.View(
        route='/users/information',
        controls=[
            ft.Text('Information'),
        ],
        vertical_alignment=view.vertical_alignment,
        horizontal_alignment=view.horizontal_alignment

    )
```
Now how to add to the main app the `main.py` file. For this we use the `add_pages` method that requires as parameter a list of all the pages of other files that we want to add.

```Python title="main.py" hl_lines="2 8"
import flet_easy as fs
from file import users

app = fs.FletEasy(
    route_init='/user/task',
)

app.add_pages([users])

app.run()
```

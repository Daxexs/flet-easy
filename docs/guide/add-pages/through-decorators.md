# Through Decorators

## Add Pages from Other Files

Use the `AddPagesy` class to organize pages in separate files and group them with a common URL prefix.

## `AddPagesy` Class

```python
class AddPagesy:
    def __init__(
        self,
        route_prefix: str = "",
        middleware: Optional[List[Callable]] = None
    )
```

### Parameters

#### `route_prefix`

**Type**: `str` (optional)

URL prefix prepended to all page routes in this group.

**Example**: `route_prefix="/user"` converts `"/profile"` to `"/user/profile"`

#### `middleware`

???+ info "Available since version 0.3.0"

**Type**: `List[Callable]` (optional)

Middleware functions automatically applied to all pages in this group.

**Example**:

```python
# Define middleware
async def login_middleware(data: fs.Datasy):
    username = await data.page.client_storage.get_async("login")
    if username is None or username not in db:
        return data.redirect("/login")

# Create AddPagesy with middleware
users = fs.AddPagesy(
    route_prefix="/user",
    middleware=[login_middleware]  # Applied to all pages
)

# All pages inherit the middleware automatically
@users.page("/profile", title="Profile")
def user_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Profile")])

@users.page("/settings", title="Settings")
def settings_page(data: fs.Datasy):
    return ft.View(controls=[ft.Text("Settings")])
```

### Methods

#### `page(route, **kwargs)`

Decorator to add a page to the group. Same parameters as `Pagesy` class. ([See documentation](../add-pages/using-functions.md#pagesy))

**Supports**: Sync and async functions

## Complete Example

### App Structure

![FletEasy](../../../assets/guide/add-pages/img/struct-views.png "Flet-Easy - Add Pages Through Decorators")

**URLs created**: `/user/task`, `/user/information`

### Using Functions

```python title="user.py"
import flet_easy as fs
import flet as ft

# Create page group with URL prefix
users = fs.AddPagesy(route_prefix="/user")

@users.page("/task", title="Task")
def task_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Task", size=24),
            ft.FilledButton(
                "Go to Information",
                on_click=data.go("/user/information"),
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@users.page("/information", title="Information")
async def information_page(data: fs.Datasy):  # Async supported
    return ft.View(
        controls=[
            ft.Text("Information", size=24),
            ft.FilledButton(
                "Back to Task",
                on_click=data.go("/user/task"),
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
```

#### 🎬 Demo

<video controls>
  <source src="../../../assets/guide/add-pages/Through-decorators-using_functions.webm" type="video/mp4" alt="Flet-Easy - Add Pages Through Decorators Using Functions">
</video>

### Using Classes

!!! warning "Available since version 0.2.4"

**Requirements**:

- Constructor must accept `data: fs.Datasy` parameter
- Must have a `build()` method that returns `ft.View` (can be async)
- No inheritance needed

**Benefits**: Code reusability through inheritance, better organization for complex pages.

```python title="user.py"
@users.page("/test", title="Test")
class TestPage:
    def __init__(self, data: fs.Datasy):
        self.data = data
        self.counter = 0

    def increment(self, e):
        self.counter += 1
        self.data.page.update()

    async def build(self):
        return ft.View(
            controls=[
                ft.Text("Test Page", size=24),
                ft.Text(f"Counter: {self.counter}"),
                ft.ElevatedButton("Increment", on_click=self.increment),
                ft.FilledButton(
                    "Back to Task",
                    on_click=self.data.go("/user/task"),
                ),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )
```

### Adding Pages to Main App

Import and register page groups using `add_pages()`.

```python title="main.py"
import flet_easy as fs
from views.user import users

app = fs.FletEasy(route_init="/user/task")

# Add single group or list of groups
app.add_pages(users)  # or app.add_pages([users, admin, products])

app.run()
```

---

## Alternative: Without `AddPagesy`

!!! warning "Available since version 0.2.7"

Use `@fs.page()` decorator directly for standalone pages without route prefix or shared middleware.

!!! note "Important"
    Set `path_views` parameter for automatic page discovery.

**Main file**:

```python title="main.py"
import flet_easy as fs
from pathlib import Path

app = fs.FletEasy(
    route_init="/test",
    path_views=Path(__file__).parent / "views",  # Required
)

app.run()
```

**Page file** (in `views/` folder):

```python title="views/user.py"
import flet_easy as fs
import flet as ft

@fs.page(route="/test", title="Test")
def page_test(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Test Page", size=24)],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@fs.page(route="/about", title="About")
def about_page(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("About Page", size=24)],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
```

---

## Summary

| Feature               | `AddPagesy`   | `@fs.page()`        |
|-----------------------|---------------|---------------------|
| **Route Prefix**      | ✅ Yes        | ❌ No               |
| **Shared Middleware** | ✅ Yes        | ❌ No               |
| **Best For**          | Grouped pages | Standalone pages    |

**Use `AddPagesy`** when you need URL prefixes or shared middleware for multiple related pages.

**Use `@fs.page()`** for simple standalone pages without grouping.

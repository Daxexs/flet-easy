# FletEasy Class

The `FletEasy` class is the core component of Flet-Easy that provides a simplified and powerful way to build Flet applications with advanced routing, authentication, and configuration capabilities.

## Overview

The `FletEasy` class serves as the main application controller, offering:

- **Advanced Routing System**: Dynamic routes with parameter validation
- **Authentication & Security**: JWT support and route protection
- **Event Management**: Keyboard and resize event handling
- **Middleware Support**: Request/response processing pipeline
- **Automatic Page Discovery**: Auto-routing from directory structures
- **Responsive Design**: Built-in responsive control system

## Class Definition

```python
class FletEasy:
    def __init__(
        self,
        route_prefix: str = "",
        route_init: str = "/",
        route_login: str = "/login",
        on_keyboard: bool = False,
        on_resize: bool = False,
        secret_key: Optional[SecretKey] = None,
        auto_logout: bool = False,
        path_views: Optional[Path] = None,
        logger: bool = False,
        use_error_boundary: bool = True
    )
```

## Parameters

### `route_prefix`

- **Type**: `str`
- **Default**: `""`
- **Description**: Base prefix for all routes in your application

**Example:**

```python
app = fs.FletEasy(route_prefix="/myapp")
# Routes will be: /myapp/home, /myapp/about, etc.
```

### `route_init`

- **Type**: `str`
- **Default**: `"/"`
- **Description**: Initial route when the application starts

**Example:**

```python
app = fs.FletEasy(route_init="/dashboard")
# App starts at /dashboard instead of /
```

### `route_login`

- **Type**: `str`
- **Default**: `"/login"`
- **Description**: Redirect route for protected pages when user is not authenticated

**Example:**

```python
app = fs.FletEasy(route_login="/auth/signin")
# Protected routes redirect to /auth/signin
```

### `on_keyboard`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Enable global keyboard event handling

**Example:**

```python
app = fs.FletEasy(on_keyboard=True)

@app.config_event_handler
def handle_events(data: fs.Datasy):
    # Access keyboard events via data.on_keyboard_event
    if data.on_keyboard_event.key() == "Escape":
        data.page.window_close()
```

### `on_resize`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Enable window resize event handling

**Example:**

```python
app = fs.FletEasy(on_resize=True)

@app.config_event_handler
def handle_events(data: fs.Datasy):
    # Access resize events via data.on_resize
    width = data.on_resize.width()
    height = data.on_resize.height()
```

### `secret_key`

- **Type**: `Optional[SecretKey]`
- **Default**: `None`
- **Description**: Secret key for JWT authentication and secure storage

**Example:**

```python
from flet_easy import SecretKey

secret = SecretKey("your-secret-key-here")
app = fs.FletEasy(secret_key=secret)
```

### `auto_logout`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Automatically logout users when JWT expires

### `path_views`

- **Type**: `Optional[Path]`
- **Default**: `None`
- **Description**: Directory path for automatic page discovery

**Example:**

```python
from pathlib import Path

app = fs.FletEasy(path_views=Path("views"))
# Automatically discovers pages in ./views/ directory
```

### `logger`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Enable detailed logging for debugging

### `use_error_boundary`

- **Type**: `bool`
- **Default**: `True`
- **Description**: Enable the visual Error Boundary screen when an error occurs during page rendering.

!!! warning "Production Security Risk"
    In production environments, it is **highly recommended** to set `use_error_boundary=False`. If left enabled (`True`), critical problems, source code paths, and stack traces could be exposed directly to end-users, posing a security risk. By setting it to `False`, the app will display a safe generic message to the user, while still logging the full traceback to your terminal.

## Core Methods

### `@app.page()` Decorator

Register a page with routing capabilities.

```python
@app.page(
    route: str,
    title: Optional[str] = None,
    index: Optional[int] = None,
    page_clear: bool = False,
    share_data: bool = False,
    protected_route: bool = False,
    custom_params: Optional[Dict[str, Callable]] = None,
    middleware: Optional[Middleware] = None,
    cache: bool = False
)
def page_function(data: fs.Datasy, **params):
    # Page implementation
    pass
```

**Parameters:**

- **`route`**: URL pattern (supports dynamic parameters)
- **`title`**: Page title for browser/window
- **`index`**: Define the index of the page, use in controls like `ft.NavigationBar` and `ft.CupertinoNavigationBar`.
- **`page_clear`**: Clear previous pages from navigation stack
- **`share_data`**: Enable data sharing between pages
- **`protected_route`**: Require authentication
- **`custom_params`**: Custom parameter validators
- **`middleware`**: Page-specific middleware
- **`cache`**: Preserve page state during navigation

### `@app.view()` Decorator

Configure the global view template.

```python
@app.view
def global_view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(title=ft.Text("My App")),
        drawer=ft.NavigationDrawer(...),
        # ... other view properties
    )
```

### `@app.login()` Decorator

Configure authentication logic.

```python
@app.login
def auth_handler(data: fs.Datasy):
    # Check if user is authenticated
    token = data.page.client_storage.get("auth_token")
    if token and verify_token(token):
        return True
    return False
```

### `@app.config_event_handler()` Decorator

Configure global event handlers.

```python
@app.config_event_handler
def event_handler(data: fs.Datasy):
    page = data.page
    def key_event(e: ft.KeyboardEvent):
        if e.key == "F11":
            page.window.full_screen = not page.window.full_screen
            page.update()

    page.on_keyboard_event = key_event

```

## Complete Example

Here's a comprehensive example showing all major features:

```python
import flet as ft
import flet_easy as fs

# Initialize app with configuration
import flet as ft
import flet_easy as fs

# Minimal setup with auth and routes
app = fs.FletEasy(
    route_prefix="/myapp",
    route_init="/myapp/home",
    route_login="/myapp/login",
)


@app.view
def page_view(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Container(
                content=ft.Container(
                    content=ft.Column(
                        # controls=controls,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    width=640,
                    padding=24,
                    border_radius=16,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                ),
                alignment=ft.alignment.center,
                padding=24,
            )
        ],
        appbar=ft.AppBar(
            title=ft.Text("My App", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.INDIGO_600,
            actions=[
                ft.IconButton(
                    ft.Icons.HOME, icon_color=ft.Colors.WHITE, on_click=data.go(data.route_init)
                ),
                ft.IconButton(
                    ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=lambda _: data.logout("auth_token")
                ),
            ],
        ),
    )


@app.login
def authenticate(data: fs.Datasy):
    return data.page.client_storage.get("auth_token") is not None


@app.config_event_handler
def event_handler(data: fs.Datasy):
    page = data.page

    def key_event(e: ft.KeyboardEvent):
        if e.key == "F11":
            page.window.full_screen = not page.window.full_screen

        if e.key == "Escape":
            page.window.close()

        page.update()

    page.on_keyboard_event = key_event


@app.page("/home", title="Home")
def home_page(data: fs.Datasy):
    view = data.view
    view.appbar.title.value = "My App"

    view.controls[0].content.content.controls = [
        ft.Text("Welcome!", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(
            [
                ft.ElevatedButton("Profile", on_click=data.go("/myapp/profile/1")),
                ft.ElevatedButton("Admin", on_click=data.go("/myapp/admin")),
            ],
            spacing=12,
        ),
    ]
    return view


@app.page("/profile/{user_id:int}", title="Profile", protected_route=True)
def profile_page(data: fs.Datasy, user_id: int):
    view = data.view
    view.appbar.title.value = "Profile"
    view.controls[0].content.content.controls = [
        ft.Text(f"User ID: {user_id}", size=24),
        ft.ElevatedButton("Back", on_click=data.go(data.route_init)),
    ]
    return view


@app.page("/login", title="Login")
def login_page(data: fs.Datasy):
    u = ft.TextField(label="Username")
    p = ft.TextField(label="Password", password=True)

    def do_login(_):
        if u.value == "admin" and p.value == "admin":
            data.login("auth_token", {"user": u.value}, next_route=data.route_init)
        else:
            data.page.open(ft.SnackBar(content=ft.Text("Invalid credentials")))

    view = data.view
    view.appbar.title.value = "Login"
    view.controls[0].content.content.controls = [
        ft.Text("Login", size=26, weight=ft.FontWeight.BOLD),
        u,
        p,
        ft.ElevatedButton("Login", on_click=do_login),
    ]
    return view


@app.page("/admin", title="Admin", protected_route=True)
def admin_page(data: fs.Datasy):
    view = data.view
    view.appbar.title.value = "Admin"
    view.controls[0].content.content.controls = [
        ft.Text("Admin Panel", size=26, weight=ft.FontWeight.BOLD),
        ft.Text("Protected content"),
        ft.ElevatedButton("Logout", on_click=lambda _: data.logout("auth_token")),
    ]
    return view


if __name__ == "__main__":
    app.run()
```

### Demo

<video controls>
  <source src="../../../assets/guide/core/FletEasy-demo.webm" type="video/webm" alt="fletEasy demo protected routes">
</video>

### Step-by-step explanation of the example

- **Imports**
  Code excerpt:

  ```python
  import flet as ft
  import flet_easy as fs
  ```

  What it does:
  - Import Flet (UI toolkit) and Flet-Easy (routing, views, helpers).

- **App instance (`fs.FletEasy`)**

  Code excerpt:

  ```python
  app = fs.FletEasy(
      route_prefix="/myapp",
      route_init="/myapp/home",
      route_login="/myapp/login",
  )
  ```

  What it does:
  - Sets a route prefix for grouping.
  - Defines the initial route and the login route used by protected pages.

- **Global view with `@app.view`**

  Code excerpt:

  ```python
  @app.view
  def page_view(data: fs.Datasy):
      return ft.View(
          controls=[ ... ],
          appbar=ft.AppBar(
              title=ft.Text("My App", color=ft.Colors.WHITE),
              bgcolor=ft.Colors.INDIGO_600,
              actions=[ ... ],
          ),
      )
  ```

  What it does:
  - Provides a shared base layout (container + AppBar) for all pages.
  - Each page later customizes `data.view` (title and central content).

- **Authentication with `@app.login`**

  Code excerpt:

  ```python
  @app.login
  def authenticate(data: fs.Datasy):
      return data.page.client_storage.get("auth_token") is not None
  ```

  What it does:
  - Returns True if a token exists. Protected routes redirect to `route_login` if not authenticated.

- **Global event handler with `@app.config_event_handler`**

  Code excerpt:

  ```python
  @app.config_event_handler
  def event_handler(data: fs.Datasy):
      page = data.page

      def key_event(e: ft.KeyboardEvent):
          if e.key == "F11":
              page.window.full_screen = not page.window.full_screen

          if e.key == "Escape":
              page.window.close()

          page.update()

      page.on_keyboard_event = key_event
  ```

  What it does:
  - Adds global keyboard shortcuts: F11 toggles full screen, Escape closes the window.

- **Home page `@app.page("/home")`**

  Code excerpt:

  ```python
  @app.page("/home", title="Home")
  def home_page(data: fs.Datasy):
      view = data.view
      view.appbar.title.value = "My App"
      view.controls[0].content.content.controls = [
          ft.Text("Welcome!", size=28, weight=ft.FontWeight.BOLD),
          ft.Row([
              ft.ElevatedButton("Profile", on_click=data.go("/myapp/profile/1")),
              ft.ElevatedButton("Admin", on_click=data.go("/myapp/admin")),
          ], spacing=12),
      ]
      return view
  ```

  What it does:
  - Sets the title and the central content with navigation buttons.

- **Profile page `@app.page("/profile/{user_id:int}")` (protected)**

  Code excerpt:

  ```python
  @app.page("/profile/{user_id:int}", title="Profile", protected_route=True)
  def profile_page(data: fs.Datasy, user_id: int):
      view = data.view
      view.appbar.title.value = "Profile"
      view.controls[0].content.content.controls = [
          ft.Text(f"User ID: {user_id}", size=24),
          ft.ElevatedButton("Back", on_click=data.go(data.route_init)),
      ]
      return view
  ```

  What it does:
  - Receives a typed parameter (`user_id`) and shows a back button to the initial route.

- **Login page `@app.page("/login")`**

  Code excerpt:

  ```python
  @app.page("/login", title="Login")
  def login_page(data: fs.Datasy):
      u = ft.TextField(label="Username")
      p = ft.TextField(label="Password", password=True)

      def do_login(_):
          if u.value == "admin" and p.value == "admin":
              data.login("auth_token", {"user": u.value}, next_route=data.route_init)
          else:
              data.page.open(ft.SnackBar(content=ft.Text("Invalid credentials")))

      view = data.view
      view.appbar.title.value = "Login"
      view.controls[0].content.content.controls = [
          ft.Text("Login", size=26, weight=ft.FontWeight.BOLD),
          u, p,
          ft.ElevatedButton("Login", on_click=do_login),
      ]
      return view
  ```

  What it does:
  - Shows a simple login form. On success, stores a token and redirects; otherwise, shows a SnackBar.

- **Admin page `@app.page("/admin")` (protected)**

  Code excerpt:

  ```python
  @app.page("/admin", title="Admin", protected_route=True)
  def admin_page(data: fs.Datasy):
      view = data.view
      view.appbar.title.value = "Admin"
      view.controls[0].content.content.controls = [
          ft.Text("Admin Panel", size=26, weight=ft.FontWeight.BOLD),
          ft.Text("Protected content"),
          ft.ElevatedButton("Logout", on_click=lambda _: data.logout("auth_token")),
      ]
      return view
  ```

  What it does:
  - Shows protected content and provides a logout action.

- **App start**

  Code excerpt:

  ```python
  if __name__ == "__main__":
      app.run()
  ```

  What it does:
  - Starts the Flet-Easy app and registers all handlers.

With this approach, you define the layout once (in `@app.view`) and, in each page, focus on updating the title and content. Authentication and keyboard shortcuts are configured globally.

## Best Practices

### **Route Organization**

```python
{{ ... }}
app = fs.FletEasy(route_prefix="/app")

# Group related routes
@app.page("/app/users/list")
@app.page("/app/users/{id:int}")
@app.page("/app/users/{id:int}/edit")
```

### **Performance Optimization**

```python
# Use caching for static pages
@app.page("/about", cache=True)
def about_page(data: fs.Datasy):
    # This page state will be preserved
    pass

# Use page_clear for navigation resets
@app.page("/home", page_clear=True)
def home_page(data: fs.Datasy):
    # Clears navigation history
    pass
```

## Advanced Configuration

### Custom Parameter Validators

```python
def validate_email(email: str) -> bool:
    return "@" in email and "." in email

@app.page(
    "/user/{email:emailValidator}",
    custom_params={"emailValidator": validate_email}
)
def user_page(data: fs.Datasy, email: str):
    # email parameter is validated before this function runs
    pass
```

### Middleware Integration

```python
class AuthMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        if not self.data.page.client_storage.get("auth_token"):
            return fs.Redirect("/login")

@app.page("/protected", middleware=[AuthMiddleware])
def protected_page(data: fs.Datasy):
    pass
```

This comprehensive guide covers all aspects of the `FletEasy` class. For more specific examples and advanced use cases, refer to the other sections of this documentation.

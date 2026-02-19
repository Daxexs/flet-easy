# API Reference

This comprehensive API reference covers all classes, methods, and functions available in Flet-Easy. Use this as your complete guide for building applications with Flet-Easy.

## Core Classes

### FletEasy

::: flet_easy.FletEasy
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - page
        - view
        - login
        - config_event_handler
        - run
        - add_pages

__Quick Reference:__

```python
import flet_easy as fs

app = fs.FletEasy(
    route_prefix="/app",
    route_init="/app/home",
    route_login="/app/login",
    on_keyboard=True,
    on_resize=True,
    secret_key=fs.SecretKey("your-key"),
    auto_logout=True,
    logger=True
)

@app.page("/home")
def home_page(data: fs.Datasy):
    return ft.View("/home", controls=[...])

app.run()
```

### Datasy

::: flet_easy.Datasy
    options:
      show_root_heading: true
      show_source: true
      members:
        - page
        - url_params
        - view
        - route_prefix
        - route_init
        - route_login
        - share
        - on_keyboard_event
        - on_resize
        - go
        - go_back
        - go_navigation_bar
        - history_routes
        - login
        - logout
        - route
        - redirect

__Quick Reference:__

```python
def my_page(data: fs.Datasy):
    # Navigation
    data.go("/other-page")
    data.go_back()
    
    # Authentication
    data.login("token", "jwt-value")
    data.logout("token", next_route="/login")
    
    # Data sharing
    data.share.set("key", "value")
    value = data.share.get("key")
    
    # Page access
    data.page.title = "New Title"
    data.page.update()
```

### Pagesy

::: flet_easy.Pagesy
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__

__Quick Reference:__

```python
from flet_easy import Pagesy

page = Pagesy(
    route="/user/{id:d}",
    view=user_view_function,
    title="User Profile",
    protected_route=True,
    middleware=[auth_middleware],
    cache=True,
    share_data=True
)
```

### AddPagesy

::: flet_easy.AddPagesy
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import AddPagesy, Pagesy

pages = AddPagesy([
    Pagesy("/home", home_view),
    Pagesy("/about", about_view),
    Pagesy("/contact", contact_view)
])

app.add_pages(pages)
```

### Viewsy

::: flet_easy.Viewsy
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import Viewsy
import flet as ft

@app.view
def main_view(data: fs.Datasy):
    return Viewsy(
        appbar=ft.AppBar(title=ft.Text("My App")),
        drawer=ft.NavigationDrawer(...),
        bgcolor=ft.Colors.GREY_50,
        padding=ft.padding.all(20)
    )
```

## Authentication & Security

### SecretKey

::: flet_easy.SecretKey
    options:
      show_root_heading: true
      show_source: true

### EasyKey

::: flet_easy.EasyKey
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import EasyKey, SecretKey

# Generate keys
key_gen = EasyKey()
secret = key_gen.secret_key()  # For HS256
private_key = key_gen.private_key()  # For RS256
public_key = key_gen.public_key()  # For RS256

# Use with FletEasy
app = fs.FletEasy(secret_key=SecretKey(secret))
```

### JWT Functions

::: flet_easy.decode
    options:
      show_root_heading: true
      show_source: true

::: flet_easy.decode_async
    options:
      show_root_heading: true
      show_source: true

::: flet_easy.encode_HS256
    options:
      show_root_heading: true
      show_source: true

::: flet_easy.encode_RS256
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import encode_HS256, decode, SecretKey

# Encode JWT
secret = SecretKey("your-secret")
payload = {"user_id": 123, "role": "admin"}
token = encode_HS256(payload, secret)

# Decode JWT
decoded = decode(token, secret)
print(decoded["user_id"])  # 123
```

## Event Handling

### Keyboardsy

::: flet_easy.Keyboardsy
    options:
      show_root_heading: true
      show_source: true
      members:
        - add_control
        - key
        - shift
        - ctrl
        - alt
        - meta
        - test

__Quick Reference:__

```python
@app.config_event_handler
def handle_events(data: fs.Datasy):
    if data.on_keyboard_event:
        key = data.on_keyboard_event.key()
        if key == "Escape":
            data.go("/home")
        elif key == "F1":
            data.go("/help")
```

### Resizesy

::: flet_easy.Resizesy
    options:
      show_root_heading: true
      show_source: true
      members:
        - add_control
        - width
        - height
        - test

__Quick Reference:__

```python
@app.config_event_handler
def handle_events(data: fs.Datasy):
    if data.on_resize:
        width = data.on_resize.width()
        height = data.on_resize.height()
        
        # Responsive layout adjustments
        if width < 600:
            # Mobile layout
            pass
        else:
            # Desktop layout
            pass
```

## Responsive Design

### ResponsiveControlsy

::: flet_easy.ResponsiveControlsy
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import ResponsiveControlsy
import flet as ft

responsive_text = ResponsiveControlsy(
    controls={
        "xs": ft.Text("Mobile", size=14),
        "sm": ft.Text("Tablet", size=16),
        "md": ft.Text("Desktop", size=18),
        "lg": ft.Text("Large Desktop", size=20),
    }
)
```

## Reference System

### Ref

::: flet_easy.Ref
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import Ref
import flet as ft

def my_page(data: fs.Datasy):
    text_ref = Ref[ft.TextField]()
    
    def handle_click(_):
        value = text_ref.current.value
        print(f"Input value: {value}")
    
    return ft.View(
        "/page",
        controls=[
            ft.TextField(ref=text_ref, label="Enter text"),
            ft.ElevatedButton("Get Value", on_click=handle_click)
        ]
    )
```

## Middleware System

### MiddlewareRequest

::: flet_easy.MiddlewareRequest
    options:
      show_root_heading: true
      show_source: true
      members:
        - before_request
        - after_request

__Quick Reference:__

```python
from flet_easy import MiddlewareRequest, Redirect

class AuthMiddleware(MiddlewareRequest):
    def before_request(self):
        if not self.data.page.client_storage.get("auth_token"):
            return Redirect("/login")
    
    def after_request(self):
        # Log the request
        print(f"Accessed: {self.data.route}")

@app.page("/protected", middleware=[AuthMiddleware])
def protected_page(data: fs.Datasy):
    return ft.View("/protected", controls=[...])
```

## Utility Classes

### Redirect

::: flet_easy.Redirect
    options:
      show_root_heading: true
      show_source: true

__Quick Reference:__

```python
from flet_easy import Redirect

def auth_middleware(data: fs.Datasy):
    if not data.page.client_storage.get("token"):
        return Redirect("/login")
    return None
```

## Route Parameter Types

Flet-Easy supports several parameter types in dynamic routes:

| Type       | Syntax       | Description                     | Example                                          |
|------------|--------------|---------------------------------|--------------------------------------------------|
| Integer    | `{name:d}`   | Matches integers                | `/user/{id:d}` → `/user/123`                     |
| String     | `{name:str}` | Matches any string              | `/category/{name:str}` → `/category/electronics` |
| Lowercase  | `{name:l}`   | Matches lowercase strings       | `/tag/{slug:l}` → `/tag/python-tips`             |
| Float      | `{name:f}`   | Matches floating point numbers  | `/price/{amount:f}` → `/price/19.99`             |

__Example Usage:__

```python
@app.page("/blog/{year:d}/{month:d}/{slug:str}")
def blog_post(data: fs.Datasy, year: int, month: int, slug: str):
    # year and month are automatically converted to int
    # slug remains as string
    post = get_blog_post(year, month, slug)
    return ft.View(f"/blog/{year}/{month}/{slug}", controls=[...])
```

## Configuration Options

### FletEasy Configuration

| Parameter      | Type        | Default    | Description                             |
|----------------|-------------|------------|-----------------------------------------|
| `route_prefix` | `str`       | `""`       | Base prefix for all routes              |
| `route_init`   | `str`       | `"/"`      | Initial route when app starts           |
| `route_login`  | `str`       | `"/login"` | Redirect route for protected pages      |
| `on_keyboard`  | `bool`      | `False`    | Enable keyboard event handling          |
| `on_resize`    | `bool`      | `False`    | Enable window resize events             |
| `secret_key`   | `SecretKey` | `None`     | Secret key for JWT and encryption       |
| `auto_logout`  | `bool`      | `False`    | Auto-logout on JWT expiration           |
| `path_views`   | `Path`      | `None`     | Directory for automatic page discovery  |
| `logger`       | `bool`      | `False`    | Enable detailed logging                 |

### Pagesy Configuration

| Parameter         | Type        | Default    | Description                    |
|-------------------|-------------|------------|--------------------------------|
| `route`           | `str`       | Required   | URL pattern for the page       |
| `view`            | `Callable`  | Required   | Function that returns a View   |
| `title`           | `str`       | `None`     | Page title for browser         |
| `index`           | `int`       | `None`     | Navigation index for tabs      |
| `clear`           | `bool`      | `False`    | Clear navigation history       |
| `share_data`      | `bool`      | `False`    | Enable data sharing            |
| `protected_route` | `bool`      | `False`    | Require authentication         |
| `custom_params`   | `Dict`      | `None`     | Custom parameter validators    |
| `middleware`      | `List`      | `None`     | Page-specific middleware       |
| `cache`           | `bool`      | `False`    | Preserve page state            |

## Error Handling

### Common Exceptions

```python
from flet_easy.exceptions import (
    FletEasyError,
    AddPagesError,
    LoginError,
    LogoutError,
    MiddlewareError
)

try:
    app = fs.FletEasy()
    app.run()
except FletEasyError as e:
    print(f"FletEasy error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Error Handling in Pages

```python
@app.page("/api-demo")
def api_demo_page(data: fs.Datasy):
    try:
        # Your logic here
        result = fetch_api_data()
        return create_success_view(result)
    except Exception as e:
        # Show error to user
        data.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Error: {str(e)}"))
        )
        # Return error view
        return ft.View(
            "/api-demo",
            controls=[
                ft.Text("An error occurred", color=ft.Colors.RED),
                ft.ElevatedButton("Retry", on_click=data.go("/api-demo")),
                ft.ElevatedButton("Go Home", on_click=data.go("/home"))
            ]
        )
```

## Performance Tips

### __Use Caching Wisely__

```python
# Cache expensive pages
@app.page("/reports", cache=True)
def reports_page(data: fs.Datasy):
    # Expensive computation
    return ft.View("/reports", controls=[...])

# Don't cache dynamic content
@app.page("/live-feed", cache=False)
def live_feed_page(data: fs.Datasy):
    # Real-time data
    return ft.View("/live-feed", controls=[...])
```

### __Optimize Page Updates__

```python
def update_multiple_controls(data: fs.Datasy):
    # Batch updates
    control1.value = "New Value 1"
    control2.value = "New Value 2"
    control3.value = "New Value 3"
    
    # Single update call
    data.page.update()
```

### __Use Lazy Loading__

```python
@app.page("/heavy-page")
def heavy_page(data: fs.Datasy):
    # Load heavy content only when needed
    def load_content(_):
        heavy_data = load_heavy_data()
        content_container.content = create_heavy_ui(heavy_data)
        data.page.update()
    
    content_container = ft.Container()
    
    return ft.View(
        "/heavy-page",
        controls=[
            ft.ElevatedButton("Load Content", on_click=load_content),
            content_container
        ]
    )
```

## Migration Guide

### From v0.1.x to v0.2.x

__Breaking Changes:__

- `update_login` → `login`
- `logaut` → `logout`
- Function parameters changed for `login` and `config_event_handler` decorators

__Migration Example:__

```python
# Old (v0.1.x)
@app.login
def check_auth(page: ft.Page):
    return page.client_storage.get("token") is not None

# New (v0.2.x)
@app.login
def check_auth(data: fs.Datasy):
    return data.page.client_storage.get("token") is not None
```

This API reference provides comprehensive coverage of all Flet-Easy features. For detailed examples and tutorials, refer to the other sections of this documentation.

# Datasy Object

The `Datasy` class is the central data management object in Flet-Easy that provides access to page data, routing functionality, authentication, and event handling. Every page function receives a `Datasy` instance as its first parameter.

## Overview

The `Datasy` object serves as your main interface for:

- **Page Access**: Direct access to Flet's Page object
- **URL Parameters**: Extract dynamic route parameters
- **Navigation**: Advanced routing and navigation methods
- **Authentication**: Login/logout functionality with JWT support
- **Data Sharing**: Session-based data sharing between pages
- **Event Handling**: Keyboard and resize event management
- **View Management**: Access to configured view templates

## Core Properties

### `page`

- **Type**: `ft.Page`
- **Description**: Direct access to the Flet Page object

```python
@app.page("/example")
def example_page(data: fs.Datasy):
    # Access page properties
    data.page.title = "My Page Title"
    data.page.window_width = 800
    data.page.window_height = 600
    data.page.update()
```

### `url_params`

- **Type**: `Dict[str, Any]`
- **Description**: Dictionary containing URL route parameters

```python
@app.page("/user/{id:int}/profile/{tab:str}")
def user_profile(data: fs.Datasy, id: int, tab: str):
    # Access via function parameters (recommended)
    user_id = id
    active_tab = tab
    
    # Or via url_params dictionary
    user_id = data.url_params["id"]
    active_tab = data.url_params["tab"]
```

### `view`

- **Type**: `fs.Viewsy`
- **Description**: Access to the configured global view template

```python
@app.page("/example")
def example_page(data: fs.Datasy):
    # Modify the global view
    data.view.appbar.title = ft.Text("New Title")
    data.view.appbar.bgcolor = ft.Colors.RED
    
    return ft.View(
        controls=[ft.Text("Content")],
        appbar=data.view.appbar,
        drawer=data.view.drawer
    )
```

### Route Properties

```python
# Access route configuration
data.route_prefix    # App route prefix
data.route_init      # Initial route
data.route_login     # Login redirect route
data.route           # Current route path
```

## Navigation Methods

### `go (route)`

Navigate to a specific route.

```python
@app.page("/home")
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.ElevatedButton(
                "Go to Profile",
                on_click=data.go("/profile")
            ),
            ft.ElevatedButton(
                "Go to Settings",
                on_click=data.go("/settings")
            ),
            # Using lambda for event handlers
            ft.ElevatedButton(
                "Go to About",
                on_click=lambda _: data.go("/about")
            )
        ]
    )
```

### `go_back()`

!!! Note "⚡ Enhanced in v0.3.0"

Navigate to the previous route in history. Now executes directly without returning a lambda function.

```python
@app.page("/details")
def details_page(data: fs.Datasy):
    def handle_back(_):
        # v0.3.0: Executes immediately
        data.go_back()
    
    return ft.View(
        controls=[
            ft.Text("Details Page"),
            ft.ElevatedButton("Go Back", on_click=handle_back),
            # Or use lambda wrapper for event handling
            ft.ElevatedButton("Back (Lambda)", on_click=lambda _: data.go_back())
        ]
    )
```

### `go_navigation_bar (e)`

!!! Note "New in v0.3.0"

Handle navigation bar changes for `ft.NavigationBar` or `ft.CupertinoNavigationBar`. This method automatically navigates to the page with the corresponding `index` parameter.

```python
# Define pages with index parameters
@app.page("/home", title="Home", index=0)
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Home Page")],
        navigation_bar=data.view.navigation_bar
    )

@app.page("/search", title="Search", index=1)
def search_page(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Search Page")],
        navigation_bar=data.view.navigation_bar
    )

# Configure global navigation bar
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
            ],
            on_change=data.go_navigation_bar  # Direct method reference
        )
    )
```

### `go_route (route)`

!!! Note "New in v0.3.0"

Navigate to a specific route immediately (executes directly, unlike `data.go()` which returns a lambda function).

```python
@app.page("/dashboard")
def dashboard_page(data: fs.Datasy):
    def handle_quick_nav(_):
        # Direct navigation - executes immediately
        data.go_route("/settings")
    
    return ft.View(
        controls=[
            ft.Text("Dashboard"),
            ft.ElevatedButton("Quick Settings", on_click=handle_quick_nav),
            # Compare with lambda approach
            ft.ElevatedButton("Lambda Settings", on_click=data.go("/settings"))
        ]
    )
```

### `redirect (route)`

!!! Note "Enhanced in v0.3.0"

Redirect to a specific route immediately. This method is executed directly, and importantly, it is now available not just for middlewares, but also directly in page functions to force a quick redirection.

```python
@app.page("/old-route")
def old_page(data: fs.Datasy):
    # Determine if we should redirect automatically instead of rendering
    if not user_has_feature_enabled():
        # Executes directly and prevents rendering the current view
        return data.redirect("/new-route")

    return ft.View(
        controls=[ft.Text("Old Route Content")]
    )
```

### `page_reload()`

!!! Note "New in v0.3.0"

Reload the current page and restore default values. This method is particularly useful for resetting page state and stopping ongoing processes.

**Use Cases:**

- Reset form fields to default values
- Stop running counters or timers
- Clear temporary page state
- Refresh dynamic content

```python
import flet as ft
import flet_easy as fs
import time

app = fs.FletEasy(route_init="/counter")

@app.page(route="/counter", title="Counter")
def counter_page(data: fs.Datasy):
    page = data.page
    txt_number = ft.TextField(value="0", text_align="right", width=100)
    play = False

    def add_numbers(e):
        nonlocal play

        if not play:
            # Long running process
            play = True
            for i in range(100):
                txt_number.value = str(int(txt_number.value) + 1)
                time.sleep(1)
                page.update()

    def reload_page(e):
        # Reset everything to default state
        data.page_reload()

    return ft.View(
        controls=[
            ft.Row([
                ft.IconButton(
                    ft.Icons.REPLAY_OUTLINED, 
                    on_click=reload_page,
                    tooltip="Reset Page"
                ),
                txt_number,
                ft.IconButton(
                    ft.Icons.PLAY_ARROW, 
                    on_click=add_numbers,
                    tooltip="Start Counter"
                ),
            ], alignment="center"),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../../assets/guide/core/Datasy-page_reload.webm" type="video/mp4" alt="fletEasy -app use page_reload">
</video>

### `dynamic_control(control, func_update)`

!!! Note "New in v0.3.0"

Add dynamic control updates for cached pages. Allows real-time updates when caching is enabled.

```python
@app.page("/live-data", cache=True)
def live_data_page(data: fs.Datasy):
    # Dynamic appbar title updates
    def update_title(appbar):
        current_time = datetime.now().strftime("%H:%M:%S")
        appbar.title = ft.Text(f"Live Data - {current_time}")
        data.page.update()
    
    # Register dynamic control
    data.dynamic_control(data.view.appbar, update_title)
    
    # Dynamic content updates
    content_text = ft.Text("Loading...")
    
    def update_content(text_control):
        text_control.value = f"Updated at {datetime.now()}"
        data.page.update()
    
    data.dynamic_control(content_text, update_content)
    
    return ft.View(
        controls=[
            content_text,
            ft.ElevatedButton(
                "Refresh",
                on_click=lambda _: data.page_reload()
            )
        ],
        appbar=data.view.appbar
    )
```

### `history_routes`

- **Type**: `deque[Tuple[str, int]]`
- **Description**: Get navigation history as a deque of (route, timestamp) tuples

```python
@app.page("/debug")
def debug_page(data: fs.Datasy):
    history = data.history_routes
    history_text = "\n".join([f"{route} at {timestamp}" for route, timestamp in history])
    
    return ft.View(
        controls=[
            ft.Text("Navigation History:"),
            ft.Text(history_text),
        ]
    )
```

## Authentication Methods

### `login(key, value, next_route)`

Store authentication data in client storage.

```python
@app.page("/login")
def login_page(data: fs.Datasy):
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    
    def handle_login(_):
        username = username_field.value
        password = password_field.value
        
        # Validate credentials (your logic here)
        if authenticate_user(username, password):
            # Store authentication token
            data.login("auth_token", username, next_route='/dashboard')

        else:
            data.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Invalid credentials"))
            )
    
    return ft.View(
        controls=[
            ft.Text("Login", size=24),
            username_field,
            password_field,
            ft.ElevatedButton("Login", on_click=handle_login)
        ]
    )
```

### `logout(key, next_route)`

!!! Note "⚡ Enhanced in v0.3.0"

Closes the sessions of all browser tabs or the device used, which has been previously configured with the `login` method. Now executes directly without returning a lambda function.

**Parameters:**

- `key` (str): The storage key to remove from client storage
- `next_route` (str, optional): Route to navigate to after logout. Defaults to `route_login` if not specified.

```python
@app.page("/dashboard", protected_route=True)
def dashboard_page(data: fs.Datasy):
    def handle_logout(_):
        # v0.3.0: Executes immediately and redirects
        data.logout('auth_token', next_route='/other-route')
    
    return ft.View(
        controls=[
            ft.Text("Welcome to Dashboard"),
            ft.ElevatedButton("Logout", on_click=handle_logout)
            ft.ElevatedButton("Quick Logout", on_click=lambda _: data.logout('auth_token'))
        ]
    )
```

## Data Sharing System

The `share` property provides enhanced session storage with additional methods.

### Basic Usage

```python
@app.page("/page1", share_data=True)
def page1(data: fs.Datasy):
    def save_data(_):
        # Store shared data
        data.share.set("user_preferences", {
            "theme": "dark",
            "language": "en"
        })
        data.share.set("cart_items", ["item1", "item2", "item3"])
        data.go("/page2")
    
    return ft.View(
        controls=[
            ft.Text("Page 1 - Set Data"),
            ft.ElevatedButton("Save & Go to Page 2", on_click=save_data)
        ]
    )

@app.page("/page2", share_data=True)
def page2(data: fs.Datasy):
    # Retrieve shared data
    preferences = data.share.get("user_preferences")
    cart_items = data.share.get("cart_items")
    
    return ft.View(
        controls=[
            ft.Text("Page 2 - Retrieved Data"),
            ft.Text(f"Theme: {preferences.get('theme') if preferences else 'None'}"),
            ft.Text(f"Cart Items: {len(cart_items) if cart_items else 0}"),
        ]
    )
```

### Enhanced Methods

```python
@app.page("/data-manager", share_data=True)
def data_manager_page(data: fs.Datasy):
    # Check if shared data exists
    has_data = data.share.contains()
    
    # Get all shared values as a list
    all_values = data.share.get_values()
    
    # Get complete shared data dictionary
    all_data = data.share.get_all()
    
    return ft.View(
        controls=[
            ft.Text(f"Has shared data: {has_data}"),
            ft.Text(f"Number of values: {len(all_values)}"),
            ft.Text(f"All keys: {list(all_data.keys())}"),
        ]
    )
```

## Event Handling

### Keyboard Events

```python
@app.page("/keyboard-demo")
def keyboard_demo(data: fs.Datasy):
    output_text = ft.Text("Press any key...")
    
    # Add keyboard event handler
    def handle_keyboard():
        key_info = data.on_keyboard_event.test()  # Get all key info
        key = data.on_keyboard_event.key()
        shift = data.on_keyboard_event.shift()
        ctrl = data.on_keyboard_event.ctrl()
        alt = data.on_keyboard_event.alt()
        meta = data.on_keyboard_event.meta()
        
        output_text.value = f"Key: {key}, Shift: {shift}, Ctrl: {ctrl}, Alt: {alt}, Meta: {meta}"
        data.page.update()
    
    # Register the handler
    data.on_keyboard_event.add_control(handle_keyboard)
    
    return ft.View(
        controls=[
            ft.Text("Keyboard Event Demo"),
            output_text,
        ]
    )
```

### Resize Events

```python
@app.page("/resize-demo")
def resize_demo(data: fs.Datasy):
    size_text = ft.Text("Resize the window...")
    
    def handle_resize():
        width = data.on_resize.width()
        height = data.on_resize.height()
        size_text.value = f"Window size: {width}x{height}"
        data.page.update()
    
    # Register resize handler
    data.on_resize.add_control(handle_resize)
    
    return ft.View(
        controls=[
            ft.Text("Resize Event Demo"),
            size_text,
        ]
    )
```

---

The `Datasy` object is your primary interface for building interactive Flet-Easy applications. Master these methods and properties to create powerful, responsive applications with excellent user experience.

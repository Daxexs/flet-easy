# Begin

## Flet-Easy

`Flet-Easy` is a package built as an add-on for [`Flet`](https://github.com/flet-dev/flet), designed for beginners, what it does is to facilitate the use of `Flet` when building your applications, with a tidier and simpler code.

## Features

* Easy to use (**hence the name**).
* Facilitates `flet` event handling.
* Simple page routing (There are three ways) for whichever one suits you best. [[`See more`](../guide/routing/dynamic-routes.md)]
* App construction with numerous pages and custom flet configurations for desktop, mobile and web sites.
* Provides a better construction of your code, which can be scalable and easy to read (it adapts to your preferences, there are no limitations).
* Dynamic routing, customization in the routes for greater accuracy in sending data. [[`See more`](../guide/routing/dynamic-routes.md#custom-validation)]
* Routing protection [[`See more`](../advanced/route-protection.md)]
* Custom Page 404 [[`See more`](../advanced/configuration/page-404.md)]
* Controlled data sharing between pages. [[`See more`](../advanced/data-sharing-between-pages.md)]
* Asynchronous support.
* Middleware Support (in the app in general and in each of the pages). [[`See more`](../advanced/middleware.md)]
* JWT support for authentication sessions in the data parameter. (useful to control the time of sessions) [[`See more`](../advanced/basic-jwt.md)]
* Working with other applications. [[`See more`](../advanced/integration/working-with-other-apps.md)]
* CLI to create app structure `FletEasy` (`fs init`) [[`See more`](../cli/create-app.md)]
* Easy integration of `on_keyboard_event` in each of the pages. [[`See more`](../advanced/events/keyboard-event.md)]
* Use the percentage of the page width and height of the page with `on_resize`. [[`See more`](../advanced/events/on-resize.md)]
* `ResponsiveControlsy` control to make the app responsive, useful for desktop applications. [[`See more`](../advanced/responsiveControlsy.md)]
* Supports Application Packaging for distribution. [[`See more`]](https://flet.dev/docs/publish)

## Flet events it handles

* `on_route_change` :  Dynamic routing
* `on_view_pop`
* [`on_keyboard_event`](../advanced/events/keyboard-event.md)
* [`on_resize`](../advanced/events/on-resize.md)
* `on_error`

## Complete App Example

Here's a comprehensive example showcasing Flet-Easy's key features including the new v0.3.0 capabilities:

### Basic Setup

```python
import flet as ft
import flet_easy as fs

# Create app with advanced configuration
app = fs.FletEasy(
    route_init="/home",
    on_keyboard=True,  # Enable keyboard events
    on_resize=True     # Enable resize events
)
```

### Configure Global View

!!! note "New in v0.3.0"

```python
@app.view
def main_view(data: fs.Datasy):
    # We return a Viewsy object containing the shared structure
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("Flet-Easy Demo"),
            bgcolor=ft.Colors.BLUE,
            actions=[
                ft.IconButton(
                    ft.Icons.REFRESH,
                    on_click=lambda _: data.page_reload() # Resets page to initial state
                )
            ]
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.ADD, label="Counter"),
            ],
            on_change=data.go_navigation_bar # Automatic routing based on destination index
        ),
        bgcolor=ft.Colors.GREY_50
    )
```

### Create Pages with Navigation Support

```python
# Home page: linked to index 0 of the NavigationBar
@app.page("/home", title="Home", index=0, cache=True) 
def home_page(data: fs.Datasy):
    
    # Example of dynamic_control: update AppBar title without rebuilding the whole view
    def update_title(appbar):
        appbar.title = ft.Text("Welcome Home!")
        data.page.update()
    
    data.dynamic_control(data.view.appbar, update_title)
    
    return ft.View(
        controls=[
            ft.Text("🏠 Welcome to Flet-Easy!", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("This demo showcases v0.3.0 features", size=16),
            ft.ElevatedButton(
                "Go to Counter",
                on_click=lambda _: data.go_route("/counter") # Instant navigation
            ),
        ],
        # Reuse properties from the global view
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center"
    )

# Counter page with caching disabled
@app.page("/counter", title="Counter", index=1, cache=True)
def counter_page(data: fs.Datasy):
    page = data.page
    
    # State will reset each time due to cache=False
    txt_number = ft.TextField(value="0", text_align="center", width=100)
    
    def update_counter(delta):
        current = int(txt_number.value)
        txt_number.value = str(current + delta)
        page.update()
    
    return ft.View(
        controls=[
            ft.Text("🔢 Interactive Counter", size=24),
            ft.Row([
                ft.IconButton(
                    ft.Icons.REMOVE_CIRCLE,
                    on_click=lambda _: update_counter(-1),
                    bgcolor=ft.Colors.RED_100
                ),
                txt_number,
                ft.IconButton(
                    ft.Icons.ADD_CIRCLE,
                    on_click=lambda _: update_counter(1),
                    bgcolor=ft.Colors.GREEN_100
                ),
            ], alignment="center"),
            ft.ElevatedButton(
                "← Back to Home",
                on_click=lambda _: data.go_back()  # Improved v0.3.0 method
            ),
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center"
    )
```

### Add Middleware

!!! note "Enhanced in v0.3.0"

```python
class LoggingMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        print(f"📍 Navigating to: {self.data.route}")
    
    def after_request(self):
        print(f"✅ Loaded: {self.data.route}")

# Add middleware to the app
app.add_middleware(LoggingMiddleware)

# Run the application
if __name__ == "__main__":
    app.run()
```

### Key Features Demonstrated

* ✨ **Navigation Bar Integration**: Automatic page switching with `index` parameter
* 🔄 **Page Caching**: State preservation with `cache=True/False`
* 🎯 **Dynamic Controls**: Real-time updates with `dynamic_control()`
* 🚀 **Direct Navigation**: Immediate routing with `go_route()`
* 🔧 **Enhanced Middleware**: Class-based middleware system
* 📱 **Responsive Design**: Global view configuration with `Viewsy`

### Demo

<video controls>
  <source src="../../assets/started/begin-example.webm" type="video/webm" alt="Begin Flet-Easy">
</video>

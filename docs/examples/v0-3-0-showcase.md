# Flet-Easy v0.3.0 Feature Showcase

Welcome to the Flet-Easy v0.3.0 showcase! This document provides real, runnable examples directly from our test suite, demonstrating the new declarative components, Flet hooks, and powerful class-based middlewares.

## Example 1: Declarative Routing with Decorators

This example (`tests/render-page-decorator.py`) demonstrates how to build a modern application using Flet's `@ft.component` ecosystem integrated seamlessly with Flet-Easy's `@app.page()` decorators.

!!! warning "Flet Version Requirement"
    The use of declarative components (`@ft.component`) is only available from **Flet version 0.80.0** onwards.

### 1. State Management and Reusable Components

We start by defining a reactive state using `@ft.observable` and a `dataclass`. Then, we create a reusable Flet component (`counter`) that manages its own internal state using `ft.use_state()`. Notice that this component does *not* need a route decorator!

```python
import asyncio
from dataclasses import dataclass

import flet as ft
import flet_easy as fs

app = fs.FletEasy()

@dataclass
@ft.observable
class CounterState:
    count: int = 0

    def add(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def remove(self):
        self.count -= 1

# Reusable UI component
@ft.component
def counter():
    state, _ = ft.use_state(CounterState())

    return ft.Column(
        controls=[
            ft.Text(value=f"{state.count}", size=30),
            ft.Row(
                controls=[
                    ft.Button("Add", on_click=state.add),
                    ft.Button("Remove", on_click=state.remove),
                    ft.Button("Reset", on_click=state.reset),
                ],
                alignment="center",
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )
```

### 2. Class-Based Middlewares

Flet-Easy v0.3.0 introduces `fs.MiddlewareRequest`. This allows you to define `before_request` and `after_request` hooks.

!!! tip "Execution Hierarchy (Outside-In)"
    Notice the power of the new middleware hierarchy! Middlewares execute in a strict outer-to-inner cascading order: **Global ➔ Sub-Router ➔ Page-Specific**. You can even pass arrays of mixed functional and class-based middlewares (e.g., `middleware=[funcMd, ClassMd]`).

Here, we add a logging middleware globally to all routes, and a smaller functional middleware specifically for our home page.

```python
class MiddlewareRoutes(fs.MiddlewareRequest):
    def before_request(self):
        print(f"route: {self.data.route} - before home")

    def after_request(self):
        print(f"route: {self.data.route} - after home")

# Add middleware to all routes globally
app.add_middleware(MiddlewareRoutes)

# Functional middleware for specific pages
def middleware_home(data: fs.Datasy):
    data.page.show_dialog(ft.SnackBar(ft.Text(f"route: {data.route} - Hello from middleware!")))
```

### 3. Declarative Page Routing

By combining `@app.page()` and Flet's `@ft.component`, Flet-Easy natively passes its context directly into declarative components. Notice how you can use native navigation (`ft.context.page.push_route`) right alongside traditional `data.go()` calls!

```python
@ft.component
# Array of middlewares in specific page decorator!
@app.page(route="/", title="Home", middleware=[middleware_home], cache=True)
def home_page(data: fs.Datasy):

    async def go_test():
        await ft.context.page.push_route("/test")

    return ft.View(
        controls=[
            counter(),  # Integrating our stateful component
            ft.Button("go test", on_click=go_test),
            ft.Button("go progress-bar", on_click=data.go("/add-pagesy/progress-bar")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@app.page(route="/test", title="test")
def test(data: fs.Datasy):

    return ft.View(
        controls=[
            ft.Text("test"),
            ft.Button("go back", on_click=data.go("/")),
            ft.Button("go test3", on_click=data.go("/add-pagesy/progress-bar")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
```

### 4. Page Groups and Sub-Routes (`AddPagesy`)

To organize large applications natively, you can group routes using `fs.AddPagesy()`. In v0.3.0, `AddPagesy` now fully supports assigning both Functional **and Class-Based** Middlewares directly!

!!! info "Sub-Router Middleware Execution"
    When you assign `middleware=[func, ClassMd]` to an `AddPagesy` instance, they act as **Sub-Router Middlewares**. They execute *after* any Global middlewares, but *before* your specific Page middlewares.

Here we create a sub-module with a `/add-pagesy` prefix, demonstrating how smoothly `asyncio` and `ft.use_state` work inside Flet-Easy pages.

```python
@dataclass
@ft.observable
class AppState:
    counter: float

    async def start_counter(self):
        self.counter = 0
        for _ in range(0, 10):
            self.counter += 0.1
            await asyncio.sleep(0.5)

# Group routes under a specific prefix
app2 = fs.AddPagesy(
    route_prefix="/add-pagesy",
    middleware=[middleware_home, MiddlewareRoutes], # Array of functional and class-based middleware!
)

@ft.component
@app2.page(route="/progress-bar", title="progress-bar")
def progress_bar(data: fs.Datasy):
    state, _ = ft.use_state(AppState(counter=0))

    async def go_back():
        await ft.context.page.push_route("/")

    return ft.View(
        controls=[
            ft.ProgressBar(state.counter),
            ft.Button("Run!", on_click=state.start_counter),
            ft.Button("go back", on_click=go_back),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# Register the sub-routes and run
app.add_pages([app2])
app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/v0-3-0-showcase/declarative-routing-with-decorators.webm" type="video/webm" alt="Flet-Easy - declarative-routing-with-decorators">
</video>

---

## Example 2: Manual Routing Without Decorators

This example (`tests/render-page.py`) showcases Flet-Easy's impressive ability to handle complex class-based architectures, and how to register them manually using `fs.Pagesy` (bypassing the `@app.page()` decorators entirely).

### 1. View Functions and Declarative Views

Flet-Easy seamlessly bridges URL parameters and the `data` object into declarative components. For instance:

- `home`: An imperative function needing `data: fs.Datasy`.
- `about`: A declarative component. `data: fs.Datasy` is injected optionally if requested!

```python
import flet as ft
import flet_easy as fs

# 1. Standard imperative view function
def home(data: fs.Datasy):
    return ft.View(
        controls=[ft.Text("Home"), ft.Button("go about", on_click=data.go("/about"))],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 2. Declarative component (@ft.component)
@ft.component
def about(data: fs.Datasy):
    async def go_contact(e):
        await ft.context.page.push_route("/contact")

    return ft.View(
        controls=[
            ft.Text("About"),
            ft.Button("go contact", on_click=go_contact),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 3. Declarative component using data.go()
@ft.component
def contact(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Contact"),
            ft.Button("go config", on_click=data.go("/config")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 4. Standard imperative view function without decorator
def config(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Config"),
            ft.Button("go support", on_click=data.go("/support")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )
```

### 2. Class-Based Views

Flet-Easy v0.3.0 brings huge enhancements to OOP architectures!

- `Support`: A classic imperative class. Flet-Easy passes `data` automatically into `__init__`.
- `Profile`: A declarative class with `@ft.component` wrapping the `build()` method. Flet-Easy instantly injects `self.data` without you needing to explicitly declare an `__init__()` method!

```python
# 5. Class-based imperative view.
class Support:
    def __init__(self, data: fs.Datasy):
        self.data = data

    def build(self):
        return ft.View(
            controls=[
                ft.Text("Support"),
                ft.Button("go profile", on_click=self.data.go("/profile")),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )

# 6. Class-based declarative component (v0.3.0+ Feature).
class Profile:
    @ft.component
    def build(self):
        return ft.View(
            controls=[
                ft.Text("Profile"),
                ft.Button("go home", on_click=self.data.go("/")),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )
```

### 3. Registering Pages Manually

Rather than decorating each function, we can instantiate the app, define our middlewares, and explicitly map all of our views through `fs.Pagesy()`.

!!! tip "Page-Specific Overrides"
    Even if you have Global or Sub-Router middlewares protecting a route, you can attach a dedicated `middleware=[...]` directly to a specific `Pagesy()` instance for granular execution control.

```python
# Middleware 1: Functional Middleware
def middleware_home(data: fs.Datasy):
    print(f"before page (function) - route: {data.route} - Hello from middleware!")

# Middleware 2: Class-based Middleware
class MiddlewareDialog(fs.MiddlewareRequest):
    def before_request(self):
        print(f"before page (class) - route: {self.data.route} - Hello from middleware!\n")

    def after_request(self):
        self.data.page.show_dialog(
            ft.SnackBar(
                ft.Text(f"after page (class) - route: {self.data.route} - Hello from middleware!")
            )
        )

# 1. Create app
app = fs.FletEasy()

# 2. Add routes using Pagesy
app.add_routes(
    add_views=[
        # Page-specific middleware override!
        fs.Pagesy(route="/", title="Home", view=home, middleware=[middleware_home, MiddlewareDialog]),
        fs.Pagesy(route="/about", title="About", view=about),
        fs.Pagesy(route="/contact", title="Contact", view=contact),
        fs.Pagesy(route="/config", title="Config", view=config),
        fs.Pagesy(route="/support", title="Support", view=Support),
        fs.Pagesy(route="/profile", title="Profile", view=Profile),
    ]
)

# 3. Add middlewares and run
app.add_middleware(middleware_home, MiddlewareDialog)
app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/v0-3-0-showcase/manual-routing-without-decorators.webm" type="video/webm" alt="Flet-Easy - manual-routing-without-decorators">
</video>

---

## Example 3: Essential Application Scenarios

While the test scripts demonstrate powerful declarative and imperative structures, Flet-Easy v0.3.0 brings massive upgrades for **State, Navigation, and Authentication**. Here are specific snippets mirroring the `CHANGELOG.md` features not fully present in the basic component tests.

### 1. Navigation Bar with `index` Routing

!!! info "More details in [Navigation Bar](../guide/routing/navigation.md#datago_navigation_bar)"

The `NavigationBar` integration is now fully native. Flet-Easy automatically computes tab selections when you use `on_change=data.go_navigation_bar` and define `index` values in your `@app.page()` decorators.

Also note **`data.page_reload()`** and **`data.logout()`**. These v0.3.0 methods execute immediately; no lambda wrapping required inside normal execution flows or event bindings!

```python
@app.view
def global_view(data: fs.Datasy, page: ft.Page):
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("Flet-Easy v0.3.0"),
            actions=[
                ft.IconButton(ft.Icons.REFRESH, on_click=lambda _: data.page_reload()),
                ft.IconButton(ft.Icons.LOGOUT, on_click=lambda _: data.logout("auth_token", next_route="/login")),
            ]
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),  # mapped to index 0
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profile"),  # mapped to index 1
            ],
            on_change=data.go_navigation_bar, # 🆕 Native auto-routing!
        )
    )

@app.page("/home", index=0)
def home_page(data: fs.Datasy):
    return ft.View([ft.Text("I am tab 0!")])
```

### 2. Form Caching and Dynamic Updates

!!! info "More details in [Form Caching](../advanced/page-caching.md)"

Imperative functions support `cache=True`. State changes (like filling forms or incrementing counters) will persist perfectly when you navigate away and come back.

To update cached controls in the background (like live clocks) without disrupting user state, use `data.dynamic_control()`:

```python
@app.page("/cached-form", cache=True) 
def form_page(data: fs.Datasy):
    # This value persists even if you switch tabs!
    form_input = ft.TextField(label="Start typing, move to another page and come back")
    
    # 🆕 dynamic_control runs every time the cached page is visited
    visitors_text = ft.Text("")
    def update_visitors():
        visitors_text.value = f"Visited at {datetime.now().time()}"
    data.dynamic_control(visitors_text, update_visitors)

    return ft.View([form_input, visitors_text])
```

> **Note**: As mentioned in the CHANGELOG, the `cache=True` mechanism currently only works in standard imperative routing. Declarative routing (`@ft.component` classes) does not yet support automatic caching, so persist form data safely into `self.data.page.shared_preferences` instead.

### 3. JWT Authentication

!!! info "More details in [JWT Authentication](../advanced/basic-jwt.md)"

The `SecretKey` and `data.login()` methods power secure encryption naturally. Pass your authentication payloads into `data.login()` or `data.login_async()`, and seamlessly verify identity internally using `decode_jwt()` (or `decode_jwt_async()`). Note that the `next_route` parameter in the login methods is now **mandatory** for secure and immediate redirections.

```python
app = fs.FletEasy(
    route_init="/dashboard",
    route_login="/login",
    secret_key=fs.SecretKey(secret="your-secret-key"),
    logger=True # 🆕 Advanced terminal logging
)

@app.page("/login")
def login(data: fs.Datasy):
    async def handle_login(_):
        # Authenticate asynchronously, store encrypted token, and jump to dashboard
        await data.login_async("auth_token", {"user": "admin", "role": "superuser"}, next_route="/dashboard")
        
    return ft.View([ft.ElevatedButton("Log In", on_click=handle_login)])

@app.login
async def login_required(data: fs.Datasy) -> bool:
    # 🆕 decode_jwt_async is highly recommended over fs.decode_async
    return await data.decode_jwt_async(key_login="auth_token")
```

### 4. Seamless Pop Configurations

When a user triggers a back navigation via the system back button or `page.views.pop()`, you can instantly synchronize Flet-Easy's internal routing engine by passing the event natively into `data.confirm_pop()`.

```python
@app.view
def global_view(data: fs.Datasy, page: ft.Page):
    # Flet-Easy auto-aligns history state seamlessly
    page.on_view_pop = data.confirm_pop
    
    return fs.Viewsy(
        appbar=ft.AppBar(title=ft.Text("Flet-Easy v0.3.0"))
    )
```

### 5. Direct Execution vs Lambdas

!!! info "More details in [Direct Execution vs Lambdas](../guide/routing/navigation.md)"

Flet-Easy v0.3.0 cleanly distinguishes between delayed event triggers and instant executions:

- **`data.go(route)`**: Returns an asynchronous lambda. Perfect for event bindings like `on_click=data.go("/route")`.
- **`data.go_route(route)`**: Executes *immediately*. Use this inside custom functions when you need to trigger a route change manually.
- **`data.go_back()`**: Executes *immediately* to return to the previous path in the history.
- **`data.redirect(route)`**: Executes *immediately*. Typically used within middlewares or decorators to enforce an instant redirect before a page even loads.

### 6. Package Architecture & Modernization

Under the hood, v0.3.0 is completely rebuilt for speed, scale, and modern Python:

- **Package Reorganization**: The monolithic engine has been cleanly split into `core/`, `security/`, and `ui/`, whilst maintaining **100% backward compatibility** with your existing `import flet_easy` imports.
- **Python 3.9+ (PEP 585)**: Full standardization of built-in generics (`list`, `dict`), bringing better IDE hints, zero deprecation warnings, and a leaner router logic.
- **Ultimate Flet Compatibility**: Features robust routing fallbacks designed to safely support legacy Flet `0.27.*` all the way through the `@ft.component` architecture of Flet `0.80.*`.

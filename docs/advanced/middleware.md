# Middleware System

Middleware acts as an intermediary between different software components, intercepting and processing requests and responses. Flet-Easy's middleware system allows you to add functionalities before and after page loading in a flexible and modular way.

## Key Features

!!! note "New in v0.3.0"

* **Function-based Middleware**: Simple functions for basic middleware logic
* **Class-based Middleware**: Enhanced `MiddlewareRequest` class with `before_request` and `after_request` methods
* **Page-specific Middleware**: Apply middleware to individual pages via `AddPagesy`
* **Global Middleware**: Apply middleware to all routes in the application
* **Request/Response Lifecycle**: Control both request processing and response handling

## Middleware Types

### Function-based Middleware (Legacy)

Simple functions that receive a `Datasy` parameter:

```python
def auth_middleware(data: fs.Datasy):
    if data.route == "/login":
        return  # Allow access to login page
    
    token = data.page.client_storage.get("auth_token")
    if not token:
        return data.redirect("/login")

app.add_middleware([auth_middleware])
```

### Class-based Middleware

!!! note "New in v0.3.0"

Enhanced middleware using the `MiddlewareRequest` class:

```python
class AuthMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        """Executed before the page loads"""
        if self.data.route in ["/login", "/register"]:
            return  # Skip auth for public pages
        
        token = self.data.page.client_storage.get("auth_token")
        if not token:
            return fs.Redirect("/login")
    
    def after_request(self):
        """Executed after the page loads"""
        # Log successful page access
        print(f"User accessed: {self.data.route}")

class LoggingMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        print(f"📍 Navigating to: {self.data.route}")
    
    def after_request(self):
        print(f"✅ Loaded: {self.data.route}")

# Apply multiple class-based middlewares
app.add_middleware(AuthMiddleware, LoggingMiddleware)
```

## Available Methods and Attributes

* `data.route`: Current route being accessed
* `data.redirect()`: Redirect to another route
* `data.page`: Access to Flet Page object
* `data.page.client_storage`: Browser storage access
* Return `fs.Redirect("/path")` or `data.redirect("/path")` to redirect
* Return `None` to allow normal page loading

!!! tip "Performance Tip"
    Use class-based middleware for complex logic and better organization. Function-based middleware is suitable for simple checks.

## Execution Hierarchy and Lists

Flet-Easy applies middleware following a strict **Outside-In** hierarchy. If multiple layers of middleware exist for a given route, they execute in this cascading order:

1. **Global Middlewares (`app.add_middleware`)**: Applied to every single route in the application.
2. **Sub-router Middlewares (`fs.AddPagesy(middleware=...)`)**: Applied to all pages belonging to that group/prefix.
3. **Specific Page Middlewares (`@app.page(middleware=...)`)**: Applied only to that specific page.

Additionally, when adding middlewares you can provide a list of mixed types (functions and classes) which execute sequentially from left to right: `middleware=[func_md, ClassMd]`.

```python
# 1. Global
app.add_middleware(GlobalMiddleware)

# 2. Sub-router (Mixed Array)
admin_group = fs.AddPagesy(route_prefix="/admin", middleware=[auth_func, AdminClassMd])

# 3. Page specific
@admin_group.page("/dashboard", middleware=[DashboardSpecificMiddleware])
def dashboard(data: fs.Datasy):
    pass
```

Navigation to `/admin/dashboard` triggers the `before_request` events in order: `Global -> auth_func -> AdminClassMd -> DashboardSpecific`.

## General Application

A global application flow as an alternative to protected-routes:

## Page-specific Middleware

!!! note "New in v0.3.0"

Apply middleware to individual pages using `AddPagesy`. This feature allows you to create middleware that only applies to specific pages or groups of pages.

### Basic Page-Specific Middleware

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/admin/dashboard")


# Authentication middleware
class AuthMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        if self.data.route == "/login":
            return  # Skip auth for login page

        token = self.data.page.client_storage.get("auth_token")
        if not token:
            return fs.Redirect("/login")


# Admin-specific middleware
class AdminMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        user_data = self.data.page.client_storage.get("user_data")
        if not user_data or user_data.get("role") != "admin":
            return fs.Redirect("/unauthorized")

    def after_request(self):
        print(f"+ Admin action logged: {self.data.route}")


# User-specific middleware
class UserMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        print(f"+ User accessing: {self.data.route}")

    async def after_request(self):
        # Async after_request example
        user_data = self.data.page.client_storage.get("user_data")
        if user_data:
            print(f"+ User {user_data.get('name')} completed action")


# Function-based middleware for logging
def request_logger(data: fs.Datasy):
    print(f"📍 Request: {data.route} at {data.page.client_storage.get('timestamp')}")


# Create different page groups with specific middleware
admin_tools = fs.AddPagesy(middleware=[AuthMiddleware, AdminMiddleware, request_logger])

user_tools = fs.AddPagesy(middleware=[AuthMiddleware, UserMiddleware])


# Admin pages
@admin_tools.page(route="/admin/dashboard", title="Admin Dashboard")
def admin_dashboard(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("🔐 Admin Dashboard", size=28),
            ft.Text("Welcome, Administrator!", size=16),
            ft.Row(
                [
                    ft.ElevatedButton("Manage Users", on_click=data.go("/admin/users")),
                    ft.ElevatedButton("System Settings", on_click=data.go("/admin/settings")),
                    ft.ElevatedButton(
                        "Logout", on_click=lambda _: data.logout("auth_token", next_route="/login")
                    ),
                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@admin_tools.page(route="/admin/users", title="User Management")
def admin_users(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("👥 User Management", size=28),
            ft.Text("Manage system users", size=16),
            ft.ElevatedButton("← Back to Dashboard", on_click=data.go("/admin/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@admin_tools.page(route="/admin/settings", title="System Settings")
def admin_settings(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("⚙️ System Settings", size=28),
            ft.Text("Configure system parameters", size=16),
            ft.ElevatedButton("← Back to Dashboard", on_click=data.go("/admin/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# User pages
@user_tools.page(route="/profile", title="User Profile")
def user_profile(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("👤 User Profile", size=28),
            ft.Text("Manage your profile", size=16),
            ft.ElevatedButton("Edit Profile", on_click=lambda _: print("Edit profile")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@user_tools.page(route="/settings", title="User Settings")
def user_settings(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("🔧 User Settings", size=28),
            ft.Text("Customize your experience", size=16),
            ft.ElevatedButton("← Back to Profile", on_click=data.go("/profile")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# Add all page groups to the app
app.add_pages(admin_tools)
app.add_pages(user_tools)


# Public pages (no middleware)
@app.page("/login", title="Login")
def login_page(data: fs.Datasy):
    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)

    def handle_login(_):
        # Simple demo login

        if username_field.value == "" or password_field == "":
            data.page.open(ft.SnackBar(ft.Text("Empty fields")))
            return

        user_data = {
            "name": username_field.value,
            "role": "admin" if username_field.value == "admin" else "user",
        }

        data.page.client_storage.set("user_data", user_data)

        # Redirect based on role
        route = "/admin/dashboard" if user_data["role"] == "admin" else "/profile"

        data.login("auth_token", user_data, next_route=route)

    return ft.View(
        controls=[
            ft.Text("🔐 Login", size=28),
            username_field,
            password_field,
            ft.ElevatedButton("Login", on_click=handle_login),
            ft.Text("Demo: Use 'admin' for admin access", size=12),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


@app.page("/unauthorized", title="Unauthorized")
def unauthorized_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("🚫 Unauthorized", size=28),
            ft.Text("You don't have permission to access this page", size=16),
            ft.ElevatedButton("← Back to Login", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


app.run()
```

### Key Benefits of Page-Specific Middleware

* **🎯 Targeted Security**: Apply authentication/authorization only where needed
* **📊 Granular Logging**: Different logging strategies for different page groups
* **⚡ Performance**: Avoid unnecessary middleware execution on public pages
* **🔧 Modularity**: Organize middleware by functionality or user role
* **🧪 Testing**: Easier to test specific middleware combinations

```python hl_lines="4 12 15 21 25 35 57"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/login", route_login="/login")

db = []  # Database

# -------------------------------------------------------------------------------


# Customized middleware
async def login_middleware(data: fs.Datasy):
    """ If the path is '/login', it will return the None function,
    which will not prevent access to the page. """
    if data.route == "/login":
        return

    username = await data.page.client_storage.get_async("login")
    if username is None or username not in db:
        data.page.open(ft.SnackBar(ft.Text("You are not logged in")))
        return data.redirect("/login")


# Middleware that runs in general, i.e. every time you load a page.
app.add_middleware([login_middleware])
# -------------------------------------------------------------------------------


@app.page(route="/dashboard", title="Dashboard")
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=lambda e: data.logout("login")),
            ft.ElevatedButton("go Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# -------------------------------------------------------------------------------


@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username", width=200)

    def store_login(e):
        db.append(username.value)  # We add to the simulated databas

        """First the values must be stored in the browser, then in the
        login decorator the value must be retrieved through the key used
        and then validations must be used."""
        data.login(key="login", value=username.value, next_route="/dashboard")

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton("store login in browser", on_click=store_login),
            ft.ElevatedButton("go Dashboard", on_click=data.go("/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


app.run()
```

#### **Demo**

<video controls>
  <source src="../../assets/advanced/middleware-general-application.webm" type="video/mp4" alt="Middleware-example">
</video>

## For each page

Another alternative to protected-route

???+ info "Available since version 0.3.0"
    **Class-based Middleware:**

    ```python
    class LoggingMiddleware(fs.MiddlewareRequest):
        def before_request(self):
            print(f"Accessing route: {self.data.route}")
            # Log request details
            
        def after_request(self):
            print(f"Finished processing: {self.data.route}")
            # Log response details
    
    class RateLimitMiddleware(fs.MiddlewareRequest):
        def before_request(self):
            user_id = self.data.page.client_storage.get("user_id")
            if is_rate_limited(user_id):
                return fs.Redirect("/rate-limited")
    
    # Apply class-based middleware
    @app.page(route="/dashboard", title="Dashboard", middleware=[login_middleware, LoggingMiddleware, RateLimitMiddleware])
    ```

```python hl_lines="4 13 15 19 25 45"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/login", route_login="/login")

db = []  # Database

# -------------------------------------------------------------------------------

# Customized middleware
async def login_middleware(data: fs.Datasy):
    username = await data.page.client_storage.get_async("login")
    if username is None or username not in db:
        data.page.open(ft.SnackBar(ft.Text("You are not logged in")))
        return data.redirect("/login")

# -------------------------------------------------------------------------------
# Middleware used to load this page
@app.page(route="/dashboard", title="Dashboard", middleware=[login_middleware])
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=lambda e: data.logout("login")),
            ft.ElevatedButton("go Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# -------------------------------------------------------------------------------

@app.page(route="/login", title="Login")
def login_page(data: fs.Datasy):
    # create login stored user
    username = ft.TextField(label="Username", width=200)

    def store_login(e):
        db.append(username.value)  # We add to the simulated databas

        """First the values must be stored in the browser, then in the
        login decorator the value must be retrieved through the key used
        and then validations must be used."""
        data.login(key="login", value=username.value, next_route="/dashboard")

    return ft.View(
        controls=[
            ft.Text("login", size=30),
            username,
            ft.ElevatedButton("store login in browser", on_click=store_login),
            ft.ElevatedButton("go Dashboard", on_click=data.go("/dashboard")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

## **Demo**

<video controls>
  <source src="../../assets/advanced/middleware-general-application.webm" type="video/webm" alt="Middleware-example">
</video>

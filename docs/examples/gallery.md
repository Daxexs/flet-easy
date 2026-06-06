# Examples Gallery

This gallery showcases practical examples of Flet-Easy applications, from simple demos to complex real-world scenarios.

## Basic Examples

### Hello World App

The quickest way to get started. This example demonstrates how to initialize the Flet-Easy app, register a route, and respond to user events.

**1. App Initialization**  
First, we import the necessary libraries and initialize the `FletEasy` instance. This object manages all the internal routing and configurations of your application.

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy()
```

**2. Defining Pages**  
Use the `@app.page()` decorator to assign a URL route to your view function. The `data` parameter (of type `fs.Datasy`) contains all contextual information, including the current `page` object. We use it to open a SnackBar on button click.

```python
@app.page("/")
def home_page(data: fs.Datasy):
    page = data.page

    # add snack bar
    def add_snack_bar(e):
        page.open(ft.SnackBar(content=ft.Text("Hello World!"), open=True))

    return ft.View(
        controls=[
            ft.Text("Hello, Flet-Easy!", size=30),
            ft.ElevatedButton("Click me!", on_click=add_snack_bar),
        ]
    )
```

**3. Execution**  
Finally, call `app.run()` to start the server.

```python
if __name__ == "__main__":
    app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/hello-world-app.webm" type="video/webm" alt="Flet-Easy - Hello World App">
</video>

### Counter App

This application illustrates how to organize UI controls using Object-Oriented Programming (OOP) and how to persist state across different routes utilizing Flet-Easy's built-in `share_data` functionality.

**1. Reusable UI Components**  
Creating custom classes extending native Flet controls keeps your views clean and maintainable. Here we define custom widgets like `Header`, `NavButton`, and a reactive `CounterCard`.

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy()

# ==========================
# Reusable Components (OOP)
# ==========================
class Header(ft.Container):
    def __init__(self, title: str):
        super().__init__(
            content=ft.Text(
                title,
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(
                vertical=14,
                horizontal=16,
            ),
            border_radius=12,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[
                    ft.Colors.INDIGO_700,
                    ft.Colors.BLUE_700,
                ],
            ),
        )


class NavButton(ft.ElevatedButton):
    def __init__(self, text: str, color: str, on_click):
        super().__init__(
            text,
            on_click=on_click,
            width=140,
            height=48,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=24),
                elevation=6,
            ),
        )


class IconButtonPill(ft.ElevatedButton):
    def __init__(self, text: str, color: str, on_click):
        super().__init__(
            text,
            on_click=on_click,
            width=80,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=4,
            ),
        )


class InfoText(ft.Text):
    def __init__(self, value: str):
        super().__init__(
            value,
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        )


class CounterCard(ft.Container):
    def __init__(self, value: int = 0):
        self._label = ft.Text(
            str(value),
            size=70,
            weight=ft.FontWeight.BOLD,
        )
        super().__init__(
            content=self._label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(24),
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(
                opacity=0.10,
                color=ft.Colors.BLUE_200,
            ),
            border=ft.border.all(
                width=2,
                color=ft.Colors.BLUE_200,
            ),
        )
        self.set_value(value)

    def set_value(self, value: int):
        self._label.value = str(value)
        if value > 0:
            self._label.color = ft.Colors.TEAL_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.TEAL_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.TEAL_300,
            )
        elif value < 0:
            self._label.color = ft.Colors.RED_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.RED_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.RED_300,
            )
        else:
            self._label.color = ft.Colors.BLUE_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.BLUE_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.BLUE_300,
            )
```

**2. Utilizing Shared Data (Home Page)**  
By passing `share_data=True` to the `@app.page` decorator, Flet-Easy automatically maintains a session dictionary `data.share` across all pages. Notice how the counter increments/decrements update both the view and the shared dictionary.

```python
# Demo: share_data=True allows data to persist between pages
@app.page("/", share_data=True)
def counter_page(data: fs.Datasy):
    count = data.share.get("count") or 0
    data.share.set("count", count)
    card = CounterCard(count)

    def increment(_):
        new_count = data.share.get("count") + 1
        data.share.set("count", new_count)
        card.set_value(new_count)
        card.update()
        data.page.update()

    def decrement(_):
        new_count = data.share.get("count") - 1
        data.share.set("count", new_count)
        card.set_value(new_count)
        card.update()
        data.page.update()

    return ft.View(
        controls=[
            Header("Counter Controls"),
            ft.Container(height=16),
            card,

            # Controls
            ft.Container(height=15),
            ft.Row([
                IconButtonPill("−", ft.Colors.RED_600, decrement),
                ft.Container(width=20),
                IconButtonPill("+", ft.Colors.TEAL_600, increment),
            ], alignment=ft.MainAxisAlignment.CENTER),

            # Navigation
            ft.Container(height=20),
            NavButton(
                text="View Value →",
                color=ft.Colors.INDIGO_700,
                on_click=data.go("/display"),
            ),

            # Info
            ft.Container(height=15),
            InfoText("💡 share_data=True: Counter persists between pages"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.GREY_100,
    )
```

**3. Retrieving Shared Data (Display Page)**  
On the second page, we use `data.share.get("count")` to display the exact same value. If `share_data` were omitted, this variable wouldn't persist between navigation events.

```python
# Demo: share_data=True allows accessing the same shared data
@app.page("/display", share_data=True)
def display_page(data: fs.Datasy):
    count = data.share.get("count") or 0

    # Components
    card = CounterCard(count)
    status = ft.Text(
        f"Status: {'↑ Positive' if count > 0 else '→ Zero' if count == 0 else '↓ Negative'}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREY_800,
        text_align=ft.TextAlign.CENTER,
    )

    return ft.View(
        controls=[
            Header("Shared Value"),
            ft.Container(height=16),
            card,
            ft.Container(height=12),
            status,
            ft.Container(height=20),
            NavButton(
                text="← Back to Controls",
                color=ft.Colors.AMBER_700,
                on_click=data.go("/"),
            ),
            ft.Container(height=12),
            InfoText("🔄 Same shared value from previous page"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.GREY_100,
    )
```

**4. Execution**  
Run the application as usual.

```python
# Run the demo app
if __name__ == "__main__":
    app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/counter-app.webm" type="video/webm" alt="Flet-Easy - Counter App">
</video>

### Comprehensive Application

!!! info "Compatible with flet < 0.80.0 by using `page.client_storage`, change to `data.shared_preferences` or `ft.SharedPreferences` for compatibility."

This advanced example demonstrates the full capabilities of Flet-Easy v0.3.0 in a complete, router-based application. It serves as an excellent production-ready template incorporating **Authentication**, **Navigation**, **Middlewares**, and **Page Caching**.

#### 🎬 Application Demo

<video controls>
  <source src="../../assets/examples/example-0.3.0v.webm" type="video/webm" alt="Flet-Easy - v0.3.0 Showcase">
</video>

<br>

#### Feature Breakdown

- 🧭 **Native NavigationBar**: Uses the new `index` parameter and `data.go_navigation_bar` to automatically handle tab selection natively.
- 🛡️ **Enhanced Class-Based Middlewares**:
  - **Authentication Guard**: A global middleware that protects routes and safely redirects guests to `/login`.
  - **Performance Monitor**: Logs precise load-times utilizing `before_request` and `after_request` hooks.
  - **Page-Specific Guards**: An `AdminMiddleware` applied exclusively to `/admin/*` routes to enforce role-based access.
- 💾 **Smart Form Caching (`cache=True`)**: Pages like `/home` and `/settings` seamlessly maintain their form data and UI states when navigating between tabs.
- ⚡ **Dynamic Background Updates**: Uses `data.dynamic_control()` to update UI elements safely while the page is cached.
- 🚀 **Direct Executions**: Employs `data.page_reload()`, `data.logout()`, and `data.go_route()` for instant, lambda-less routing in button callbacks.

#### Source Code Breakdown

**1. App Initialization**  
Import dependencies, create the Flet-Easy instance, and set global settings such as `Themes` directly via `@app.config`.

```python
import flet as ft
import flet_easy as fs
from datetime import datetime
import asyncio

# compatible with flet < 0.80.0 for using page.client_storage

# Create app with enhanced v0.3.0 features
app = fs.FletEasy(
    route_init="/home",
    on_keyboard=True,
    on_resize=True,
    secret_key=fs.SecretKey(secret="your-secret-key-here"),
)


@app.config
def config(page: ft.Page):
    """Initial page configuration"""
    page.theme_mode = ft.ThemeMode.DARK
```

**2. Global View Configuration**  
Instead of explicitly placing navigation wrappers on every single page, `Flet-Easy` lets you define a master layout through `@app.view()`. The view returns a `fs.Viewsy` component that injects the `NavigationBar` and `AppBar` into all connected pages seamlessly using `data.go_navigation_bar`.

```python
# Global View Configuration
@app.view
def main_view(data: fs.Datasy):
    """Configure global app layout with NavigationBar integration"""

    def handle_logout(e):
        """Enhanced logout with v0.3.0 direct execution"""
        # Clear multiple storage keys and redirect to login
        data.logout(
            "auth_token", next_route="/login"
        )  # 🆕 v0.3.0 - Executes directly with redirect
        # For additional cleanup, use page.client_storage directly
        data.page.client_storage.remove("user_data")

    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("Flet-Easy v0.3.0 Demo"),
            bgcolor=ft.Colors.BLUE,
            actions=[
                ft.IconButton(
                    ft.Icons.REFRESH,
                    tooltip="Reload Page",
                    on_click=lambda _: data.page_reload(),  # 🆕 v0.3.0
                ),
                ft.IconButton(ft.Icons.LOGOUT, tooltip="Logout", on_click=handle_logout),
            ],
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME, selected_icon=ft.Icons.HOME_FILLED, label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.DASHBOARD,
                    selected_icon=ft.Icons.DASHBOARD_OUTLINED,
                    label="Dashboard",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON, selected_icon=ft.Icons.PERSON_OUTLINED, label="Profile"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS,
                    selected_icon=ft.Icons.SETTINGS_OUTLINED,
                    label="Settings",
                ),
            ],
            on_change=data.go_navigation_bar,  # 🆕 v0.3.0 - Direct integration
        ),
        bgcolor=ft.Colors.GREY_50,
        padding=ft.padding.all(20),
    )
```

**3. Class-Based Middlewares**  
Middlewares intercept requests before they load (`before_request`) or post-loading (`after_request`). Here, `AuthenticationMiddleware` ensures unauthenticated users are booted to the login page smoothly.

```python
# Enhanced Middleware System
class AuthenticationMiddleware(fs.MiddlewareRequest):
    """🆕 v0.3.0 - Class-based middleware with before/after hooks"""

    def before_request(self):
        """Execute before page loads"""
        # Skip auth for public pages
        public_routes = ["/login", "/register", "/about"]
        if self.data.route in public_routes:
            return

        # Check authentication
        token = self.data.page.client_storage.get("auth_token")
        if not token:
            return fs.Redirect("/login")

    def after_request(self):
        """Execute after page loads"""
        # Log successful access
        user = self.data.page.client_storage.get("user_data")
        if user:
            print(f"✅ User {user.get('name', 'Unknown')} accessed {self.data.route}")


class PerformanceMiddleware(fs.MiddlewareRequest):
    """🆕 v0.3.0 - Performance monitoring middleware"""

    def before_request(self):
        # Store request start time
        self.start_time = datetime.now()
        print(f"🚀 Loading {self.data.route}...")

    def after_request(self):
        # Calculate and log load time
        if hasattr(self, "start_time"):
            load_time = (datetime.now() - self.start_time).total_seconds()
            print(f"⏱️  {self.data.route} loaded in {load_time:.3f}s")


# Apply global middleware
app.add_middleware(AuthenticationMiddleware, PerformanceMiddleware)
```

**4. Smart Caching with Dynamic Updates (Home Page)**  
Notice `cache=True` in the decorator. The counter state will freeze flawlessly when you swap tabs. To display real-time updates (like the clock in the AppBar) *without* re-rendering the cached page, we register `data.dynamic_control()`.

```python
# Pages with Navigation Integration
@app.page("/home", title="Home", index=0, cache=True)  # 🆕 v0.3.0
def home_page(data: fs.Datasy):
    """Home page with dynamic controls and caching"""

    # Dynamic appbar title update
    def update_welcome_message(appbar):
        current_time = datetime.now().strftime("%H:%M")
        appbar.title = ft.Text(f"Welcome! ({current_time})")
        data.page.update()

    # 🆕 v0.3.0 - Register dynamic control for cached page
    data.dynamic_control(data.view.appbar, update_welcome_message)

    # Counter that persists due to cache=True
    counter_text = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)

    def increment(_):
        current = int(counter_text.value)
        counter_text.value = str(current + 1)
        data.page.update()

    def decrement(_):
        current = int(counter_text.value)
        counter_text.value = str(max(0, current - 1))
        data.page.update()

    return ft.View(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "🏠 Welcome to Flet-Easy v0.3.0!", size=28, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "This page demonstrates caching - your counter persists!",
                            size=16,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Container(height=20),
                        # Persistent counter (due to cache=True)
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Persistent Counter", size=18),
                                        counter_text,
                                        ft.Row(
                                            [
                                                ft.IconButton(
                                                    ft.Icons.REMOVE,
                                                    on_click=decrement,
                                                    bgcolor=ft.Colors.RED_100,
                                                ),
                                                ft.IconButton(
                                                    ft.Icons.ADD,
                                                    on_click=increment,
                                                    bgcolor=ft.Colors.GREEN_100,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=20,
                            )
                        ),
                        ft.Container(height=20),
                        # Navigation examples
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Go to Dashboard",
                                    on_click=lambda _: data.go_route("/dashboard"),  # 🆕 v0.3.0
                                ),
                                ft.ElevatedButton(
                                    "Quick Profile",
                                    on_click=data.go("/profile"),  # Traditional method
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

**5. Non-Cached Pages with Asynchronous Event Loops (Dashboard)**  
The Dashboard sets `cache=False`, meaning its state drops when you leave. Here we leverage Python's `async/await` directly in the page builder, running endless background tasks exclusively while the user views it.

```python
# Dashboard page without caching
@app.page("/dashboard", title="Dashboard", index=1, cache=False)  # 🆕 v0.3.0
async def dashboard_page(data: fs.Datasy):
    """Dashboard with real-time data (no caching)"""

    # This will reset every time due to cache=False
    live_data = ft.Text("Loading...", size=16)

    async def update_live_data():
        """Simulate live data updates"""
        counter = 0
        try:
            while True:
                live_data.value = (
                    f"Live Data: {counter} (Updated: {datetime.now().strftime('%H:%M:%S')})"
                )
                counter += 1
                data.page.update()
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            pass

    # Start live data updates using Flet's recommended way
    data.page.run_task(update_live_data)

    return ft.View(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📊 Dashboard", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "This page resets on each visit (cache=False)",
                            size=16,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Real-time Data", size=18),
                                        live_data,
                                        ft.ProgressRing(width=16, height=16, stroke_width=2),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=20,
                            )
                        ),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "← Back to Home",
                            on_click=lambda _: data.go_back(),  # 🆕 v0.3.0 - Direct execution
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

**6. State Preservation in Forms (Profile & Settings)**  
More usages of `cache=True`. Try filling the profile details, selecting "Dark Mode" on the settings pane, and jumping across the Navigation Bar. You'll notice no values are lost upon your return.

```python
@app.page("/profile", title="Profile", index=2, cache=True)
def profile_page(data: fs.Datasy):
    """User profile with persistent form data"""

    # Form fields that persist due to caching
    name_field = ft.TextField(label="Full Name", width=300)
    email_field = ft.TextField(label="Email", width=300)
    bio_field = ft.TextField(label="Bio", multiline=True, min_lines=3, max_lines=5, width=300)

    def save_profile(_):
        # Save to client storage
        profile_data = {
            "name": name_field.value,
            "email": email_field.value,
            "bio": bio_field.value,
            "updated": datetime.now().isoformat(),
        }
        data.page.client_storage.set("profile", profile_data)

        # Show success message
        data.page.open(
            ft.SnackBar(content=ft.Text("✅ Profile saved successfully!"), bgcolor=ft.Colors.GREEN)
        )

    def load_profile(_):
        # Load from client storage
        profile_data = data.page.client_storage.get("profile")
        if profile_data:
            name_field.value = profile_data.get("name", "")
            email_field.value = profile_data.get("email", "")
            bio_field.value = profile_data.get("bio", "")
            data.page.update()

    def reset_profile(_):
        # Clear profile data
        data.page.client_storage.remove("profile")
        data.page_reload()

    # Load profile on page load
    load_profile(None)

    return ft.View(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("👤 User Profile", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Form data persists due to caching", size=16, color=ft.Colors.GREY_700
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        name_field,
                                        email_field,
                                        bio_field,
                                        ft.Container(height=20),
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "💾 Save Profile",
                                                    on_click=save_profile,
                                                    bgcolor=ft.Colors.BLUE,
                                                ),
                                                ft.ElevatedButton(
                                                    "🔄 Reset Form",
                                                    on_click=reset_profile,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=20,
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

```python
@app.page("/settings", title="Settings", index=3, cache=True)
def settings_page(data: fs.Datasy):
    """Settings page with theme switching and preferences"""

    # Theme switch
    dark_mode_switch = ft.Switch(
        label="🌙 Dark Mode", value=data.page.theme_mode == ft.ThemeMode.DARK
    )

    def toggle_theme(e):
        if dark_mode_switch.value:
            data.page.theme_mode = ft.ThemeMode.DARK
        else:
            data.page.theme_mode = ft.ThemeMode.LIGHT
        data.page.update()

    dark_mode_switch.on_change = toggle_theme

    # Notification settings
    notifications_switch = ft.Switch(label="🔔 Notifications", value=True)
    auto_save_switch = ft.Switch(label="💾 Auto-save", value=False)

    return ft.View(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("⚙️ Settings", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Configure your app preferences", size=16, color=ft.Colors.GREY_700
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Appearance", size=18, weight=ft.FontWeight.BOLD),
                                        dark_mode_switch,
                                        ft.Divider(),
                                        ft.Text("Preferences", size=18, weight=ft.FontWeight.BOLD),
                                        notifications_switch,
                                        auto_save_switch,
                                        ft.Container(height=20),
                                        ft.ElevatedButton(
                                            "🔄 Reset to Defaults",
                                            on_click=lambda _: data.page_reload(),
                                        ),
                                    ]
                                ),
                                padding=20,
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

**7. Route-Specific Protection (Admin & Login)**  
You can chain custom middlewares to specific arrays of routes using `middleware=[AdminMiddleware]`. The robust `data.login()` method automatically issues an encrypted token payload enabling secure validation.

```python
class AdminMiddleware(fs.MiddlewareRequest):
"""🆕 v0.3.0 - Page-specific middleware for admin routes"""

    def before_request(self):
        user_data = self.data.page.client_storage.get("user_data")
        if not user_data or user_data.get("role") != "admin":
            return fs.Redirect("/unauthorized")


def admin_dashboard_view(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("🔐 Admin Dashboard", size=24),
            ft.Text("Only admins can see this page"),
        ]
    )


def admin_users_view(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("� User Management", size=24),
            ft.Text("Manage application users"),
        ]
    )


# Create admin pages with specific middleware
admin_pages = [
    fs.Pagesy(
        "/admin/dashboard",
        admin_dashboard_view,
        title="Admin Dashboard",
        middleware=[AdminMiddleware],  # 🆕 v0.3.0 - Page-specific middleware
    ),
    fs.Pagesy(
        "/admin/users", admin_users_view, title="User Management", middleware=[AdminMiddleware]
    ),
]

app.add_routes(admin_pages)
```

```python
@app.page("/login", title="Login")
def login_page(data: fs.Datasy):
    """Login page with authentication"""

    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)

    def handle_login(_):
        username = username_field.value
        password = password_field.value

        # Simple validation (replace with real authentication)
        if username and password:
            # Store authentication data
            user_data = {
                "name": username,
                "role": "admin" if username == "admin" else "user",
                "login_time": datetime.now().isoformat(),
            }

            data.login("auth_token", user_data, next_route="/home")
        else:
            data.page.open(
                ft.SnackBar(
                    content=ft.Text("❌ Please enter username and password"), bgcolor=ft.Colors.RED
                )
            )

    return ft.View(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("🔐 Login", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Enter your credentials to continue", size=16),
                        ft.Container(height=30),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        username_field,
                                        password_field,
                                        ft.Container(height=20),
                                        ft.ElevatedButton(
                                            "🚀 Login",
                                            on_click=handle_login,
                                            width=300,
                                            bgcolor=ft.Colors.BLUE,
                                        ),
                                        ft.Container(height=10),
                                        ft.Text(
                                            "Demo: Use any username/password",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=30,
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

**8. Entry Point**  

```python
# Run the application
if __name__ == "__main__":
    app.run()
```

----

## More Examples

For additional examples and tutorials, visit:

- [GitHub Repository Examples](https://github.com/Daxexs/flet-easy/tree/main/tests)

Each example includes:

- Complete source code
- Step-by-step explanations
- Best practices
- Common pitfalls to avoid
- Extension ideas

Start with the basic examples and gradually work your way up to more complex applications as you become comfortable with Flet-Easy concepts.

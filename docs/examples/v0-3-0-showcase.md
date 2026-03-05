# v0.3.0 Feature Showcase

This comprehensive example demonstrates all the new features introduced in Flet-Easy v0.3.0, including navigation bar integration, page caching, dynamic controls, enhanced middleware, and more.

## Complete Application Example

### App Setup with Advanced Configuration

```python
import flet as ft
import flet_easy as fs
from datetime import datetime
import asyncio

# Create app with enhanced v0.3.0 features
app = fs.FletEasy(
    route_init="/home",
    on_keyboard=True,
    on_resize=True,
    secret_key=fs.SecretKey(secret="your-secret-key-here")
)

@app.config
def config(page: ft.Page):
    """Initial page configuration"""
    page.theme_mode = ft.ThemeMode.DARK
```

### Global View Configuration

```python
@app.view
def main_view(data: fs.Datasy):
    """Configure global app layout with NavigationBar integration"""

    def handle_logout(e):
        """Enhanced logout with v0.3.0 direct execution"""
        # Clear multiple storage keys and redirect to login
        data.logout("auth_token", next_route="/login")  # 🆕 v0.3.0 - Executes directly with redirect
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
                    on_click=lambda _: data.page_reload()  # 🆕 v0.3.0
                ),
                ft.IconButton(
                    ft.Icons.LOGOUT,
                    tooltip="Logout",
                    on_click=handle_logout
                )
            ]
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME_FILLED,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.DASHBOARD,
                    selected_icon=ft.Icons.DASHBOARD_OUTLINED,
                    label="Dashboard"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON,
                    selected_icon=ft.Icons.PERSON_OUTLINED,
                    label="Profile"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS,
                    selected_icon=ft.Icons.SETTINGS_OUTLINED,
                    label="Settings"
                ),
            ],
            on_change=data.go_navigation_bar  # 🆕 v0.3.0 - Direct integration
        ),
        bgcolor=ft.Colors.GREY_50,
        padding=ft.padding.all(20)
    )
```

### Enhanced Middleware System

```python
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
        if hasattr(self, 'start_time'):
            load_time = (datetime.now() - self.start_time).total_seconds()
            print(f"⏱️  {self.data.route} loaded in {load_time:.3f}s")

# Apply global middleware
app.add_middleware(AuthenticationMiddleware, PerformanceMiddleware)
```

### Pages with Navigation Integration

```python
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

### Page-Specific Middleware

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

### Login Page

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

# Run the application
if __name__ == "__main__":
    app.run()
```

### JWT Authentication with `decode_jwt`

!!! note "Replaced `fs.decode` and `fs.decode_async`"

* **`data.decode_jwt(key)`**: Decode JWT synchronously from `Datasy`
* **`data.decode_jwt_async(key)`**: Decode JWT asynchronously — preferred in `async` login decorators

```python
import flet_easy as fs

app = fs.FletEasy(
    route_init="/home",
    route_login="/login",
    secret_key=fs.SecretKey(
        algorithm=fs.Algorithm.HS256,
        secret="your-secret-key",
    ),
    auto_logout=True,
)

# Decode JWT in the login decorator (recommended: async)
@app.login
async def login_required(data: fs.Datasy) -> bool:
    return await data.decode_jwt_async(key_login="auth_token")

# Equivalent sync version (uses run_task internally)
@app.login
def login_required_sync(data: fs.Datasy) -> bool:
    return data.decode_jwt(key_login="auth_token")
```

### 🎬 Demo

<video controls>
  <source src="../../assets/examples/example-0.3.0v.webm" type="video/webm" alt="Flet-Easy - v0.3.0 Showcase">
</video>

## Key v0.3.0 Features Demonstrated

### Navigation Bar Integration

!!! note "New in v0.3.0"

* **`index` parameter**: Automatic page mapping with NavigationBar
* **`go_navigation_bar()`**: Direct method for handling navigation changes
* **Seamless switching**: No manual index management required

### Page Caching System

!!! note "New in v0.3.0"

* **`cache=True/False`**: Control page state persistence
* **Form preservation**: Input fields retain values when navigating
* **Performance optimization**: Reduce re-rendering for complex pages

### Dynamic Controls

!!! note "New in v0.3.0"

* **`dynamic_control()`**: Real-time updates for cached pages
* **Live updates**: Modify controls without losing page state
* **Enhanced UX**: Smooth interactions with preserved context

### Enhanced Middleware

!!! note "New in v0.3.0"

* **Class-based middleware**: `MiddlewareRequest` with before/after hooks
* **Page-specific middleware**: Apply middleware to individual pages via `AddPagesy`
* **Better organization**: Separate concerns with dedicated middleware classes

### Direct Method Execution

!!! note "New in v0.3.0"

* **`go_route()`**: Immediate navigation without lambda wrappers
* **`go_back()`**: Direct execution instead of returning functions
* **`logout()`**: Immediate logout action with optional `next_route`
* **`page_reload()`**: Instant page refresh and state reset

### Python 3.9 Support

!!! note "New in v0.3.0"

* **Compatibility**: Extended support for Python 3.9+
* **Performance**: Optimized for newer Python versions
* **Future-ready**: Prepared for upcoming Python features

This comprehensive example showcases the power and flexibility of Flet-Easy v0.3.0, demonstrating how these new features work together to create more intuitive, performant, and maintainable applications.

# Page Management (Pagesy)

The `Pagesy` class is the foundation for defining pages in Flet-Easy applications. It provides comprehensive configuration options for routing, middleware, authentication, caching, and parameter validation.

## Overview

`Pagesy` enables you to:

- **Define Routes**: Create URL patterns with dynamic parameters
- **Configure Security**: Set up route protection and authentication
- **Add Middleware**: Implement request/response processing
- **Enable Caching**: Preserve page state during navigation
- **Validate Parameters**: Custom validation for route parameters
- **Share Data**: Enable cross-page data sharing

## Class Definition

```python
class Pagesy:
    def __init__(
        self,
        route: str,
        view: ViewHandler,
        title: Optional[str] = None,
        index: Optional[int] = None,
        clear: bool = False,
        share_data: bool = False,
        protected_route: bool = False,
        custom_params: Optional[Dict[str, Callable[[], bool]]] = None,
        middleware: Optional[Middleware] = None,
        cache: bool = False
    )
```

## Parameters

### `route` (Required)

- **Type**: `str`
- **Description**: URL pattern for the page, supports dynamic parameters

**Static Routes:**

```python
# Simple static route
Pagesy("/home", home_view)
Pagesy("/about", about_view)
Pagesy("/contact", contact_view)
```

**Dynamic Routes:**

```python
# Integer parameter
Pagesy("/user/{id:int}", user_view)

# String parameter
Pagesy("/category/{name:str}", category_view)

# Multiple parameters
Pagesy("/blog/{year:int}/{month:int}/{slug:str}", blog_post_view)

# Optional parameters with defaults
Pagesy("/search/{query:str}/{page:int}", search_view)
```

**Parameter Types:**

- `{name:int}` - Integer
- `{name:str}` - String
- `{name:str}` - Lowercase string
- `{name:float}` - Float

### `view` (Required)

- **Type**: `ViewHandler` (Callable[[Datasy], View])
- **Description**: Function that returns a Flet View

```python
def my_page_view(data: fs.Datasy) -> ft.View:
    return ft.View(
        controls=[
            ft.Text("Hello World!")
        ]
    )

# Register the page
page = Pagesy("/my-page", my_page_view)
```

### `title`

- **Type**: `Optional[str]`
- **Default**: `None`
- **Description**: Page title displayed in browser/window title bar

```python
Pagesy("/dashboard", dashboard_view, title="User Dashboard")
Pagesy("/settings", settings_view, title="Application Settings")
```

### `index`

!!! Note "New in v0.3.0"

- **Type**: `Optional[int]`
- **Default**: `None`
- **Description**: Navigation index for use with `ft.NavigationBar` and `ft.CupertinoNavigationBar`

```python
# Define pages with navigation indices
Pagesy("/home", home_view, title="Home", index=0)
Pagesy("/search", search_view, title="Search", index=1)
Pagesy("/profile", profile_view, title="Profile", index=2)

# Use with NavigationBar
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profile"),
            ],
            on_change=data.go_navigation_bar  # Automatically handles index mapping
        )
    )
```

### `cache`

!!! Note "New in v0.3.0"

- **Type**: `bool`
- **Default**: `False`
- **Description**: Preserve page state when navigating. Controls retain their values instead of resetting

```python
# Enable caching - page state preserved
Pagesy("/form", form_view, cache=True)

# Disable caching - page resets on each visit (default)
Pagesy("/live-feed", feed_view, cache=False)

# Example: Form with caching
@app.page("/user-form", cache=True)
def user_form(data: fs.Datasy):
    # These fields will retain their values when navigating away and back
    name_field = ft.TextField(label="Name")
    email_field = ft.TextField(label="Email")
    
    return ft.View(
        controls=[
            ft.Text("User Information Form"),
            name_field,
            email_field,
            ft.ElevatedButton("Save Draft", on_click=lambda _: data.go("/dashboard")),
            ft.ElevatedButton("Reset", on_click=lambda _: data.page_reload())
        ]
    )
```

### `clear`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Remove pages from the `page.views` list of Flet (deprecated - use with caution)

```python
# Clear navigation history when accessing this page
Pagesy("/login", login_view, clear=True)
Pagesy("/profile", profile_view, index=2)

# Use in NavigationBar
navigation_bar = ft.NavigationBar(
    selected_index=data.current_page_index,  # Use the index
    destinations=[
        ft.NavigationDestination(icon=ft.Icons.HOME, label="Home"),
        ft.NavigationDestination(icon=ft.Icons.SEARCH, label="Search"),
        ft.NavigationDestination(icon=ft.Icons.PERSON, label="Profile"),
    ]
)
```

### `clear`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Clears navigation history when navigating to this page

```python
# Clear history for main landing pages
Pagesy("/home", home_view, clear=True)
Pagesy("/login", login_view, clear=True)

# Preserve history for detail pages
Pagesy("/user/{id:int}", user_detail_view, clear=False)
```

### `share_data`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Enables data sharing between pages using session storage

```python
# Enable data sharing for form wizard pages
Pagesy("/wizard/step1", step1_view, share_data=True)
Pagesy("/wizard/step2", step2_view, share_data=True)
Pagesy("/wizard/step3", step3_view, share_data=True)

def step1_view(data: fs.Datasy):
    def save_and_continue(_):
        # Save form data
        data.share.set("user_info", {
            "name": name_field.value,
            "email": email_field.value
        })
        data.go("/wizard/step2")
    
    return ft.View("/wizard/step1", controls=[...])

def step2_view(data: fs.Datasy):
    # Access data from step1
    user_info = data.share.get("user_info")
    return ft.View("/wizard/step2", controls=[...])
```

### `protected_route`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Requires authentication to access the page

```python
# Public pages
Pagesy("/home", home_view, protected_route=False)
Pagesy("/login", login_view, protected_route=False)

# Protected pages
Pagesy("/dashboard", dashboard_view, protected_route=True)
Pagesy("/admin", admin_view, protected_route=True)
Pagesy("/user/{id:int}/edit", edit_user_view, protected_route=True)

# Configure authentication handler in FletEasy
@app.login
def check_auth(data: fs.Datasy):
    token = data.page.client_storage.get("auth_token")
    return token is not None and verify_token(token)
```

### `custom_params`

- **Type**: `Optional[Dict[str, Callable[[], bool]]]`
- **Default**: `None`
- **Description**: Custom validators for route parameters

```python
def validate_user_id(user_id: str) -> bool:
    """Validate that user ID exists in database"""
    return user_exists(int(user_id))

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Apply custom validators
Pagesy(
    "/user/{id:id_profile}/profile",
    user_profile_view,
    custom_params={"id_profile": validate_user_id}
)

Pagesy(
    "/contact/{email:email_contact}",
    contact_view,
    custom_params={"email_contact": validate_email}
)

Pagesy(
    "/events/{date:date_event}",
    events_view,
    custom_params={"date_event": validate_date}
)
```

### `middleware`

- **Type**: `Optional[Middleware]`
- **Description**: Request/response processing pipeline

**Function-based Middleware:**

```python
def auth_middleware(data: fs.Datasy) -> Optional[fs.Redirect]:
    """Check if user is authenticated"""
    if not data.page.client_storage.get("auth_token"):
        return fs.Redirect("/login")
    return None

def admin_middleware(data: fs.Datasy) -> Optional[fs.Redirect]:
    """Check if user has admin privileges"""
    user_role = data.page.client_storage.get("user_role")
    if user_role != "admin":
        return fs.Redirect("/unauthorized")
    return None

# Apply middleware
Pagesy(
    "/admin/users",
    admin_users_view,
    middleware=[auth_middleware, admin_middleware]
)
```

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
Pagesy(
    "/api/data",
    api_data_view,
    middleware=[LoggingMiddleware, RateLimitMiddleware]
)
```

### `cache`

- **Type**: `bool`
- **Default**: `False`
- **Description**: Preserves page state during navigation

```python
# Cache expensive-to-render pages
Pagesy("/reports/dashboard", title="Dashboard", view=reports_view, cache=True)
Pagesy("/data/visualization", title="Visualization", view=charts_view, cache=True)

# Don't cache dynamic pages
Pagesy("/live/feed", title="Live Feed", view=live_feed_view, cache=False)
Pagesy("/user/{id:int}/messages", title="Messages", view=messages_view, cache=False)

def reports_view(data: fs.Datasy):
    # This page state will be preserved when user navigates away and back
    expensive_chart = generate_complex_chart()
    
    return ft.View(
        controls=[expensive_chart]
    )
```

## Complete Examples

### Multi-step Form with Data Sharing

This example demonstrates how to create a **multi-step registration form** where data persists across different pages using `share_data=True`. This is ideal for wizards, checkout processes, or any workflow that requires multiple steps.

#### What You'll Learn

- **Share data between pages** using `data.share`
- **Validate and persist form data** across navigation
- **Implement navigation guards** to prevent skipping steps
- **Handle back navigation** while preserving user input

#### How It Works

The form has 3 steps:

1. **Step 1**: Collect personal information (name, email, phone)
2. **Step 2**: Collect address information (address, city)
3. **Step 3**: Display a summary of all collected data

All data is stored in `data.share` with the key `"registration_form"`, making it accessible across all pages.

#### Key Concepts

**`data.share.get(key)`**: Retrieves shared data by key. Returns `None` if not found.

**`data.share.set(key, value)`**: Stores data that persists across page navigation.

**`data.share.clear()`**: Removes all shared data (useful for resetting the form).

**`share_data=True`**: Must be enabled in `Pagesy` to use shared data functionality.

```python
import flet as ft
import flet_easy as fs


# ========================================
# STEP 1: Personal Information
# ========================================
def step1_view(data: fs.Datasy):
    """First step: Collect user's personal information"""
    
    # 1. Load existing data (if user navigates back to this step)
    form_data = data.share.get("registration_form") or {}

    # 2. Create text fields with saved values (if any)
    name_field = ft.TextField(
        label="Full Name", 
        value=form_data.get("name", "")
    )
    email_field = ft.TextField(
        label="Email", 
        value=form_data.get("email", "")
    )
    phone_field = ft.TextField(
        label="Phone", 
        value=form_data.get("phone", "")
    )

    def save_and_continue(_):
        """Validate, save data, and navigate to next step"""
        
        # Validate required fields
        if not name_field.value or not email_field.value:
            data.page.open(
                ft.SnackBar(content=ft.Text("Please fill all required fields"))
            )
            return

        # Get current form data and update with new values
        form_data = data.share.get("registration_form") or {}
        form_data.update({
            "name": name_field.value,
            "email": email_field.value,
            "phone": phone_field.value
        })
        
        # Save to shared storage
        data.share.set("registration_form", form_data)

        # Navigate to step 2
        data.go_route("/register/step2")
    
    def reload_page(e):
        """Clear all form data and reload the page"""
        data.share.clear()
        data.page_reload()

    return ft.View(
        controls=[
            ft.Text("Registration - Step 1", size=24, weight="bold"),
            ft.Text("Personal Information", size=16, color="grey"),
            ft.Divider(height=20),
            name_field,
            email_field,
            phone_field,
            ft.Row(
                [
                    ft.ElevatedButton("Next →", on_click=save_and_continue),
                    ft.OutlinedButton("Reset", on_click=reload_page),
                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        padding=20,
    )


# ========================================
# STEP 2: Address Information
# ========================================
def step2_view(data: fs.Datasy):
    """Second step: Collect user's address information"""
    
    # 1. Load form data
    form_data = data.share.get("registration_form") or {}

    # 2. Navigation guard: Redirect to step 1 if not completed
    if not form_data.get("name"):
        data.go_route("/register/step1")
        return ft.View("/register/step2", controls=[])

    # 3. Create address fields with saved values
    address_field = ft.TextField(
        label="Address", 
        value=form_data.get("address", "")
    )
    city_field = ft.TextField(
        label="City", 
        value=form_data.get("city", "")
    )

    def save_and_continue(_):
        """Save address data and go to confirmation"""
        form_data = data.share.get("registration_form") or {}
        form_data.update({
            "address": address_field.value,
            "city": city_field.value
        })
        data.share.set("registration_form", form_data)
        data.go_route("/register/step3")

    def go_back(_):
        """Save current data before going back to step 1"""
        form_data = data.share.get("registration_form") or {}
        form_data.update({
            "address": address_field.value,
            "city": city_field.value
        })
        data.share.set("registration_form", form_data)
        data.go_route("/register/step1")

    return ft.View(
        controls=[
            ft.Text("Registration - Step 2", size=24, weight="bold"),
            ft.Text("Address Information", size=16, color="grey"),
            ft.Divider(height=20),
            address_field,
            city_field,
            ft.Row(
                [
                    ft.OutlinedButton("← Back", on_click=go_back),
                    ft.ElevatedButton("Next →", on_click=save_and_continue),
                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        padding=20,
    )


# ========================================
# STEP 3: Confirmation
# ========================================
def step3_view(data: fs.Datasy):
    """Final step: Display summary of all collected data"""
    
    # Load all form data
    form_data = data.share.get("registration_form") or {}
    
    return ft.View(
        controls=[
            ft.Text("Registration - Step 3", size=24, weight="bold"),
            ft.Text("Confirmation", size=16, color="grey"),
            ft.Divider(height=20),
            
            # Display collected information
            ft.Container(
                content=ft.Column([
                    ft.Text("📋 Summary", size=18, weight="bold"),
                    ft.Divider(),
                    ft.Text(f"Name: {form_data.get('name', 'N/A')}"),
                    ft.Text(f"Email: {form_data.get('email', 'N/A')}"),
                    ft.Text(f"Phone: {form_data.get('phone', 'N/A')}"),
                    ft.Text(f"Address: {form_data.get('address', 'N/A')}"),
                    ft.Text(f"City: {form_data.get('city', 'N/A')}"),
                ]),
                padding=20,
                border=ft.border.all(1, "grey"),
                border_radius=10,
            ),
            
            ft.Row(
                [
                    ft.OutlinedButton("← Back", on_click=data.go_back),
                    ft.ElevatedButton("🏠 Home", on_click=data.go(data.route_init)),
                ],
                alignment="center",
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        padding=20,
    )


# ========================================
# MAIN APPLICATION
# ========================================
def main(page: ft.Page):
    """Initialize and configure the multi-step form application"""
    
    # Create app starting at step 1
    app = fs.FletEasy(route_init="/register/step1")

    # Register all steps with share_data=True
    app.add_routes([
        fs.Pagesy(
            "/register/step1",
            step1_view,
            title="Registration - Personal Info",
            share_data=True,  # Enable data sharing
        ),
        fs.Pagesy(
            "/register/step2",
            step2_view,
            title="Registration - Address",
            share_data=True,  # Enable data sharing
        ),
        fs.Pagesy(
            "/register/step3",
            step3_view,
            title="Registration - Confirmation",
            share_data=True,  # Enable data sharing
        ),
    ])

    # Start the application
    app.start(page)


# Run the app
ft.app(target=main)
```

#### Demo

<video controls>
  <source src="../../../assets/guide/core/Pagesy-Data_sharing.webm" type="video/webm" alt="flet-easy - pagesy data sharing">
</video>

---

The `Pagesy` class provides the foundation for creating sophisticated, secure, and user-friendly page routing in Flet-Easy applications. Use these features to build robust navigation systems that enhance your application's functionality and user experience.

# Migration Guide: v0.2.x to v0.3.0

This guide helps you migrate your Flet-Easy applications from version 0.2.x to 0.3.0, taking advantage of new features while maintaining compatibility.

## What's New in v0.3.0

* 🆕 **Navigation Bar Integration**: Built-in support for `ft.NavigationBar`
* 🆕 **Page Caching System**: Optional state preservation during navigation
* 🆕 **Dynamic Controls**: Real-time updates for cached pages
* 🆕 **Enhanced Middleware**: Class-based middleware with before/after hooks
* 🆕 **Direct Method Execution**: Simplified API for common operations
* 🆕 **Python 3.9 Support**: Extended compatibility
* ⚡ **Performance Improvements**: Optimized routing and middleware execution
* 🆕 **`decode_jwt` / `decode_jwt_async`** methods added to `Datasy`, replacing the standalone `fs.decode()` / `fs.decode_async()` functions.
* ⚠️ **`fs.decode` and `fs.decode_async` are deprecated** — they still work but emit a `FutureWarning` and will be removed in a future version.

## Breaking Changes

### Method Execution Changes

**Before (v0.2.x):**

```python
# These methods returned lambda functions
button = ft.ElevatedButton("Back", on_click=data.go_back())
button = ft.ElevatedButton("Logout", on_click=data.logout("token"))
```

**After (v0.3.0):**

```python
# These methods now execute directly - wrap in lambda for event handlers
button = ft.ElevatedButton("Back", on_click=lambda _: data.go_back())
button = ft.ElevatedButton("Logout", on_click=lambda _: data.logout("token"))

# Or use the new direct methods in functions
def handle_back(_):
    data.go_back()  # Executes immediately

def handle_logout(_):
    data.logout("token")  # Executes immediately
```

### New Direct Navigation Method

**New in v0.3.0:**

```python
# Direct navigation - executes immediately
def some_function():
    data.go_route("/dashboard")  # New method

# Traditional method still works
button = ft.ElevatedButton("Dashboard", on_click=data.go("/dashboard"))
```

## New Features Migration

### Navigation Bar Integration

**Before (Manual Implementation):**

```python
@app.page("/home")
def home_page(data: fs.Datasy):
    def on_nav_change(e):
        selected = e.control.selected_index
        if selected == 0:
            data.go("/home")
        elif selected == 1:
            data.go("/search")
        elif selected == 2:
            data.go("/profile")
    
    return ft.View(
        controls=[...],
        navigation_bar=ft.NavigationBar(
            selected_index=0,  # Manual management
            on_change=on_nav_change,
            destinations=[...]
        )
    )
```

**After (v0.3.0 - Automatic):**

```python
# Define pages with index parameters
@app.page("/home", index=0)
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[...],
        navigation_bar=data.view.navigation_bar  # From global view
    )

@app.page("/search", index=1)
def search_page(data: fs.Datasy):
    return ft.View(
        controls=[...],
        navigation_bar=data.view.navigation_bar
    )

# Configure global navigation bar
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        navigation_bar=ft.NavigationBar(
            destinations=[...],
            on_change=data.go_navigation_bar  # Automatic handling
        )
    )
```

### Page Caching

**New Feature - Add to Existing Pages:**

```python
# Enable caching for form pages
@app.page("/user-form", cache=True)  # Add cache parameter
def user_form_page(data: fs.Datasy):
    # Form fields will retain values when navigating away and back
    return ft.View(controls=[...])

# Disable caching for real-time data pages
@app.page("/live-feed", cache=False)  # Explicit disable (default)
def live_feed_page(data: fs.Datasy):
    # Page resets on each visit
    return ft.View(controls=[...])
```

### Dynamic Controls

**New Feature for Cached Pages:**

```python
@app.page("/dashboard", cache=True)
def dashboard_page(data: fs.Datasy):
    # Update controls dynamically without losing page state
    def update_title(appbar):
        appbar.title = ft.Text(f"Dashboard - {datetime.now().strftime('%H:%M')}")
        data.page.update()
    
    # Register dynamic control
    data.dynamic_control(data.view.appbar, update_title)
    
    return ft.View(controls=[...])
```

### Enhanced Middleware

**Before (Function-based):**

```python
def auth_middleware(data: fs.Datasy):
    if data.route == "/login":
        return
    
    token = data.page.client_storage.get("auth_token")
    if not token:
        return data.redirect("/login")

app.add_middleware([auth_middleware])
```

**After (Class-based - Recommended):**

```python
class AuthMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        if self.data.route == "/login":
            return
        
        token = self.data.page.client_storage.get("auth_token")
        if not token:
            return fs.Redirect("/login")
    
    def after_request(self):
        # New: Execute after page loads
        print(f"User accessed: {self.data.route}")

# Both function and class-based middleware work
app.add_middleware(AuthMiddleware)
```

### Page-Specific Middleware

**New Feature:**

```python
class AdminMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        user_role = self.data.page.client_storage.get("user_role")
        if user_role != "admin":
            return fs.Redirect("/unauthorized")

# Apply middleware to specific pages
admin_pages = fs.AddPagesy([
    fs.Pagesy("/admin/dashboard", admin_view, middleware=[AdminMiddleware]),
    fs.Pagesy("/admin/users", users_view, middleware=[AdminMiddleware]),
])

app.add_pages(admin_pages)
```

## Step-by-Step Migration

### Update Dependencies

```bash
# Upgrade to v0.3.0
pip install flet-easy>=0.3.0 --upgrade

# Or install with all features
pip install flet-easy[all]>=0.3.0 --upgrade
```

### Fix Method Calls

Search and replace in your codebase:

```python
# Find patterns like these and wrap in lambda:
on_click=data.go_back()          → on_click=lambda _: data.go_back()
on_click=data.logout("token")    → on_click=lambda _: data.logout("token")

# Or refactor to use functions:
def handle_back(_):
    data.go_back()

on_click=handle_back
```

### Add Navigation Indices (Optional)

```python
# Add index parameters to pages that should appear in NavigationBar
@app.page("/home", index=0)      # Add index=0
@app.page("/search", index=1)    # Add index=1
@app.page("/profile", index=2)   # Add index=2
```

### Enable Caching (Optional)

```python
# Add caching to form pages
@app.page("/form", cache=True)   # Add cache=True

# Explicitly disable for real-time pages
@app.page("/live", cache=False)  # Add cache=False
```

### Upgrade Middleware (Optional)

```python
# Convert function-based middleware to class-based
class MyMiddleware(fs.MiddlewareRequest):
    def before_request(self):
        # Your existing middleware logic here
        pass

    def after_request(self):
        # New: Add post-processing logic
        pass

app.add_middleware(MyMiddleware)
```

### Migrate JWT Decoding (v0.3.0+)

Replace the deprecated standalone functions with the new `Datasy` methods:

```python
# Before (deprecated — emits FutureWarning)
@app.login
def login_required(data: fs.Datasy):
    return fs.decode(key_login="login", data=data)

@app.login
async def login_required(data: fs.Datasy):
    return await fs.decode_async(key_login="login", data=data)

# After (v0.3.0+)
@app.login
def login_required(data: fs.Datasy) -> bool:
    return data.decode_jwt(key_login="login")

@app.login
async def login_required(data: fs.Datasy) -> bool:
    return await data.decode_jwt_async(key_login="login")
```

## Compatibility Notes

* **Backward Compatibility**: All v0.2.x code continues to work
* **Function-based Middleware**: Still supported alongside class-based
* **Traditional Navigation**: `data.go()` method unchanged
* **Existing Parameters**: All previous `Pagesy` parameters remain valid

## Testing Your Migration

1. **Run Your App**: Ensure basic functionality works
2. **Test Navigation**: Verify all page transitions work correctly
3. **Check Event Handlers**: Ensure buttons and interactions work
4. **Validate Middleware**: Confirm authentication and routing logic
5. **Test Caching**: If enabled, verify state preservation works as expected

## Common Issues and Solutions

### Issue: Button clicks not working

**Problem**: Using old method syntax

```python
# Wrong (v0.3.0)
on_click=data.go_back()
```

**Solution**: Wrap in lambda

```python
# Correct (v0.3.0)
on_click=lambda _: data.go_back()
```

### Issue: Navigation bar not updating

**Problem**: Missing index parameters

**Solution**: Add index to page decorators

```python
@app.page("/home", index=0)  # Add index
```

### Issue: Form data not persisting

**Problem**: Caching not enabled

**Solution**: Add cache parameter

```python
@app.page("/form", cache=True)  # Enable caching
```

### Issue: `FutureWarning` about `fs.decode` or `fs.decode_async`

**Problem**: Using the deprecated standalone functions.

```python
# Deprecated
value = fs.decode(key_login="login", data=data)
```

**Solution**: Use the `Datasy` methods instead.

```python
# Correct (v0.4.0+)
value = data.decode_jwt(key_login="login")           # sync
value = await data.decode_jwt_async(key_login="login")  # async
```

## Performance Benefits

After migration, you'll benefit from:

* **Faster Routing**: Optimized route loading and middleware execution
* **Better Memory Usage**: Improved caching system
* **Smoother Navigation**: Enhanced NavigationBar integration
* **Cleaner Code**: More intuitive API design

## Getting Help

* **Documentation**: Check the updated [API Reference](../api/reference.md)
* **Examples**: See [v0.3.0 Showcase](v0-3-0-showcase.md)
* **Issues**: Report problems on [GitHub Issues](https://github.com/Daxexs/flet-easy/issues)

Happy migrating! 🚀

# Page Caching System

!!! note "New in v0.3.0"

The page caching system in Flet-Easy v0.3.0 allows you to preserve page state when navigating between routes. This is particularly useful for applications where you want to maintain ongoing processes, form data, or UI state without interruption.

## Overview

When caching is enabled (`cache=True`), the page View is not reloaded when you return to it. All controls maintain their state, including:

- Form field values
- Running processes (counters, timers, etc.)
- Component state
- User interactions

## Key Features

- **State Preservation**: Controls retain their values and state
- **Process Continuity**: Background processes continue running
- **Performance Optimization**: Reduces re-rendering overhead
- **Seamless Navigation**: Smooth user experience across pages
- **Dynamic Updates**: Works with `dynamic_control()` for real-time updates

## Basic Usage

### Enabling Cache

```python hl_lines="7 27"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/form")

# Enable caching for this page
@app.page("/form", title="User Form", cache=True)
def form_page(data: fs.Datasy):
    # Form fields will retain their values
    name_field = ft.TextField(label="Name", value="", width=200)
    email_field = ft.TextField(label="Email", value="", width=200)

    return ft.View(
        controls=[
            ft.Text("User Form (Cached)", size=24),
            name_field,
            email_field,
            ft.ElevatedButton("Save", on_click=lambda _: print("Saved!")),
            ft.ElevatedButton("go to live feed", on_click=data.go("/live-feed")),
            ft.ElevatedButton("Reset", on_click=lambda _: data.page_reload())
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# Disable caching (default behavior)
@app.page("/live-feed", title="Live Feed")
def live_feed_page(data: fs.Datasy):
    # Page resets on each visit
    return ft.View(
        controls=[
            ft.Text("Live Feed (No Cache)", size=24),
            ft.Text("This page resets every time you visit it"),
            ft.ElevatedButton("go to form", on_click=data.go("/form")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()
```

### Demo

<video controls>
  <source src="../../assets/advanced/page-caching_basic-usage.webm" type="video/webm" alt="Flet-Easy - Page Caching - Basic Usage">
</video>

## Advanced Example: Counter with Caching

This example demonstrates how caching preserves running processes:

```python hl_lines="92 115 133"
import asyncio
import random
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/")

# Remove page transition animations for smoother experience
@app.config
def config(page: ft.Page):
    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.NONE,
            android=ft.PageTransitionTheme.NONE,
            ios=ft.PageTransitionTheme.NONE,
            macos=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
        ),
    )

# Global view with navigation
@app.view
def config_view(data: fs.Datasy):
    def change_color(e):
        colors = [ft.Colors.RED, ft.Colors.GREEN, ft.Colors.BLUE, ft.Colors.YELLOW]
        appbar.bgcolor = random.choice(colors)
        data.page.update()

    appbar = ft.AppBar(
        bgcolor=ft.Colors.BLACK45,
        actions=[
            ft.IconButton(
                icon=ft.Icons.RESTART_ALT_ROUNDED,
                icon_color=ft.Colors.WHITE,
                on_click=change_color,
                tooltip="Change Color"
            )
        ],
    )

    return fs.Viewsy(
        appbar=appbar,
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.CODE, label="Counter 1"),
                ft.NavigationBarDestination(icon=ft.Icons.SYNC_DISABLED, label="Counter 2"),
                ft.NavigationBarDestination(icon=ft.Icons.CODE, label="Counter 3"),
            ],
            on_change=data.go_navigation_bar,
        ),
    )

# Custom counter component
class Counter(ft.Container):
    def __init__(self, update_func, color: str):
        super().__init__()
        self.update_func = update_func
        self.is_running = False

        self.number = ft.TextField(value="0", text_size=50, text_align="center")
        self.start_button = ft.FilledButton("Start", on_click=self.toggle_counter, height=50)

        self.content = ft.Column([
            self.number,
            self.start_button,
        ], horizontal_alignment="center")

        self.width = 400
        self.bgcolor = color
        self.border_radius = 10
        self.padding = 20

    async def toggle_counter(self, e):
        if not self.is_running:
            self.is_running = True
            self.start_button.text = "Stop"
            self.start_button.bgcolor = ft.Colors.RED
            self.update_func()

            # Start counting
            while self.is_running:
                self.number.value = str(int(self.number.value) + 1)
                self.update_func()
                await asyncio.sleep(1)
        else:
            self.is_running = False
            self.start_button.text = "Start"
            self.start_button.bgcolor = None
            self.update_func()

# Cached page - counter continues running when you navigate away
@app.page("/", title="Counter 1", index=0, cache=True)
def counter1_page(data: fs.Datasy):
    appbar = data.view.appbar

    # Dynamic title update
    async def update_title(control):
        control.title = ft.Text("Counter 1 - Cached")

    data.dynamic_control(appbar, update_title)

    return ft.View(
        controls=[
            ft.Text("Counter 1 (Cached)", size=50),
            ft.Text("This counter keeps running when you navigate away!", size=16),
            Counter(data.page.update, ft.Colors.RED_500),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        horizontal_alignment="center",
        vertical_alignment="center",
    )

# Non-cached page - counter resets every time
@app.page("/counter2", title="Counter 2", index=1, cache=False)
def counter2_page(data: fs.Datasy):
    appbar = data.view.appbar
    appbar.title = ft.Text("Counter 2 - No Cache")

    return ft.View(
        controls=[
            ft.Text("Counter 2 (No Cache)", size=50),
            ft.Text("This counter resets every time you visit", size=16),
            Counter(data.page.update, ft.Colors.BLUE_500),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# Another cached page
@app.page("/counter3", title="Counter 3", index=2, cache=True)
def counter3_page(data: fs.Datasy):
    appbar = data.view.appbar

    # Lambda function for quick updates
    data.dynamic_control(
        appbar, 
        func_update=lambda e: setattr(e, "title", ft.Text("Counter 3 - Cached"))
    )

    return ft.View(
        controls=[
            ft.Text("Counter 3 (Cached)", size=50),
            ft.Text("Another cached counter for comparison", size=16),
            Counter(data.page.update, ft.Colors.GREEN_500),
        ],
        appbar=appbar,
        navigation_bar=data.view.navigation_bar,
        horizontal_alignment="center",
        vertical_alignment="center",
    )

app.run()
```

### Demo

<video controls>
  <source src="../../assets/advanced/page-caching-counter.webm" type="video/webm" alt="Flet-Easy - Page Caching - Counter">
</video>

## Working with Dynamic Controls

When using caching, you can update shared controls dynamically using `data.dynamic_control()`:

```python
@app.page("/dashboard", cache=True)
def dashboard_page(data: fs.Datasy):
    appbar = data.view.appbar
    
    # Update appbar title dynamically
    def update_title(control):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        control.title = ft.Text(f"Dashboard - {current_time}")
        data.page.update()
    
    # Register dynamic control
    data.dynamic_control(appbar, update_title)
    
    # Auto-update every 5 seconds
    async def auto_update():
        while True:
            await asyncio.sleep(5)
            update_title(appbar)
    
    # Start auto-update task
    data.page.run_task(auto_update)
    
    return ft.View(
        controls=[
            ft.Text("Dashboard with Live Updates", size=24),
            ft.ElevatedButton(
                "Manual Update", 
                on_click=lambda _: update_title(appbar)
            ),
            ft.ElevatedButton(
                "Reset Page", 
                on_click=lambda _: data.page_reload()
            )
        ],
        appbar=appbar
    )
```

## Best Practices

### When to Use Caching

**✅ Good Use Cases:**

- Forms with user input
- Pages with running processes (timers, counters)
- Complex UI state that's expensive to recreate
- Pages with ongoing data streams
- Multi-step workflows

**❌ Avoid Caching When:**

- Page content should always be fresh
- Real-time data that needs constant updates
- Simple static pages
- Pages with sensitive information

### Performance Considerations

```python
# Good: Use caching for complex forms
@app.page("/user-profile", cache=True)
def profile_page(data: fs.Datasy):
    # Complex form with many fields
    return ft.View(controls=[...])

# Good: No caching for simple pages
@app.page("/about", cache=False)  # Default
def about_page(data: fs.Datasy):
    # Simple static content
    return ft.View(controls=[ft.Text("About Us")])

# Good: Reset when needed
def reset_form(_):
    data.page_reload()  # Clears cache and resets page
```

### Memory Management

- Cached pages consume more memory
- Use `data.page_reload()` to clear cache when needed
- Consider the number of cached pages in your app
- Monitor memory usage in production

## Troubleshooting

### Common Issues

- **Problem**: Page doesn't update after navigation
- **Solution**: Use `data.dynamic_control()` for shared controls

---

- **Problem**: Memory usage increasing
- **Solution**: Limit cached pages and use `page_reload()` strategically

---

- **Problem**: Stale data in cached page
- **Solution**: Implement refresh mechanisms or disable caching

The page caching system in Flet-Easy v0.3.0 provides powerful state management capabilities while maintaining simplicity and performance. Use it strategically to create smooth, responsive applications that preserve user context across navigation.

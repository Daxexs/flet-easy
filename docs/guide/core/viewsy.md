# View System (Viewsy)

The `Viewsy` class provides a comprehensive view template system for Flet-Easy applications, allowing you to define consistent layouts, navigation elements, and responsive designs across your entire application.

## Overview

`Viewsy` enables you to:

- **Global Layout**: Define consistent app-wide layout templates
- **Navigation Components**: Configure app bars, drawers, and navigation bars
- **Responsive Design**: Create adaptive layouts for different screen sizes
- **Theme Management**: Apply consistent styling and theming
- **Component Reusability**: Share common UI elements across pages

## Class Definition

```python
class Viewsy(ft.View):
    def __init__(
        self,
        route: str = "/",
        controls: Optional[List[ft.Control]] = None,
        appbar: Optional[ft.AppBar] = None,
        drawer: Optional[ft.NavigationDrawer] = None,
        end_drawer: Optional[ft.NavigationDrawer] = None,
        floating_action_button: Optional[ft.FloatingActionButton] = None,
        navigation_bar: Optional[ft.NavigationBar] = None,
        bgcolor: Optional[str] = None,
        spacing: Optional[float] = None,
        padding: Optional[ft.Padding] = None,
        vertical_alignment: Optional[ft.MainAxisAlignment] = None,
        horizontal_alignment: Optional[ft.CrossAxisAlignment] = None,
        scroll: Optional[ft.ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        fullscreen_dialog: Optional[bool] = None,
        on_scroll_interval: Optional[int] = None,
        on_scroll: Optional[Callable] = None
    )
```

## Basic Usage

This example demonstrates how to create a **global view template** that applies consistent navigation and styling across all pages in your application.

### 🎯 What You'll Learn

- **Define a global view** using `@app.view` decorator
- **Create consistent navigation** with AppBar and NavigationDrawer
- **Reuse view components** across multiple pages
- **Access global view properties** via `data.view`

### 📋 How It Works

The `@app.view` decorator creates a **template** that defines common UI elements (AppBar, Drawer, background color, padding) that will be shared across all pages. Each page can then access these elements through `data.view`.

### 💡 Key Concepts

**`@app.view`**: Decorator that defines a global view template for the entire application.

**`data.view.appbar`**: Access the global AppBar defined in the view template.

**`data.view.drawer`**: Access the global NavigationDrawer defined in the view template.

**`data.view.bgcolor`**: Access the global background color.

**`data.view.padding`**: Access the global padding configuration.

```python
import flet as ft
import flet_easy as fs

# Create the application
app = fs.FletEasy()


# ========================================
# GLOBAL VIEW TEMPLATE
# ========================================
@app.view
def main_view(data: fs.Datasy):
    """
    Define a global view template that will be shared across all pages.
    This includes the AppBar, NavigationDrawer, background color, and padding.
    """
    return fs.Viewsy(
        # Global AppBar - appears on all pages
        appbar=ft.AppBar(
            title=ft.Text("My Application"),
            center_title=True,
            bgcolor=ft.Colors.BLUE,
            actions=[
                # Quick action button to navigate to profile
                ft.IconButton(
                    ft.Icons.SETTINGS,
                    on_click=data.go("/profile"),
                    tooltip="Go to Profile"
                ),
            ]
        ),
        
        # Global NavigationDrawer - side menu for navigation
        drawer=ft.NavigationDrawer(
            controls=[
                # Home navigation item
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text("Home"),
                    on_click=data.go("/")
                ),
                # Profile navigation item
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text("Profile"),
                    on_click=data.go("/profile")
                ),
            ]
        ),
        
        # Global background color
        bgcolor=ft.Colors.BLACK12,
        
        # Global padding for all pages
        padding=ft.padding.all(20)
    )


# ========================================
# HOME PAGE
# ========================================
@app.page("/")
def home_page(data: fs.Datasy):
    """
    Home page that uses the global view template.
    Notice how we access global elements via data.view
    """
    return ft.View(
        controls=[
            ft.Text("Welcome to the Home Page!", size=24, weight="bold"),
            ft.Text("This page uses the global view template", color="grey"),
            ft.Divider(height=20),
            ft.ElevatedButton(
                "Go to Profile →",
                on_click=data.go("/profile"),
                icon=ft.Icons.PERSON
            )
        ],
        # Reuse global view components
        appbar=data.view.appbar,      # Use global AppBar
        drawer=data.view.drawer,      # Use global NavigationDrawer
        bgcolor=data.view.bgcolor,    # Use global background color
        padding=data.view.padding     # Use global padding
    )


# ========================================
# PROFILE PAGE
# ========================================
@app.page("/profile")
def profile_page(data: fs.Datasy):
    """
    Profile page that also uses the global view template.
    All pages share the same AppBar, Drawer, and styling.
    """
    return ft.View(
        controls=[
            ft.Text("Welcome to the Profile Page!", size=24, weight="bold"),
            ft.Text("This page also uses the global view template", color="grey"),
            ft.Divider(height=20),
            
            # User profile card
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.BLUE),
                        ft.Text("User Profile", size=18),
                        ft.Text("Manage your account settings", size=12, color="grey"),
                    ], horizontal_alignment="center"),
                    padding=20,
                )
            ),
            
            ft.ElevatedButton(
                "← Back to Home",
                on_click=data.go("/"),
                icon=ft.Icons.HOME
            )
        ],
        # Reuse global view components
        appbar=data.view.appbar,      # Use global AppBar
        drawer=data.view.drawer,      # Use global NavigationDrawer
        bgcolor=data.view.bgcolor,    # Use global background color
        padding=data.view.padding     # Use global padding
    )


# Run the application
if __name__ == "__main__":
    app.run()
```

### ✨ Benefits of Using Viewsy

**1. Consistency**: All pages share the same navigation and styling automatically.

**2. DRY Principle**: Define common elements once, use everywhere (Don't Repeat Yourself).

**3. Easy Maintenance**: Update the global view in one place, changes apply to all pages.

**4. Flexibility**: Individual pages can still override or customize specific elements if needed.

## 🎬 Demo

<video controls>
  <source src="../../../assets/guide/core/Viewsy-Simple_Global_View.webm" type="video/mp4" alt="Flet-Easy - Viewsy Simple Global View">
</video>

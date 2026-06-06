# Flet-Easy Documentation

[![github](https://img.shields.io/badge/my_profile-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Daxexs)
[![pypi](https://img.shields.io/badge/Pypi-0A66C2?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/flet-easy)
[![Downloads](https://static.pepy.tech/badge/flet-easy)](https://pepy.tech/project/flet-easy) [![Socket Badge](https://badge.socket.dev/pypi/package/flet-easy?artifact_id=tar-gz)](https://socket.dev/pypi/package/flet-easy)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Flet 0.27+](https://img.shields.io/badge/Flet-0.27%2B-orange?logo=flutter&logoColor=white)

<div align="center">
    <img src="assets/images/logo.png" alt="logo" width="250">
</div>

**Flet-Easy** is a comprehensive Python framework that extends Flet with powerful features for building modern desktop, web, and mobile applications. It provides a clean, intuitive API with advanced routing, authentication, middleware, page caching, and responsive design capabilities — all with **zero breaking changes** when upgrading Flet versions.

!!! success "Broad Compatibility"
    - 🐍 **Python 3.9+** — works with any modern Python version
    - ⚡ **Flet 0.27+** — compatible across all Flet releases from `0.27.*` up to the latest `0.80+`
    - 🖥️ **All platforms** — Desktop (Windows, macOS, Linux), Web, and Mobile

!!! tip "Latest Release - v0.3.0 🎉"
    **New features**: NavigationBar integration, page caching system, enhanced middleware, declarative component routing, and multi-user concurrency safety. [See what's new →](changelog.md)

## Key Features

- **🛣️ Advanced Routing**: Dynamic routes, NavigationBar integration, regex-based parameter validation, and custom 404 pages
- **💾 Page Caching**: Optional per-page state preservation across navigation for seamless user experience
- **🔐 Built-in Authentication**: JWT support (HS256 / RS256 / RS512) with automatic session management
- **🔧 Enhanced Middleware**: Class-based and functional middleware with global and per-page application
- **🎭 Dual Rendering Modes**: Supports both **Declarative** (`@ft.component`) and **Imperative** routing seamlessly
- **🔒 Concurrency-Safe**: Session isolation via `contextvars` — no data leakage in multi-user async environments
- **🎛️ Dynamic Controls**: Real-time UI updates with `dynamic_control()` — works with cached pages
- **📱 Responsive Design**: `ResponsiveControlsy` and `on_resize` hooks for adaptive desktop/tablet/mobile layouts
- **⚡ High Performance**: O(1) exact route lookup, lazy-loaded components, and intelligent view caching
- **🎨 Sub-router Support**: Organize pages into independent modules with `AddPagesy` and route prefixes
- **🛠️ Developer Tools**: CLI (`fs init`) for project scaffolding, code generation, and app templates
- **🐍 Python 3.9+**: Uses modern Python generics and type hints out of the box
- **📦 Flet 0.27+ Compatible**: Tested from Flet `0.27.*` all the way to `0.80+` with automatic fallbacks
- **📚 Comprehensive Documentation**: Step-by-step guides, API reference, and practical examples

## Quick Start

### Installation

```bash
# Basic installation
pip install flet-easy

# Full installation with all features
pip install flet-easy[all] --upgrade
```

### Your First App

```python
import flet as ft
import flet_easy as fs

# 1. Initialize Flet-Easy
# We set the initial route to "/home"
app = fs.FletEasy(route_init="/home")

# 2. Define a Global View
# This layout (AppBar, NavigationBar, etc.) will be shared across pages
@app.view
def main_view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("My Flet-Easy App"),
            bgcolor=ft.Colors.BLUE,
        ),
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.INFO, label="About"),
            ],
            on_change=data.go_navigation_bar, # Handles automatic routing via index
        ),
        bgcolor=ft.Colors.GREY_50,
    )

# 3. Create the Home Page
@app.page("/home", title="Home", index=0) # index=0 matches the first Nav interface
def home_page(data: fs.Datasy):
    data.view.appbar.title = ft.Text("Welcome Home! 🏠")

    return ft.View(
        controls=[
            ft.Text("Welcome to Flet-Easy! 🎉", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Now with page caching and NavigationBar support!", size=16),
            ft.ElevatedButton(
                "Go to About",
                on_click=lambda _: data.go_route("/about"), # Direct navigation
            ),
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 4. Create the About Page
@app.page("/about", title="About", index=1)
def about_page(data: fs.Datasy):
    data.view.appbar.title = ft.Text("About Flet-Easy")

    return ft.View(
        controls=[
            ft.Text("About Flet-Easy", size=24),
            ft.Text("Build amazing apps with Python and new caching features!"),
            ft.ElevatedButton("← Back Home", on_click=lambda _: data.go_back()),
        ],
        appbar=data.view.appbar,
        navigation_bar=data.view.navigation_bar,
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 5. Run the Application
if __name__ == "__main__":
    app.run()
```

#### Demo

<video controls>
  <source src="assets/index.webm" type="video/webm" alt="index demo Flet-Easy">
</video>

## What's New in v0.3.0

### Major Features

- **NavigationBar Integration**: Built-in support for `ft.NavigationBar` with automatic routing
- **Page Caching System**: Optional state preservation to maintain UI state across navigation
- **Enhanced Middleware**: Class-based middleware with page-specific application support
- **Dynamic Controls**: Real-time UI updates with `dynamic_control()` method
- **Performance Improvements**: Optimized route loading and middleware execution

### New Methods

- `page_reload()` - Reset page to default state
- `dynamic_control()` - Real-time control updates
- `go_navigation_bar()` - Handle NavigationBar events
- `go_route()` - Direct route navigation

### ⚡ API Improvements

- `go_back()` and `logout()` now execute directly
- Enhanced `Pagesy` with `index` and `cache` parameters
- Python 3.9+ compatibility with modern built-in generics
- **Flet 0.27+ compatibility** — automatic fallbacks for older API surfaces
- **Concurrency-safe middleware** — `contextvars` isolation per async task
- **Strict type safety** — fully passes `ty check` with zero `# type: ignore` comments

[**→ View complete changelog**](changelog.md)

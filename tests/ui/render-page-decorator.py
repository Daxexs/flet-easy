import asyncio
from dataclasses import dataclass

import flet as ft

import flet_easy as fs

"""
Test render page demonstrating Flet-Easy features (v0.3.0+) including the use of decorators,
native Flet components, reactive state management, and hierarchical routing.

Key Flet-Easy concepts demonstrated:
- `fs.FletEasy`: The main application class with decorator-based routing.
- `fs.Datasy`: The core data object injected into views, containing page info, routing, etc.
- `fs.MiddlewareRequest`: Base class for creating complex middlewares (before/after requests).
- `fs.AddPagesy`: Class for modular routing and hierarchical route organization.

Routing & View Capabilities (v0.3.0 Improvements):
1. **Decorator-based Routing**: Using `@app.page()` for easy route registration.
2. **Native Flet Components**: Perfect integration with `@ft.component`.
3. **Reactive State**: Demonstration of `ft.observable` and `ft.use_state`.
4. **Hierarchical Routing**: Using `AddPagesy` to group routes under a common prefix.
5. **Contextual Navigation**: Using `ft.context.page.push_route()` and `data.go()`.
"""

""" NOTE: v0.3.0
- Return ft.View is recommended
- Return ft.Text is supported
- Return list of controls is supported
- Return string is supported
- Return class is supported
- Return ft.Component is supported
- Parameter data: fs.Datasy is optional in all cases
 """

# create app
app = fs.FletEasy(logger=True)


@dataclass
@ft.observable
class CounterState:
    """Reactive state for the counter component."""

    count: int = 0

    def add(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def remove(self):
        self.count -= 1


# Counter Component: A native Flet declarative component.
@ft.component
def counter():
    state, _ = ft.use_state(CounterState())

    return ft.Column(
        controls=[
            ft.Text(value=f"{state.count}", size=30),
            ft.Row(
                controls=[
                    ft.Button("Remove", on_click=state.remove),
                    ft.Button("Add", on_click=state.add),
                    ft.Button("Reset", on_click=state.reset),
                ],
                alignment="center",
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )


# Middleware 1: Global Class-based Middleware.
# Inherits from `fs.MiddlewareRequest` to handle lifecycle hooks globally.
class MiddlewareRoutes(fs.MiddlewareRequest):
    def before_request(self):
        print(f"Middleware Global Routes - route: {self.data.route} - before home")

    def after_request(self):
        print(f"Middleware Global Routes - route: {self.data.route} - after home")


# Register global middleware to the application.
app.add_middleware(MiddlewareRoutes)


# Middleware 2: Functional Page-specific Middleware.
def middleware_home(data: fs.Datasy):
    data.page.show_dialog(
        ft.SnackBar(ft.Text(f"Middleware Home - route: {data.route} - Hello from middleware!"))
    )


# Page 1: Home - Using @ft.component and @app.page decorators.
# Demonstrates state caching and page-specific middleware.
@ft.component
@app.page(route="/", title="Home", middleware=middleware_home, cache=True)
def home_page(data: fs.Datasy):

    async def go_test():
        # Alternative navigation using Flet context
        await ft.context.page.push_route("/test")

    return ft.View(
        controls=[
            counter(),
            ft.Button("go test", on_click=go_test),
            ft.Button("go progress-bar", on_click=data.go("/add-pagesy/progress-bar")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# Page 2: Test - Simple imperative view registered with @app.page.
@app.page(route="/test", title="test")
class TestPage:
    def build(self):
        return ft.View(
            controls=[
                ft.Text("test"),
                ft.Button("go back", on_click=self.data.go("/")),
                ft.Button("go progress-bar", on_click=self.data.go("/add-pagesy/progress-bar")),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )


# ------------------------------ Modular Hierarchical Routing ------------------------------

# Create a sub-router using `fs.AddPagesy` to group related routes.
app2 = fs.AddPagesy(
    route_prefix="/add-pagesy",
    middleware=middleware_home,  # Middleware applied to all routes in this sub-router.
)


@dataclass
@ft.observable
class AppState:
    """Reactive state for the progress bar component."""

    counter: float

    async def start_counter(self):
        self.counter = 0
        for _ in range(0, 10):
            self.counter += 0.1
            await asyncio.sleep(0.5)


# Page 1 (Sub-router): Progress Bar 1 - Declarative component in a sub-router.


@app2.page(route="/progress-bar", title="progress-bar")
class ProgressBarPage:
    @ft.component
    def build(self):
        state, _ = ft.use_state(AppState(counter=0))

        async def go_back():
            await ft.context.page.push_route("/")

        return ft.View(
            controls=[
                ft.ProgressBar(state.counter),
                ft.Button("Run!", on_click=state.start_counter),
                ft.Button("go progress-bar2", on_click=self.data.go("/add-pagesy/progress-bar2")),
                ft.Button("go back", on_click=go_back),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )


# Middleware 3: Alert Middleware for specific pages in sub-router.


class MiddlewareAlert(fs.MiddlewareRequest):
    def before_request(self):
        self.data.page.show_dialog(
            ft.AlertDialog(
                ft.Text(f"Middleware Alert - route: {self.data.route} - Hello from middleware!"),
                modal=True,
                actions=[
                    ft.Button("Close", on_click=lambda e: self.data.page.pop_dialog()),
                ],
            )
        )


# Page 2 (Sub-router): Progress Bar 2 - Testing nested path and additional middleware.
@app2.page(route="/progress-bar2", title="progress-bar2", middleware=MiddlewareAlert)
def progress_bar2(data: fs.Datasy):

    return ft.Row(
        controls=[
            ft.Text("progress-bar2"),
            ft.Button("go back", on_click=lambda e: data.go_back()),
        ],
        vertical_alignment="center",
        alignment="center",
        expand=True,
    )


# Mount the sub-router to the main application.
app.add_pages([app2])

# Start the application session.
if __name__ == "__main__":
    app.run()

# Declarative Routing and Error Handling

Welcome to the beginner's guide to **Declarative Mode** in Flet-Easy!

If you come from React, Flutter, or simply prefer a style where "the UI reacts to the data," you will love this mode. We have designed this section to be **visual, intuitive, and straight to the point**.

---

## What is Declarative Mode?

In traditional Flet (Imperative Mode), you manually add controls to the page with `page.add()`. You build the interface block by block.

In **Declarative Mode**, you create **Components** (`@ft.component`). Instead of telling the page *how* to build the UI step by step, you define *what* should be shown depending on the state (the data) at any given time. Flet takes care of updating only what changes. It's magic!

!!! danger "Do not mix with Imperative Mode!"
    Flet-Easy supports both routing styles, but **you must choose one for your entire application**. If you use `@ft.component` on **any** page, the entire app switches to Flet's `render_views()` engine. This permanently freezes all controls upon rendering, which breaks any pages trying to use classic imperative updates (`control.value = X; page.update()`) with a fatal `RuntimeError: Frozen controls cannot be updated.` error. **Pick one style and stick with it!**

---

## Building our first Component

To use interactive components in Flet-Easy, we use the `@ft.component` decorator.

### 1. Basic Counter (Example)

Notice how we use `ft.use_state` to manage the state of our reactive component.

```python hl_lines="7 11 14"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/")

# 1. We declare that it's a component using the flet decorator!
@ft.component
@app.page(route="/", title="My First Component")
def my_component(data: fs.Datasy):
    # 2. We initialize the state (counter = 0)
    counter, set_counter = ft.use_state(0)

    # 3. We return a list of controls (Flet-Easy wraps it in an ft.View automatically)
    return [
        ft.Text(
            "Hello, Declarative Mode 👋",
            size=30, 
            weight="bold"
        ),
        ft.Text(
            f"You have clicked {counter} times", 
            size=20
        ),
        ft.ElevatedButton(
            "Magic Double Click!", 
            # 4. Upon clicking, we update the state. The UI updates itself!
            on_click=lambda e: set_counter(counter + 2)
        )
    ]

app.run()
```

!!! tip "List or `ft.View`"
    Flet-Easy is smart. You can return a simple list of controls `[ft.Text("Hello")]` and Flet-Easy will wrap them inside an `ft.View` by default. If you need to customize the view (for example, adding an AppBar or changing the background color of the entire page), you can return an `ft.View` directly. Flet-Easy will handle it seamlessly.

---

## The "Anti-White Screen Shield" (Error Boundary)

Have you ever misspelled a property in Flet, such as writing `alignment` instead of `vertical_alignment` inside an `ft.View`?

In previous versions (or in raw Flet components), this caused the application to "freeze" on a white screen or infinite loading screen, without telling you what the problem was.

**Flet-Easy to the rescue!** We have introduced our own **Error Boundary** system (Visual error catching).

### How does it work?

If you make an error inside your declarative component, instead of crashing or going blank, Flet-Easy will **intercept the error** and show you a visual screen directly in your application, telling you exactly what went wrong.

### Typical Error Example

```python hl_lines="10"
@ft.component
@app.page(route="/profile", title="User Profile")
def user_profile(data: fs.Datasy):
    
    return ft.Text("Hello", alingment="center")
```

**Result on Screen:**

In your application you will see a detailed error screen like this:

!!! failure "Error in Page '/profile'"
    ```python traceback
    Flet-Easy Rendering Error [/profile]

    Traceback (most recent call last):
      File "C:\Users\dxs\Desktop\flet-easy\src\flet_easy\core\router\_declarative.py", line 83, in _page_component
        result = raw_func(data, **url_params) if _has_params else raw_func()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\dxs\Desktop\flet-easy\verify_error_boundary.py", line 18, in error_page
        return ft.View(
               ^^^^^^^
            controls=[
            ^^^^^^^^^^
        ...<2 lines>...
            alignment=ft.MainAxisAlignment.CENTER, # TYPO: should be vertical_alignment
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    TypeError: View.__init__() got an unexpected keyword argument 'alignment'
    ```

!!! success "Quick Diagnosis"
    Thanks to this visual screen, you can quickly identify that you used the wrong property, go to your code, change `alignment` to `vertical_alignment`, reload the app and keep working without stress!

### Disabling the Error Boundary in Production

While the visual error screen is fantastic for development, displaying raw code tracebacks to end-users in a production environment is a security risk.

You can easily disable the visual Error Boundary by setting `use_error_boundary=False` when initializing `FletEasy`. **This works for both Imperative and Declarative modes!**

```python hl_lines="4"
import flet_easy as fs

app = fs.FletEasy(
    route_init="/", 
    use_error_boundary=False  # Hides tracebacks in the UI
)
```

If a routing error occurs while `use_error_boundary` is `False`:

- The application will show a safe, generic "An internal error occurred" message to the user.
- Flet-Easy will still print the full traceback to your terminal so you can fix it behind the scenes!

---

## Total Flexibility: Returns and Decorators (v0.3.0+)

One of the great advantages of Declarative Mode in Flet-Easy is its **total flexibility** when defining your pages. You can combine `@ft.component` with `@app.page` in various ways and return almost anything!

### The Power of the `return`

Flet-Easy adapts to your needs. Depending on the complexity of your page, you can choose the most convenient type of `return`. The parameter `data: fs.Datasy` is completely **optional** in all cases!

Here is what you can return from your declarative component:

- **`ft.View`** (Recommended for full pages, gives you complete control over background, appbar, etc.)
- **`list` of controls** (Perfect for quick prototyping; Flet-Easy automatically wraps it in an `ft.View`)
- **`ft.Component`** (You can return other declarative components directly)
- **Classes** (If you prefer object-oriented structuring)
- **`ft.Text`** or single controls (For extremely simple pages)
- **`str` (string)** (Flet-Easy will magically convert it into a Text control for you!)

### Complete Example in Action

Declarative mode doesn't limit you. **All the functionalities of Imperative Mode** are still at your disposal! This includes Middlewares, sub-routes (`fs.AddPagesy`), contextual navigation, and more.

Let's see a complete example combining native Flet components, reactive state (`ft.observable`), middlewares, and hierarchical routing (`fs.AddPagesy`):

```python
import flet as ft
import flet_easy as fs
from dataclasses import dataclass

app = fs.FletEasy(route_init="/")

# 1. We create our reactive state
@dataclass
@ft.observable
class CounterState:
    count: int = 0

    def add(self):
        self.count += 1

    def remove(self):
        self.count -= 1

# 2. A reusable native Flet declarative component
@ft.component
def counter():
    state, _ = ft.use_state(CounterState())
    return ft.Column(
        [
            ft.Text(
                f"Counter: {state.count}", 
                size=30, 
                weight="bold", 
                color="blue",
            ),
            ft.Row(
                [
                    ft.Button("Remove -", on_click=state.remove),
                    ft.Button("Add +", on_click=state.add),
                ],
                alignment="center",
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )

# 3. Middlewares work seamlessly!
def my_middleware(data: fs.Datasy):
    print(f"Navigating to: {data.route}")

# 4. Main Page with Middleware
@ft.component
@app.page(route="/", title="Flexibility Demo", middleware=my_middleware)
def home_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text(
                "Welcome to Flexible Routing 🚀", 
                size=35,
            ),
            counter(),
            ft.TextButton(
                "Go to Settings", 
                on_click=data.go("/settings")
            ),
            ft.TextButton(
                "Go to Sub-route", 
                on_click=data.go("/dashboard/stats")
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

# 5. Sub-routes (fs.AddPagesy) work perfectly too!
dashboard_app = fs.AddPagesy(route_prefix="/dashboard")

@ft.component
@dashboard_app.page(route="/stats", title="Dashboard Stats")
def stats_page(data: fs.Datasy):
    # Declarative functionality: using use_state
    likes, set_likes = ft.use_state(0)

    return ft.View(
        controls=[
            ft.Text(
                "Dashboard Stats 📊", 
                size=30
            ),
            ft.Text(
                f"Likes: {likes}", 
                size=20
            ),
            ft.Button(
                "Like 👍", 
                on_click=lambda _: set_likes(likes + 1)
            ),
            ft.Button(
                "Go Back", 
                on_click=lambda _: data.go_back(),
            ),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.add_pages([dashboard_app])

# 6. Another page using a class!
@app.page(route="/settings", title="Settings")
class SettingsPage:
    def build(self):
        return ft.Column(
            [
                ft.Text("This is the Settings Page built with a simple String!"),
                ft.TextButton(
                    "Go Back",
                    on_click=lambda _: self.data.go_back()
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
        )

if __name__ == "__main__":
    app.run()
```

!!! info "Optional `data` parameter"
    Notice how in `home_page` we used `data: fs.Datasy`, but in `SettingsPage` we didn't need it. Flet-Easy intelligently injects `data` only if you ask for it in your function signature!

!!! warning "Frozen Controls: Do Not Mutate State Imperatively"
    Because Flet-Easy unifies the rendering engine to support mixed routing seamlessly, **all pages are internally wrapped and processed as components**. As a result, Flet "freezes" all returned controls.
    **Never** try to mutate a control's property directly (e.g., `counter.value = 1` then `page.update()`). If you need local interactivity in a page (like a counter or input field), you **must** use declarative hooks like `@ft.component` and `ft.use_state`.

!!! warning "Cache is not supported in Declarative Mode"
    The `cache=True` parameter in the `@app.page` decorator **does not work** when you use Declarative Mode (`@ft.component`). Flet's declarative component lifecycle handles its own rendering and state, which is fundamentally incompatible with the static page caching mechanism.

---

## Summary for Happy Developers

1. Use `@ft.component` along with `@app.page(...)` to create reactive pages.
2. All Flet declarative functionalities are fully compatible: handle reactive variables with `ft.use_state()`, side effects with `ft.use_effect()`, context with `ft.use_context()`, and others like `ft.use_reducer()` or `ft.use_callback()`.
3. Return a `list` of controls for something quick, or an `ft.View` for highly customized pages.
4. If you make a mistake typing a property, don't panic. The **Error Supervisor** will block the crash and show you the error on the screen.

Happy declarative coding!

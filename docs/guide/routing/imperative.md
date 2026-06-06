# Imperative Routing

Welcome to the guide to **Imperative Mode** in Flet-Easy!

If you are already familiar with the standard way of working with Flet (using `page.views` and returning instances of `ft.View`), this mode will feel right at home. Flet-Easy simplifies imperative routing by handling the view stack, navigation history, and URL parameters for you.

---

## What is Imperative Mode?

In **Imperative Mode**, you are responsible for defining the full UI structure by returning a complete `ft.View` or a list of controls. Every time the user navigates to a route, Flet-Easy executes your page function, takes the result, and manually appends it to Flet's internal `page.views` list.

Unlike Declarative Mode (which reacts to state changes dynamically), Imperative Mode builds the screen from top to bottom every time a route changes.

---

## Building an Imperative Page

Creating an imperative page is incredibly straightforward. You use the `@app.page()` decorator, and your function simply returns the UI.

### Basic Example

```python hl_lines="10 16"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/")

# 1. We define the page using @app.page (No @ft.component needed!)
@app.page(route="/", title="Imperative Home")
def home_page(data: fs.Datasy):
    
    # 2. We can return an ft.View directly
    return ft.View(
        route="/",
        controls=[
            ft.Text("Hello, Imperative Mode 🚀", size=30, weight="bold"),
            ft.ElevatedButton(
                "Go to About", 
                on_click=data.go("/about") # Navigation is still easy!
            )
        ]
    )

@app.page(route="/about", title="About Us")
def about_page(data: fs.Datasy):
    # 3. Or we can just return a list of controls (Flet-Easy wraps it in a View)
    return [
        ft.Text("This is the About Page", size=25),
        ft.ElevatedButton("Go Back", on_click=data.go("/"))
    ]

app.run()
```

!!! tip "Total Flexibility"
    Just like in Declarative Mode, you don't *have* to return an `ft.View`. If you return a simple `list` of controls or even a single `ft.Text()`, Flet-Easy will intelligently wrap them in an `ft.View` so Flet's router can digest it without crashing.

---

## The Error Boundary (Visual Error Catching)

Did you think the "Anti-White Screen Shield" was only for Declarative components? **Think again!**

Flet-Easy fully protects your imperative pages too. If you make a typo in a property (for example, using `text_alignx` instead of `text_align`), Flet-Easy will intercept the crash before it breaks your app.

### See it in action

```python hl_lines="6"
@app.page(route="/broken", title="Broken Page")
def broken_page(data: fs.Datasy):
    
    return [
        # TYPO: 'text_alignx' does not exist!
        ft.Text("This will crash", text_alignx="center") 
    ]
```

Instead of a blank screen, Flet-Easy catches the `TypeError` during the view building phase and displays the beautiful **Visual Error Boundary**:

!!! failure "Error in Page '/broken'"
    ```python traceback
    TypeError: Text.__init__() got an unexpected keyword argument 'text_alignx'
    ```

!!! warning "Production Security Risk"
    Just like with Declarative Mode, **never leave the Error Boundary exposed in production**. Make sure to set `use_error_boundary=False` in `fs.FletEasy()` before deploying your app to avoid showing sensitive stack traces to your users!

---

## State Management in Imperative Mode

Since we don't have `@ft.component` or `ft.use_state()` here, state management relies on the classic Flet approach: updating control properties and calling `page.update()`.

### Example: The Classic Counter

```python hl_lines="10 12-16 18 23"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/counter")

@app.page(route="/counter", title="Classic Counter")
def counter_page(data: fs.Datasy):

    # 1. Define the control
    txt_number = ft.Text("0", size=40)

    def add_click(e):
        # 2. Update the property manually
        txt_number.value = str(int(txt_number.value) + 1)
        # 3. Tell Flet to update the screen
        data.page.update()

    return [
        ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.ADD,
                    on_click=add_click,
                ),
                txt_number,
            ],
            alignment="center",
            expand=True,
        )
    ]

app.run()
```

---

## Declarative vs Imperative: Which one should I use?

Flet-Easy supports both routing styles, but **you must choose one for your entire application**.

| Feature         | Imperative Mode                         | Declarative Mode (`@ft.component`)                |
|-----------------|-----------------------------------------|---------------------------------------------------|
| **Syntax**      | Classic Flet (`page.update()` )         | Modern, React-like (`ft.use_state`)               |
| **Updates**     | Manual. You update specific controls.   | Automatic. The UI reacts to data changes.         |
| **Complexity**  | Easier for small, static pages.         | Better for complex, dynamic interfaces.           |
| **Performance** | Excellent (No state diffing overhead).  | Very Good (Flet handles the diffing efficiently). |

!!! danger "Do not mix Imperative and Declarative modes!"
    If you use the `@ft.component` decorator on **any** page in your app, Flet-Easy automatically switches the entire application's rendering engine to Declarative Mode (which uses Flet's `page.render_views()`).

    When `page.render_views()` is active, **all controls become frozen** after they are rendered. If you try to manually mutate a control's property (e.g. `txt_number.value += 1`) and call `page.update()` in an imperative page, Flet will throw a fatal error: `RuntimeError: Frozen controls cannot be updated.`

    Therefore, **do not mix them**. If your app has declarative components, use `@ft.component` and `ft.use_state` for all dynamic pages. If your app is imperative, do not use `@ft.component` anywhere.

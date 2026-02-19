# ResponsiveControlsy

`ResponsiveControlsy` is a component that wraps a Flet control to make it responsive to size changes. It uses a `Canvas` internally to listen for resize events, allowing you to dynamically adjust the content or layout based on the available width and height.

This is particularly useful for creating adaptive layouts (e.g., switching between mobile and desktop views) or for visualizing the exact dimensions of a container during development.

!!! note
    - **Web compatibility:** While functional, it is generally not recommended for web applications if native CSS responsiveness can be used, due to potential performance overhead or layout differences.
    - **Scroll behavior:** Avoid enabling scroll on the immediate parent of `ResponsiveControlsy`. The component needs to expand to fill the available space to correctly detect resize events. If the parent scrolls, the component might not receive the correct size updates.

## Parameters

* `content` (Control): The child Flet control that you want to display and make responsive.

---

* `expand` (int | bool): Specifies how the control should fill the available space. It is crucial to set this (e.g., `expand=1` or `expand=True`) so that the `Canvas` fills the parent container. If it doesn't fill the space, resize events may not trigger as expected.

---

* `resize_interval` (int, optional): The minimum time interval (in milliseconds) between resize events. defaults to 1. Increasing this can help performance by reducing the frequency of event callbacks during rapid resizing.

---

* `on_resize` (callable, optional): A callback function triggered when the size changes. The function receives a `CanvasResizeEvent` object (containing `width` and `height`). Can be an asynchronous function (`async def`). If provided, `show_resize` behavior is overridden by this custom logic.

---

* `show_resize` (bool, optional): If `True`, overlays the current dimensions (Width x Height) on top of the content, useful for debugging layout issues. Automatically disabled if `on_resize` is provided.

---

* `show_resize_terminal` (bool, optional): If `True`, prints the dimensions (Width x Height) to the console/terminal whenever the size changes.

---

## Example

```python
import flet_easy as fs

fs.ResponsiveControlsy(
    content=ft.Container(
        content=ft.Text("on_resize"),
        bgcolor=ft.Colors.RED,
        alignment=ft.alignment.center,
        height=100
    ),
    expand=1,
    show_resize=True
)
```

## Basic use

```python hl_lines="13 23 33"
import flet as ft
import flet_easy as fs
from flet.canvas import CanvasResizeEvent

app = fs.FletEasy(route_init="/response")


@app.page(route="/response")
def response_page(data: fs.Datasy):
    page = data.page
    page.title = "Response"

    async def handle_resize(e: CanvasResizeEvent):
        # modify the content of the container to show the
        # width and height of the container
        c = e.control.content
        t = c.content
        t.value = f"Blue Container: {e.width} x {e.height}"
        page.update()

    return ft.View(
        controls=[
            fs.ResponsiveControlsy(
                content=ft.Container(
                    content=ft.Text("W x H"),
                    bgcolor=ft.Colors.RED,
                    alignment=ft.alignment.center,
                    height=100,
                ),
                expand=1,
                show_resize=True,
            ),
            fs.ResponsiveControlsy(
                ft.Container(
                    content=ft.Text("W x H"),
                    bgcolor=ft.Colors.BLUE,
                    alignment=ft.alignment.center
                ),
                on_resize=handle_resize, # modify the content
                expand=1,
            ),
        ],
    )


app.run()
```

## 🎬 **Demo**

<video controls>
  <source src="../../assets/advanced/responsiveControlsy.webm" type="video/webm" alt="ResponsiveControlsy">
</video>

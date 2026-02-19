# Examples Gallery

This gallery showcases practical examples of Flet-Easy applications, from simple demos to complex real-world scenarios.

## Basic Examples

### Hello World App

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy()


@app.page("/")
def home_page(data: fs.Datasy):
    page = data.page

    # add snack bar
    def add_snack_bar(e):
        page.open(ft.SnackBar(content=ft.Text("Hello World!"), open=True))

    return ft.View(
        controls=[
            ft.Text("Hello, Flet-Easy!", size=30),
            ft.ElevatedButton("Click me!", on_click=add_snack_bar),
        ]
    )


if __name__ == "__main__":
    app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/hello-world-app.webm" type="video/webm" alt="Flet-Easy - Hello World App">
</video>

### Counter App

```python
import flet as ft
import flet_easy as fs

app = fs.FletEasy()

# ==========================
# Reusable Components (OOP)
# ==========================
class Header(ft.Container):
    def __init__(self, title: str):
        super().__init__(
            content=ft.Text(
                title,
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(
                vertical=14,
                horizontal=16,
            ),
            border_radius=12,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[
                    ft.Colors.INDIGO_700,
                    ft.Colors.BLUE_700,
                ],
            ),
        )


class NavButton(ft.ElevatedButton):
    def __init__(self, text: str, color: str, on_click):
        super().__init__(
            text,
            on_click=on_click,
            width=140,
            height=48,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=24),
                elevation=6,
            ),
        )


class IconButtonPill(ft.ElevatedButton):
    def __init__(self, text: str, color: str, on_click):
        super().__init__(
            text,
            on_click=on_click,
            width=80,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=4,
            ),
        )


class InfoText(ft.Text):
    def __init__(self, value: str):
        super().__init__(
            value,
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        )


class CounterCard(ft.Container):
    def __init__(self, value: int = 0):
        self._label = ft.Text(
            str(value),
            size=70,
            weight=ft.FontWeight.BOLD,
        )
        super().__init__(
            content=self._label,
            alignment=ft.alignment.center,
            padding=ft.padding.all(24),
            border_radius=16,
            bgcolor=ft.Colors.with_opacity(
                opacity=0.10,
                color=ft.Colors.BLUE_200,
            ),
            border=ft.border.all(
                width=2,
                color=ft.Colors.BLUE_200,
            ),
        )
        self.set_value(value)

    def set_value(self, value: int):
        self._label.value = str(value)
        if value > 0:
            self._label.color = ft.Colors.TEAL_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.TEAL_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.TEAL_300,
            )
        elif value < 0:
            self._label.color = ft.Colors.RED_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.RED_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.RED_300,
            )
        else:
            self._label.color = ft.Colors.BLUE_900
            self.bgcolor = ft.Colors.with_opacity(
                opacity=0.12,
                color=ft.Colors.BLUE_200,
            )
            self.border = ft.border.all(
                width=2,
                color=ft.Colors.BLUE_300,
            )

# Demo: share_data=True allows data to persist between pages
@app.page("/", share_data=True)
def counter_page(data: fs.Datasy):
    count = data.share.get("count") or 0
    data.share.set("count", count)
    card = CounterCard(count)

    def increment(_):
        new_count = data.share.get("count") + 1
        data.share.set("count", new_count)
        card.set_value(new_count)
        card.update()
        data.page.update()

    def decrement(_):
        new_count = data.share.get("count") - 1
        data.share.set("count", new_count)
        card.set_value(new_count)
        card.update()
        data.page.update()

    return ft.View(
        controls=[
            Header("Counter Controls"),
            ft.Container(height=16),
            card,

            # Controls
            ft.Container(height=15),
            ft.Row([
                IconButtonPill("−", ft.Colors.RED_600, decrement),
                ft.Container(width=20),
                IconButtonPill("+", ft.Colors.TEAL_600, increment),
            ], alignment=ft.MainAxisAlignment.CENTER),

            # Navigation
            ft.Container(height=20),
            NavButton(
                text="View Value →",
                color=ft.Colors.INDIGO_700,
                on_click=data.go("/display"),
            ),

            # Info
            ft.Container(height=15),
            InfoText("💡 share_data=True: Counter persists between pages"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.GREY_100,
    )

# Demo: share_data=True allows accessing the same shared data
@app.page("/display", share_data=True)
def display_page(data: fs.Datasy):
    count = data.share.get("count") or 0

    # Components
    card = CounterCard(count)
    status = ft.Text(
        f"Status: {'↑ Positive' if count > 0 else '→ Zero' if count == 0 else '↓ Negative'}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREY_800,
        text_align=ft.TextAlign.CENTER,
    )

    return ft.View(
        controls=[
            Header("Shared Value"),
            ft.Container(height=16),
            card,
            ft.Container(height=12),
            status,
            ft.Container(height=20),
            NavButton(
                text="← Back to Controls",
                color=ft.Colors.AMBER_700,
                on_click=data.go("/"),
            ),
            ft.Container(height=12),
            InfoText("🔄 Same shared value from previous page"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.GREY_100,
    )

# Run the demo app
if __name__ == "__main__":
    app.run()
```

#### 🎬 Demo

<video controls>
  <source src="../../assets/examples/counter-app.webm" type="video/webm" alt="Flet-Easy - Counter App">
</video>

## More Examples

For additional examples and tutorials, visit:

- [GitHub Repository Examples](https://github.com/Daxexs/flet-easy/tree/main/tests)

Each example includes:

- Complete source code
- Step-by-step explanations
- Best practices
- Common pitfalls to avoid
- Extension ideas

Start with the basic examples and gradually work your way up to more complex applications as you become comfortable with Flet-Easy concepts.

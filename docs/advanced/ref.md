# Ref

Similar to [`Ref`](https://flet.dev/docs/cookbook/control-refs){:target="_blank"} of `Flet`, with the only difference being that to access the referenced control, use the property [`Ref.current`](https://flet.dev/docs/cookbook/control-refs){:target="_blank"} to `Ref.c`

!!! info
    It can be useful when we create components and we want to reference the controllers to be able to handle events in the component.

## Example

```python hl_lines="8-10 16-17 19"
import flet as ft
import flet_easy as fs

app = fs.FletEasy()

@app.page(route="/", title="Use fs.Ref")
def index_page(data: fs.Datasy):
    first_name = fs.Ref[ft.TextField]()
    last_name = fs.Ref[ft.TextField]()
    greetings = fs.Ref[ft.Column]()

    def btn_click(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
        )
        first_name.c.value = ""
        last_name.c.value = ""
        data.page.update()
        first_name.c.focus()

    return ft.View(
        controls=[
            ft.TextField(ref=first_name, label="First name", autofocus=True),
            ft.TextField(ref=last_name, label="Last name"),
            ft.ElevatedButton("Say hello!", on_click=btn_click),
            ft.Column(ref=greetings),
        ]
    )

app.run()
```

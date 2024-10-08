# General settings

This is achieved through the [`page`](https://flet.dev/docs/controls/page/) value provided by `Flet`. For this you have to use the `config` decorator of the `Flet-Easy` object.

Decorator to add a custom configuration to the app:

* The decorator function must receive a mandatory parameter, for example: [`page:ft.Page`](https://flet.dev/docs/controls/page/). Which can be used to make universal app configurations.
* The decorator function does not return anything.

## Example

!!! example ""
    In this example we change the page transitions

```python hl_lines="1 9"
@app.config
def config(page: ft.Page):
    theme = ft.Theme()
    platforms = ["android", "ios", "macos", "linux", "windows"]
    for platform in platforms:  # Removing animation on route change.
        setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)

    theme.text_theme = ft.TextTheme()
    page.theme = theme
```

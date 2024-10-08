# Page 404

Which will be activated when a page (path) is not found. [`page_404`](/flet-easy/0.1.0/how-to-use/#decorators) decorator to add a new custom page when not finding a route in the app, you need the following parameters :

## parameters

* `route`: text string of the url, for example ('/FletEasy-404'). (optional).
* `clear_page`: remove the pages from the `page.views` list of flet. (optional)
  
The decorated function must receive a mandatory parameter, for example: [`data:fs.Datasy`](/flet-easy/0.1.0/how-to-use/#datasy-data).

## Example

```python hl_lines="1"
@app.page_404("/FletEasy-404")
def page404(data: fs.Datasy):
    data.page.title = "Custom 404 error"

    return ft.View(
        controls=[
            ft.Text("Custom 404 error", size=30),
        ],
        vertical_alignment="center",
        horizontal_alignment="center"
    )
```

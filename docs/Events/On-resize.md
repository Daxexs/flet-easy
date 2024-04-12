In order to use this event, it is obtained from `data` of the function decorated by `page`.

### **1. Example**

```python hl_lines="6"
@app.page(route="/resize")
def resize_page(data:fs.Datasy):
    page = data.page

    # obtaining the values of the event.
    on_resize = data.on_resize
    
    page.title = 'Use resize'
    
    return ft.View(
        route='/resize',
        controls=[
            ft.Text('Use Resize', size=30),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
```
When we get the values of the event, we can use the methods that this `on_resize` object has.

* `heightX(<value>)` : This method allows to obtain the values of the height of the page, which requires as parameter to enter an integer value from 1 to 100 (100 = 100%).

* `widthX(<value>)` : This method is similar to the previous one in terms of page width.

Manipulation of the margin or padding of the page, this is important since it allows to use the previous methods correctly, that is to say the margin or paddinfg of the page has to be 0 so that the previous methods work correctly, in the case that you want to put a margin, customized, you can correct it modifying in margin of `on_resize`.

!!! note
    If the `AppBar` control is used, if the padding is 0, the `on_resize` margin must be 28 on the y-axis (platform dependent).

* `margin_y` : Requires an integer value on the y-axis.
* `margin_x` : Requires an integer value on the x-axis.

### **2. Example**
```python hl_lines="6 9 18 22 23 27"
@app.page(route="/resize")
def resize_page(data:fs.Datasy):
    page = data.page

    # obtaining the values of the event.
    on_resize = data.on_resize

    # Modifying the customized margin.
    on_resize.margin_y = 10
    
    page.title = 'Use resize'
    
    return ft.View(
        route='/resize',
        controls=[
            ft.Container(
                bgcolor=ft.colors.GREEN_600,
                height=on_resize.heightX(50)
            ),
            ft.Container(
                bgcolor=ft.colors.BLUE_600,
                height=on_resize.heightX(50),
                width=on_resize.widthX(50)
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=10, # Customized padding
    )

```
#### Mode

![on-resize](../images/on-resize.png "on-resize")

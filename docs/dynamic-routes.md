FletEasy provides a simple and powerful routing to manage the access to the pages created, it contains 3 ways of use (choose the one that suits you best).

## **Simple form**
Obtain the values of the parameters of the url, by means of the parameter data of the function.

### **Example**
```python hl_lines="6 12"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/test/10/user/dxs")

@app.page(route="/test/{id}/user/{name}", title="Flet-Easy")
def home_page(data: fs.Datasy, id, name):

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text(f"ID: {id} \nNAME: {name}", size=50),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

app.run(view=ft.AppView.WEB_BROWSER)
```
### 🎬 **Mode**
![alt video](assets/gifs/route-simple.gif "route simple")

## **Advanced Form**
Use dynamic parameters in the url to contain specific data, for example `id` is requested to be a number and `name` a string. For more information [here](https://github.com/r1chardj0n3s/parse#format-specification)

### **Example**
```python hl_lines="4 6-7"
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/test/10/user/dxs")

@app.page(route="/test/{id:d}/user/{name:l}", title="Flet-Easy")
def home_page(data: fs.Datasy, id:int, name:str):

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text(f"ID: {id} \nNAME: {name}", size=50),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

app.run(view=ft.AppView.WEB_BROWSER)

```
### 🎬 **Mode**
![alt video](assets/gifs/route-advanced.gif "route advanced")

## **Custom validation**
To control the validation of custom data in the dynamic path, you must use the `custom_params` parameter of the `page` decorator, in this you can enter the key and the value as a function, being a dictionary can support a wide variety of data, according to your imagination 🤔.
  
### **Example**
```python hl_lines="5 7-12 15 17"
from uuid import UUID
import flet as ft
import flet_easy as fs

app = fs.FletEasy(route_init="/test/10/user/dxs/a4cb5f2a-2281-4e66-85e4-441a40026357")

def is_uuid(value):
    try:
        UUID(value)
        return value
    except ValueError:
        return False

@app.page(
    route="/test/{id:d}/user/{name:l}/{uuid:Uuid}",
    title="Flet-Easy",
    custom_params={"Uuid": is_uuid},
)
def home_page(data: fs.Datasy, id: int, name: str, uuid: UUID):
    return ft.View(
        controls=[
            ft.Text(f"ID: {id} \nNAME: {name}\nUUID: {uuid}", size=50),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

app.run(view=ft.AppView.WEB_BROWSER)
```
### 🎬 **Mode**
![alt video](assets/gifs/route-custom.gif "route advanced")
  
## **Simple form**
Obtain the values of the parameters of the url, by means of the parameter data of the function.
  
```python hl_lines="1 7-9"
@app.page(route="/test/{id}/user/{name}")
def home_page(data: fs.Datasy, id, name):
    page = data.page
    page.title = "Flet-Easy"
    
    # Another way to obtain the values
    params = data.url_params
    id = params.get('id')
    name = params.get('name')

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text("Home page"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```
## **Advanced Form**
Use dynamic parameters in the url to contain specific data, for example `id` is requested to be a number and `name` a string. For more information [here](https://github.com/r1chardj0n3s/parse#format-specification)

```python hl_lines="1-2 9"
@app.page(route="/test/{id:d}/user/{name:l}")
def home_page(data: fs.Datasy, id:int, name:str):
    page = data.page
    page.title = "Flet-Easy"

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text(f "Home page: id={id} name={name}"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```
## **Custom validation**
To control the validation of custom data in the dynamic path, you must use the `custom_params` parameter of the `page` decorator, in this you can enter the key and the value as a function, being a dictionary can support a wide variety of data, according to your imagination 🤔.
  
### **Example**
```python hl_lines="10-11 18"
from uuid import UUID

def is_uuid(value):
    try:
        uuid.UUID(value)
        return value
    except ValueError:
        return False

@app.page(route="/test/{id:d}/user/{name:l}/{uuid:Uuid}", custom_params={"Uuid": is_uuid})
def home_page(data: fs.Datasy, id:int, name:str, uuid:UUID):
    page = data.page
    page.title = "Flet-Easy"

    return ft.View(
        route="/flet-easy",
        controls=[
            ft.Text(f "Home page: id={id} name={name} uuid={uuid}"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
```

  
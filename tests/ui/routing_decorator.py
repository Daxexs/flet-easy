import asyncio

import flet as ft

import flet_easy as fs

app = fs.FletEasy(route_init="/text-return")  # logger=True for debugging

""" NOTE: v0.3.0
- Return ft.View is recommended
- Return ft.Text is supported
- Return list of controls is supported
- Return string is supported
- Return class is supported
- Return ft.Component is supported
- Parameter data: fs.Datasy is optional in all cases
 """


async def go_route(route: str, data: fs.Datasy):
    await asyncio.sleep(2)
    await data.page.push_route(route)


async def close_app(page: ft.Page):
    await asyncio.sleep(3)
    print("✅ close app - tests routing_decorator.py success!")
    await page.window.close()


# 1. No parameters, return ft.Text Control flet is supported, without decorator @ft.component
@app.page(route="/text-return", title="Text Return")
def text_return(data: fs.Datasy):
    data.page.run_task(go_route, "/list-controls", data)
    return ft.Text("Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)


# 2. Return list of controls without decorator @ft.component
@app.page(route="/list-controls", title="List Controls")
def list_controls(data: fs.Datasy):
    data.page.run_task(go_route, "/string-return", data)
    return [ft.Text("Test return list of controls!"), ft.Text("Test return list of controls 2!")]


# 3. Return string (should be wrapped in ft.Text) without decorator @ft.component
@app.page(route="/string-return", title="String Return")
def string_return(data: fs.Datasy):
    data.page.run_task(go_route, "/text-class-return", data)
    return f"Test return string!, {data.route}"


# 4. Return class (should be wrapped in ft.View) without decorator @ft.component
@app.page(route="/text-class-return", title="Text Class Return")
class TextClassReturn:
    def build(self, data: fs.Datasy):
        data.page.run_task(go_route, "/view-return", data)
        return ft.Text("Test return class! - ft.Text")


# 5. Return ft.View without decorator @ft.component
@app.page(route="/view-return", title="View Return")
def view_return(data: fs.Datasy):
    data.page.run_task(go_route, "/text-return-component", data)
    return ft.View(
        controls=[
            ft.Text("Test return ft.View!", expand=True, align=ft.Alignment.CENTER),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# ---------------- with decorator @ft.component
@ft.component
@app.page(route="/text-return-component", title="Text Return Component")
def text_return_component(data: fs.Datasy):
    data.page.run_task(go_route, "/list-controls-component", data)
    return ft.Text("(component) Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)


# 2. Return list of controls without decorator @ft.component
@ft.component
@app.page(route="/list-controls-component", title="List Controls Component")
def list_controls_component(data: fs.Datasy):
    data.page.run_task(go_route, "/string-return-component", data)
    return [
        ft.Text("(component) Test return list of controls!"),
        ft.Text("Test return list of controls 2!"),
    ]


# 3. Return string (should be wrapped in ft.Text) without decorator @ft.component
@ft.component
@app.page(route="/string-return-component", title="String Return Component")
def string_return_component(data: fs.Datasy):
    data.page.run_task(go_route, "/text-class-return-component", data)
    return f"(component) Test return string!, {data.route}"


# 4. Return class (should be wrapped in ft.View) without decorator @ft.component
@app.page(route="/text-class-return-component", title="Text Class Return Component")
class TextClassReturnComponent:
    @ft.component
    def build(self):
        self.data.page.run_task(go_route, "/view-return-component", self.data)
        return ft.Text("(component) Test return class! - ft.Text")


# 5. Return ft.View without decorator @ft.component
@ft.component
@app.page(route="/view-return-component", title="View Return Component")
def view_return_component(data: fs.Datasy):
    data.page.run_task(go_route, "/no-params-2", data)
    return ft.View(
        controls=[
            ft.Text("(component) Test return ft.View!", expand=True, align=ft.Alignment.CENTER),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# add subrouter
app2 = fs.AddPagesy()


# 6. subrouter: data is optional in all cases, support all return types [ft.View, ft.Text, list, str, ft.Component] without decorator @ft.component
@app2.page(route="/no-params-2", title="No Params 2")
def no_params_2(data: fs.Datasy):
    data.page.run_task(go_route, "/no-params-3", data)
    return ft.Text("This works now! 2", expand=True, align=ft.Alignment.CENTER)


# 7. subrouter: data is optional in all cases, test support return ft.View  with decorator @ft.component
@ft.component
@app2.page(route="/no-params-3", title="No Params 3")
def no_params_3():

    async def go_page():
        await ft.context.page.push_route("/no-params-2")

    # close app
    ft.context.page.run_task(close_app, ft.context.page)

    return ft.View(
        controls=[
            ft.Text("This works now! 3", expand=True, align=ft.Alignment.CENTER),
            ft.Button("go no params", on_click=go_page),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# add pagesy to app
app.add_pages(app2)

if __name__ == "__main__":
    app.run()

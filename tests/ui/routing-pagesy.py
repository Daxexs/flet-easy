import asyncio

import flet as ft

import flet_easy as fs

app = fs.FletEasy(route_init="/text-return", logger=True)  # logger=True for debugging

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
    print("✅ close app - tests routing-pagesy.py success!")
    await page.window.close()


# 1. No parameters, return ft.Text Control flet is supported, without decorator @ft.component
# route="/text-return", title="Text Return"
def text_return(data: fs.Datasy):
    data.page.run_task(go_route, "/list-controls", data)
    return ft.Text("Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)


# 2. Return list of controls without decorator @ft.component
# route="/list-controls", title="List Controls"
def list_controls(data: fs.Datasy):
    data.page.run_task(go_route, "/string-return", data)
    return [ft.Text("Test return list of controls!"), ft.Text("Test return list of controls 2!")]


# 3. Return string (should be wrapped in ft.Text) without decorator @ft.component
# route="/string-return", title="String Return"
def string_return(data: fs.Datasy):
    data.page.run_task(go_route, "/text-class-return", data)
    return f"Test return string!, {data.route}"


# 4. Return class (should be wrapped in ft.View) without decorator @ft.component
# route="/text-class-return", title="Text Class Return"
class TextClassReturn:
    def build(self, data: fs.Datasy):
        data.page.run_task(go_route, "/view-return", data)
        return ft.Text("Test return class! - ft.Text")


# 5. Return ft.View without decorator @ft.component
# route="/view-return", title="View Return"
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
# 1. No parameters, return ft.Text Control flet is supported, without decorator @ft.component
# route="/text-return-component", title="Text Return Component"
@ft.component
def text_return_component(data: fs.Datasy):
    data.page.run_task(go_route, "/list-controls-component", data)
    return ft.Text("(component) Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)


# 2. Return list of controls without decorator @ft.component
# route="/list-controls-component", title="List Controls Component"
@ft.component
def list_controls_component(data: fs.Datasy):
    data.page.run_task(go_route, "/string-return-component", data)
    return [
        ft.Text("(component) Test return list of controls!"),
        ft.Text("Test return list of controls 2!"),
    ]


# 3. Return string (should be wrapped in ft.Text) without decorator @ft.component
# route="/string-return-component", title="String Return Component"
@ft.component
def string_return_component(data: fs.Datasy):
    data.page.run_task(go_route, "/text-class-return-component", data)
    return f"(component) Test return string!, {data.route}"


# 4. Return class (should be wrapped in ft.View) without decorator @ft.component
# route="/text-class-return-component", title="Text Class Return Component"
class TextClassReturnComponent:
    def __init__(self, data: fs.Datasy):
        self.data = data

    @ft.component
    def build(self):
        self.data.page.run_task(go_route, "/view-return-component", self.data)
        return ft.Text("(component) Test return class! - ft.Text")


# 5. Return ft.View without decorator @ft.component
# route="/view-return-component", title="View Return Component"
class ViewReturnComponent:
    @ft.component
    def build(self):
        self.data.page.run_task(go_route, "/no-params-2", self.data)
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
# route="/no-params-2", title="No Params 2"
def no_params_2(data: fs.Datasy):
    data.page.run_task(go_route, "/no-params-3", data)
    return ft.Text("This works now! 2", expand=True, align=ft.Alignment.CENTER)


# 7. subrouter: data is optional in all cases, test support return ft.View  with decorator @ft.component
# route="/no-params-3", title="No Params 3"
@ft.component
def no_params_3():

    # close app
    ft.context.page.run_task(close_app, ft.context.page)

    return ft.View(
        controls=[
            ft.Text("This works now! 3", expand=True, align=ft.Alignment.CENTER),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
    )


# add subrouter pagesy  to app
app.add_pages(app2)

# add routes
app.add_routes(
    add_views=[
        fs.Pagesy(route="/text-return", view=text_return, title="Text Return"),
        fs.Pagesy(route="/list-controls", view=list_controls, title="List Controls"),
        fs.Pagesy(route="/string-return", view=string_return, title="String Return"),
        fs.Pagesy(route="/text-class-return", view=TextClassReturn, title="Text Class Return"),
        fs.Pagesy(route="/view-return", view=view_return, title="View Return"),
        fs.Pagesy(
            route="/text-return-component",
            view=text_return_component,
            title="Text Return Component",
        ),
        fs.Pagesy(
            route="/list-controls-component",
            view=list_controls_component,
            title="List Controls Component",
        ),
        fs.Pagesy(
            route="/string-return-component",
            view=string_return_component,
            title="String Return Component",
        ),
        fs.Pagesy(
            route="/text-class-return-component",
            view=TextClassReturnComponent,
            title="Text Class Return Component",
        ),
        fs.Pagesy(
            route="/view-return-component",
            view=ViewReturnComponent,
            title="View Return Component",
        ),
        fs.Pagesy(
            route="/no-params-2",
            view=no_params_2,
            title="No Params 2",
        ),
        fs.Pagesy(
            route="/no-params-3",
            view=no_params_3,
            title="No Params 3",
        ),
    ]
)

if __name__ == "__main__":
    app.run()

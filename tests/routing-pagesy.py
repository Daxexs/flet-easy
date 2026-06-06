import asyncio
from unittest.mock import MagicMock

import flet as ft
import pytest

import flet_easy as fs

# --- Fixtures ---


@pytest.fixture
def app():
    """Create a FletEasy app with all routes from parament-handler.py."""
    app = fs.FletEasy(route_init="/text-return")

    # --- WITHOUT @ft.component ---

    # 1. No parameters, return ft.Text
    def text_return():
        return ft.Text("Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)

    # 2. Return list of controls
    def list_controls():
        return [
            ft.Text("Test return list of controls!"),
            ft.Text("Test return list of controls 2!"),
        ]

    # 3. Return string (should be wrapped in ft.Text)
    def string_return(data: fs.Datasy):
        return f"Test return string!, {data.route}"

    # 4. Return class (should be wrapped in ft.View)
    class TextClassReturn:
        def build(self):
            return ft.Text("Test return class! - ft.Text")

    # 5. Return ft.View
    def view_return():
        return ft.View(
            controls=[
                ft.Text("Test return ft.View!", expand=True, align=ft.Alignment.CENTER),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )

    # --- WITH @ft.component decorator ---
    # In these tests, we put @ft.component INSIDE @app.page so that Pagesy detects it
    # as a component immediately (important for local functions in tests).

    @ft.component
    def text_return_component():
        return ft.Text("(component) Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)

    @ft.component
    def list_controls_component():
        return [
            ft.Text("(component) Test return list of controls!"),
            ft.Text("(component) Test return list of controls 2!"),
        ]

    @ft.component
    def string_return_component(data: fs.Datasy):
        return f"(component) Test return string!, {data.route}"

    @ft.component
    class TextClassReturnComponent:
        def build(self):
            return ft.Text("(component) Test return class! - ft.Text")

    @ft.component
    def view_return_component():
        return ft.View(
            controls=[
                ft.Text("(component) Test return ft.View!", expand=True, align=ft.Alignment.CENTER),
            ],
            vertical_alignment="center",
            horizontal_alignment="center",
        )

    # Subrouter tests
    app2 = fs.AddPagesy()

    # 6. subrouter return ft.Text
    @app2.page(route="/no-params-2", title="No Params 2")
    def no_params_2():
        return ft.Text("This works now! 2", expand=True, align=ft.Alignment.CENTER)

    # 7. subrouter return ft.View with @ft.component
    @ft.component
    @app2.page(route="/no-params-3", title="No Params 3")
    def no_params_3():
        async def go_page():
            await ft.context.page.push_route("/no-params")

        return ft.View(
            controls=[
                ft.Text("This works now! 3", expand=True, align=ft.Alignment.CENTER),
                ft.Button("go no params", on_click=go_page),
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
                view=view_return_component,
                title="View Return Component",
            ),
        ]
    )

    return app


@pytest.fixture
def mock_page():
    """Create a mocked ft.Page object compatible with Flet-Easy."""
    page = MagicMock()
    page.views = []
    page.route = "/"
    page.web = False

    def mock_render(fn):
        try:
            from flet.components.utils import _CURRENT_RENDERER

            mock_renderer = MagicMock()

            def mock_render_component(fn, args, kwargs, key=None):
                # Simply call the original function/class with its arguments
                return fn(*args, **kwargs)

            mock_renderer.render_component.side_effect = mock_render_component
            token = _CURRENT_RENDERER.set(mock_renderer)
        except ImportError:
            token = None

        try:
            res = fn()
        finally:
            if token:
                from flet.components.utils import _CURRENT_RENDERER

                _CURRENT_RENDERER.reset(token)

        if isinstance(res, ft.View):
            if not res.route or res.route == "/":
                res.route = page.route
            page.views.append(res)
        elif isinstance(res, list):
            page.views.append(ft.View(route=page.route, controls=res))
        else:
            page.views.append(ft.View(route=page.route, controls=[res]))
        page.update()

    page.render_views = MagicMock(side_effect=mock_render)
    page.render = MagicMock(side_effect=mock_render)
    page.update = MagicMock()

    # Mocking run_task to execute the function correctly (handling async)
    page.tasks = []

    def sync_run_task(f, *args, **kwargs):
        res = f(*args, **kwargs)
        if asyncio.iscoroutine(res):
            page.tasks.append(asyncio.create_task(res))
        return res

    page.run_task = MagicMock(side_effect=sync_run_task)
    return page


# --- Tests ---


@pytest.mark.anyio
async def test_route_rendering(app, mock_page):
    """Verify that each route renders the expected controls."""

    # Initialize the app with the mock page
    app.start(mock_page)

    # Yield to allow background tasks scheduled via run_task to execute
    await asyncio.sleep(0)

    # Access the private router instance
    fsx = app._FletEasy__fsx

    # Mock share.clear to avoid SharedPreferences RuntimeError in mock environment
    fsx._data.share.clear = MagicMock(return_value=None)

    # Config push_route to trigger the router's __route_change
    async def side_effect_push_route(route):
        mock_page.route = route
        event = MagicMock()
        event.route = route
        await fsx._route_change(event)

    mock_page.push_route = MagicMock(side_effect=side_effect_push_route)

    async def navigate(route):
        await mock_page.push_route(route)

    # --- 1-5 Imperative Routes (Without component) ---

    # 1. /text-return
    await navigate("/text-return")
    last_view = mock_page.views[-1]

    assert isinstance(last_view, ft.View)
    assert last_view.route == "/text-return"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "Test return ft.Text!"

    print("\n\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 2. /list-controls
    await navigate("/list-controls")
    last_view = mock_page.views[-1]

    assert isinstance(last_view, ft.View)
    assert last_view.route == "/list-controls"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "Test return list of controls!"
    assert isinstance(last_view.controls[1], ft.Text)
    assert last_view.controls[1].value == "Test return list of controls 2!"
    print(
        "\n✅ Route: ",
        last_view.route,
        " || Controls[0].value: ",
        last_view.controls[0].value,
        " || Controls[1].value: ",
        last_view.controls[1].value,
    )

    # 3. /string-return
    await navigate("/string-return")
    last_view = mock_page.views[-1]

    assert isinstance(last_view, ft.View)
    assert last_view.route == "/string-return"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "Test return string!, /string-return"

    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 4. /text-class-return
    await navigate("/text-class-return")
    last_view = mock_page.views[-1]

    assert isinstance(last_view, ft.View)
    assert last_view.route == "/text-class-return"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "Test return class! - ft.Text"
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 5. /view-return
    await navigate("/view-return")
    last_view = mock_page.views[-1]

    assert isinstance(last_view, ft.View)
    assert last_view.route == "/view-return"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "Test return ft.View!"

    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # --------- using component ---------
    print("\n\n--------- using component ---------")
    # 6. /text-return-component
    await navigate("/text-return-component")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/text-return-component"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "(component) Test return ft.Text!"
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 7. /list-controls-component
    await navigate("/list-controls-component")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/list-controls-component"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "(component) Test return list of controls!"
    assert isinstance(last_view.controls[1], ft.Text)
    assert last_view.controls[1].value == "(component) Test return list of controls 2!"
    print(
        "\n✅ Route: ",
        last_view.route,
        " || Controls[0].value: ",
        last_view.controls[0].value,
        " || Controls[1].value: ",
        last_view.controls[1].value,
    )

    # 8. /string-return-component
    await navigate("/string-return-component")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/string-return-component"
    assert isinstance(last_view.controls[0], ft.Text)
    assert (
        last_view.controls[0].value == "(component) Test return string!, /string-return-component"
    )
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 9. /text-class-return-component
    await navigate("/text-class-return-component")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/text-class-return-component"

    control = last_view.controls[0]
    # If it's a declarative component instance, we call build() to verify its content
    if not isinstance(control, ft.Text) and hasattr(control, "build"):
        control = control.build()

    assert isinstance(control, ft.Text)
    assert control.value == "(component) Test return class! - ft.Text"
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", control.value)

    # 10. /view-return-component
    await navigate("/view-return-component")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/view-return-component"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "(component) Test return ft.View!"
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # --- 11-12 Subrouter Routes ---
    print("\n\n--------- Subrouter Routes ---------")

    # 11. /no-params-2 (component in subrouter)
    await navigate("/no-params-2")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/no-params-2"

    control = last_view.controls[0]
    if not isinstance(control, ft.Text) and hasattr(control, "build"):
        control = control.build()

    assert isinstance(control, ft.Text)
    assert control.value == "This works now! 2"
    print("✅ Route: ", last_view.route, " || Controls[0].value: ", control.value)

    # 12. /no-params-3 (Component in subrouter)
    print("\n-- Using component in subrouter --")

    await navigate("/no-params-3")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/no-params-3"

    control = last_view.controls[0]
    if not isinstance(control, ft.Text) and hasattr(control, "build"):
        control = control.build()

    assert isinstance(control, ft.Text)
    assert control.value == "This works now! 3"
    print("✅ Route: ", last_view.route, " || Controls[0].value: ", control.value)

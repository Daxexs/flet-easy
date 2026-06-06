import asyncio
from unittest.mock import MagicMock

import flet as ft
import pytest

import flet_easy as fs

# --- Fixtures ---


@pytest.fixture
def app():
    """Create a FletEasy app with all routes."""
    app = fs.FletEasy(route_init="/text-return")

    # --- WITHOUT @ft.component ---

    # 1. No parameters, return ft.Text
    @app.page(route="/text-return", title="Text Return")
    def text_return():
        return ft.Text("Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)

    # 2. Return list of controls
    @app.page(route="/list-controls", title="List Controls")
    def list_controls():
        return [
            ft.Text("Test return list of controls!"),
            ft.Text("Test return list of controls 2!"),
        ]

    # 3. Return string (should be wrapped in ft.Text)
    @app.page(route="/string-return", title="String Return")
    def string_return(data: fs.Datasy):
        return f"Test return string!, {data.route}"

    # 4. Return class (should be wrapped in ft.View)
    @app.page(route="/text-class-return", title="Text Class Return")
    class TextClassReturn:
        def build(self):
            return ft.Text("Test return class! - ft.Text")

    # 5. Return ft.View
    @app.page(route="/view-return", title="View Return")
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
    @app.page(route="/text-return-component", title="Text Return Component")
    def text_return_component():
        return ft.Text("(component) Test return ft.Text!", expand=True, align=ft.Alignment.CENTER)

    @ft.component
    @app.page(route="/list-controls-component", title="List Controls Component")
    def list_controls_component():
        return [
            ft.Text("(component) Test return list of controls!"),
            ft.Text("(component) Test return list of controls 2!"),
        ]

    @ft.component
    @app.page(route="/string-return-component", title="String Return Component")
    def string_return_component(data: fs.Datasy):
        return f"(component) Test return string!, {data.route}"

    @ft.component
    @app.page(route="/text-class-return-component", title="Text Class Return Component")
    class TextClassReturnComponent:
        def build(self):
            return ft.Text("(component) Test return class! - ft.Text")

    @ft.component
    @app.page(route="/view-return-component", title="View Return Component")
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

    app.add_pages(app2)
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

            token = _CURRENT_RENDERER.set(MagicMock())
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
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "(component) Test return class! - ft.Text"
    print("\n✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

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
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "This works now! 2"
    print("✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

    # 12. /no-params-3 (Component in subrouter)
    print("\n-- Using component in subrouter --")

    await navigate("/no-params-3")
    last_view = mock_page.views[-1]
    assert isinstance(last_view, ft.View)
    assert last_view.route == "/no-params-3"
    assert isinstance(last_view.controls[0], ft.Text)
    assert last_view.controls[0].value == "This works now! 3"
    print("✅ Route: ", last_view.route, " || Controls[0].value: ", last_view.controls[0].value)

import asyncio
from unittest.mock import AsyncMock, MagicMock

import flet as ft
import pytest

import flet_easy as fs

# --- Fixtures ---


class MockSharedPreferences:
    """A mock SharedPreferences that handles both SessionStorage and SharedPreferences."""

    def __init__(self, *args, **kwargs):
        # Handles:
        # 1. SharedPreferences(prefix="...")
        # 2. SessionStorage(page)
        # 3. SharedPreferencesEdit(prefix="...")
        # 4. SessionStorageEdit(page)
        self._prefix = kwargs.get("prefix", "")
        if args and isinstance(args[0], str):
            self._prefix = args[0]

        self._store = {}

    async def set(self, key, value):
        self._store[f"{self._prefix}{key}"] = value

    async def get(self, key):
        return self._store.get(f"{self._prefix}{key}")

    async def remove(self, key):
        self._store.pop(f"{self._prefix}{key}", None)

    async def clear(self):
        if self._prefix:
            keys_to_remove = [k for k in self._store if k.startswith(self._prefix)]
            for k in keys_to_remove:
                self._store.pop(k, None)
        else:
            self._store.clear()

    async def get_keys(self, prefix):
        full_prefix = f"{self._prefix}{prefix}"
        return [k[len(self._prefix) :] for k in self._store if k.startswith(full_prefix)]

    @property
    def page(self):
        return MagicMock()


@pytest.fixture
def app(monkeypatch):
    """Create a FletEasy app with routes from shared_preferences.py."""

    # Monkeypatch SharedPreferences and SharedPreferencesEdit everywhere
    if hasattr(ft, "SharedPreferences"):
        monkeypatch.setattr(ft, "SharedPreferences", MockSharedPreferences)
    if hasattr(ft, "SessionStorage"):
        monkeypatch.setattr(ft, "SessionStorage", MockSharedPreferences)

    import flet_easy.ui.controls as controls

    monkeypatch.setattr(controls, "SharedPreferencesEdit", MockSharedPreferences)
    monkeypatch.setattr(controls, "SessionStorageEdit", MockSharedPreferences)

    import flet_easy.core.data as data_module

    monkeypatch.setattr(data_module, "SharedPreferencesEdit", MockSharedPreferences)
    monkeypatch.setattr(data_module, "SessionStorageEdit", MockSharedPreferences)

    app = fs.FletEasy(route_init="/")

    @app.page("/", title="test")
    async def test_page(data: fs.Datasy):
        page = data.page
        has_sp = hasattr(ft, "SharedPreferences")

        # reset all data
        if has_sp:
            await ft.SharedPreferences().clear()
            await page.shared_preferences.clear()
            await data.share.clear()
        else:
            await data.share.clear()

        if has_sp:
            # class SharedPreferences is deprecated since version 0.80.0 and will be removed in version 0.90.0. Use SharedPreferences() instead.
            await ft.SharedPreferences().set("Shared", "1")

            # class SessionStorage is deprecated since version 0.80.0 and will be removed in version 0.90.0. Use SharedPreferences() instead.
            await page.shared_preferences.set("page-shared_preferences", "1")

            # Use SharedPreferencesEdit to shared data between pages, and the data will be cleared when the page is closed.
            await data.share.set("data-shared", "1")

            # get values
            shared = await ft.SharedPreferences().get("Shared")

            page_shared_preferences = await ft.SharedPreferences().get("page-shared_preferences")
            assert shared == "1"
            assert page_shared_preferences == "1"

            # print values
            print("\n✅ test 1 - SharedPreferences")
            print(f"✅ Shared = 1: {shared}")
            print(f"✅ page-shared_preferences = 1: {page_shared_preferences}")
        else:
            await data.share.set("data-shared", "1")

            print("\n✅ test 1 - SessionStorage")

        # get values
        data_share = await data.share.get("data-shared")
        assert data_share == "1"

        # print values
        print(f"✅ data-shared = 1: {data_share}")

        return ft.View(
            controls=[
                ft.Text("test 1"),
            ]
        )

    @app.page("/test", title="test 2")
    async def test_page2(data: fs.Datasy):
        page = data.page
        has_sp = hasattr(ft, "SharedPreferences")

        if has_sp:
            # it should always work with shared_data set to True or False
            assert await ft.SharedPreferences().get("Shared") == "1"
            assert await page.shared_preferences.get("page-shared_preferences") == "1"

            # data-shared should be cleared when the page is closed (navigation)
            assert await data.share.get("data-shared") is None

            # send the value of data.share.get("data-shared") to route /test3
            await data.share.set("data-shared-2", "1")

            # get values
            shared = await ft.SharedPreferences().get("Shared")
            page_shared_preferences = await ft.SharedPreferences().get("page-shared_preferences")

            # print values
            print("\n✅ test 2 - SharedPreferences")
            print(f"✅ Shared = 1: {shared}")
            print(f"✅ page-shared_preferences = 1: {page_shared_preferences}")
        else:
            assert await data.share.get("data-shared") is None
            await data.share.set("data-shared-2", "1")

            print("\n✅ test 2 - SessionStorage")

        data_shared = await data.share.get("data-shared")
        data_shared_2 = await data.share.get("data-shared-2")

        # print values
        print(f"✅ data-shared = None: {data_shared}")
        print(f"✅ data-shared-2 = 1: {data_shared_2}")

        return ft.View(
            controls=[
                ft.Text("Hello"),
            ]
        )

    @app.page("/test3", title="test 3", share_data=True)
    async def test_page3(data: fs.Datasy):
        has_sp = hasattr(ft, "SharedPreferences")

        if has_sp:
            # it should always work with shared_data set to True or False
            assert await ft.SharedPreferences().get("Shared") == "1"
            assert await data.page.shared_preferences.get("page-shared_preferences") == "1"

            # share_data=True, so data-shared-2 should persist from /test to /test3
            assert await data.share.get("data-shared-2") == "1"

            # get values
            shared = await ft.SharedPreferences().get("Shared")
            page_shared_preferences = await ft.SharedPreferences().get("page-shared_preferences")

            # print values
            print("\n✅ test 3 - SharedPreferences")
            print(f"✅ Shared = 1: {shared}")
            print(f"✅ page-shared_preferences = 1: {page_shared_preferences}")
        else:
            assert await data.share.get("data-shared-2") == "1"

            print("\n✅ test 3 - SessionStorage")

        data_shared = await data.share.get("data-shared")
        data_shared_2 = await data.share.get("data-shared-2")

        # print values
        print(f"✅ data-shared = None: {data_shared}")
        print(f"✅ data-shared-2 = 1: {data_shared_2}")

        return ft.View(
            controls=[
                ft.Text("Hello"),
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
        res = fn()
        if isinstance(res, ft.View):
            page.views.append(res)
        elif isinstance(res, list):
            page.views.append(ft.View(controls=res))
        else:
            page.views.append(ft.View(controls=[res]))
        page.update()

    page.render_views = MagicMock(side_effect=mock_render)
    page.render = MagicMock(side_effect=mock_render)
    page.update = MagicMock()

    # Mocking shared_preferences
    mock_sp = MagicMock()
    mock_sp.set = AsyncMock()
    mock_sp.get = AsyncMock()
    mock_sp.clear = AsyncMock()
    mock_sp.remove = AsyncMock()
    mock_sp.get_keys = AsyncMock(return_value=[])

    # Store for mock_sp to behave somewhat realistically
    sp_store = {}

    async def sp_set(k, v):
        sp_store[k] = v

    async def sp_get(k):
        return sp_store.get(k)

    async def sp_clear():
        sp_store.clear()

    async def sp_remove(k):
        sp_store.pop(k, None)

    async def sp_get_keys(prefix):
        return [k for k in sp_store if k.startswith(prefix)]

    mock_sp.set.side_effect = sp_set
    mock_sp.get.side_effect = sp_get
    mock_sp.clear.side_effect = sp_clear
    mock_sp.remove.side_effect = sp_remove
    mock_sp.get_keys.side_effect = sp_get_keys

    page.shared_preferences = mock_sp

    # Mocking run_task to execute the function correctly (handling async)
    page.tasks = []

    def sync_run_task(f, *args, **kwargs):
        res = f(*args, **kwargs)
        if asyncio.iscoroutine(res):
            # In a real app, this would be scheduled. Here we might need to wait for it.
            # But for simplicity, we'll let the test handle it.
            page.tasks.append(asyncio.create_task(res))
        return res

    page.run_task = MagicMock(side_effect=sync_run_task)
    return page


# --- Tests ---


@pytest.mark.anyio
async def test_shared_preferences_flow(app, mock_page, monkeypatch):
    """Verify shared preferences and data sharing flow."""

    # We need to monkeypatch ft.SharedPreferences to return our mock_sp
    # because it's called as ft.SharedPreferences() in the app code
    if hasattr(ft, "SharedPreferences"):
        monkeypatch.setattr(ft, "SharedPreferences", lambda: mock_page.shared_preferences)
    if hasattr(ft, "SessionStorage"):
        monkeypatch.setattr(ft, "SessionStorage", lambda: mock_page.shared_preferences)

    # Initialize the app with the mock page
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx

    # Config push_route to trigger the router's __route_change
    async def side_effect_push_route(route):
        mock_page.route = route
        event = MagicMock()
        event.route = route
        await fsx._route_change(event)

    mock_page.push_route = MagicMock(side_effect=side_effect_push_route)

    async def navigate(route):
        await mock_page.push_route(route)
        # Wait for any tasks spawned by go_route if necessary
        # In this test, we navigate manually using mock_page.push_route
        # which calls the router's __route_change directly.

    # 1. Start at /
    await navigate("/")

    # 2. Go to /test (should verify assertions in test_page2)
    # The assertions are inside the page function, so if they fail, navigating will raise AssertionError
    await navigate("/test")

    # 3. Go to /test3 (should verify assertions in test_page3)
    await navigate("/test3")

    print("\n✅ Shared preferences flow verified successfully!")

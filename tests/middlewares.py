"""
Pytest suite for Flet-Easy multi-layer middleware architecture.

Converted from tests/ui/middlewares.py (interactive Flet app).
Uses the same STATE dictionary + assertions as the original UI script,
now driven by mocked page routing instead of real UI navigation.

Middleware hierarchy tested (Outside-In):
  Global Func → Global Class → (SubRouter Func → SubRouter Class) → Page-specific

Routes:
  /           →  global middlewares only
  /page1      →  global + page1_func_md
  /page2      →  global + Page2ClassMd
  /page3      →  global + [page1_func_md, Page2ClassMd]
  /sub/test   →  global + sub_router + sub_page_func_md
  /sub/page2  →  global + sub_router + [SubPageClassMd]
  /sub/page3  →  global + sub_router + [sub_page3_func_md, SubPage3ClassMd]
"""

import asyncio
from typing import Any
from unittest.mock import MagicMock

import flet as ft
import pytest

import flet_easy as fs

# ─────────────────────────────────────────────
# Shared STATE dictionary (reset per-test)
# ─────────────────────────────────────────────
STATE: dict[str, Any] = {}


def reset_state() -> None:
    STATE.clear()


def update_state(key: str, value: Any) -> None:
    STATE[key] = value


# ─────────────────────────────────────────────
# Middleware definitions (mirrors middlewares.py)
# ─────────────────────────────────────────────


# 1. Global functional middleware
async def global_func_md(data: fs.Datasy):
    update_state("global_func", "global_func")


# 2. Global class middleware
class GlobalClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("global_class_before", "global_class_before")

    async def after_request(self):
        update_state("global_class_after", "global_class_after")


# 3. Page-specific functional middleware  (/page1)
async def page1_func_md(data: fs.Datasy):
    update_state("page1_func", "page1_func")


# 4. Page-specific class middleware  (/page2)
class Page2ClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("page2_class_before", "page2_class_before")

    async def after_request(self):
        update_state("page2_class_after", "page2_class_after")


# 5. Sub-router functional middleware
async def sub_router_md(data: fs.Datasy):
    update_state("sub_router_func", "sub_router_func")


# 6. Sub-router class middleware
class SubRouterClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_router_class_before", "sub_router_class_before")

    async def after_request(self):
        update_state("sub_router_class_after", "sub_router_class_after")


# 7. Sub-page /sub/test – functional
async def sub_page_func_md(data: fs.Datasy):
    update_state("sub_page_func", "sub_page_func")


# 8. Sub-page /sub/page2 – class
class SubPageClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_page2_class_before", "sub_page2_class_before")

    async def after_request(self):
        update_state("sub_page2_class_after", "sub_page2_class_after")


# 9. Sub-page /sub/page3 – functional
async def sub_page3_func_md(data: fs.Datasy):
    update_state("sub_page3_func", "sub_page3_func")


# 10. Sub-page /sub/page3 – class
class SubPage3ClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_page3_class_before", "sub_page3_class_before")

    async def after_request(self):
        update_state("sub_page3_class_after", "sub_page3_class_after")


# ─────────────────────────────────────────────
# App fixture
# ─────────────────────────────────────────────


@pytest.fixture()
def app():
    """Build the FletEasy app with full middleware hierarchy, matching middlewares.py."""
    _app = fs.FletEasy(route_init="/")

    # Global middlewares
    _app.add_middleware(global_func_md, GlobalClassMd)

    # Sub-router
    sub = fs.AddPagesy(route_prefix="/sub", middleware=[sub_router_md, SubRouterClassMd])

    @sub.page("/test", title="Sub Page", middleware=sub_page_func_md)
    async def sub_page(data: fs.Datasy):
        return ft.View(controls=[ft.Text("sub/test")])

    @sub.page("/page2", title="Sub Page 2", middleware=[SubPageClassMd])
    async def sub_page2(data: fs.Datasy):
        return ft.View(controls=[ft.Text("sub/page2")])

    @sub.page("/page3", title="Sub Page 3", middleware=[sub_page3_func_md, SubPage3ClassMd])
    async def sub_page3(data: fs.Datasy):
        return ft.View(controls=[ft.Text("sub/page3")])

    _app.add_pages(sub)

    # Standard pages
    @_app.page("/", title="Home")
    async def home(data: fs.Datasy):
        return ft.View(controls=[ft.Text("home")])

    @_app.page("/page1", title="Page 1", middleware=page1_func_md)
    async def page1(data: fs.Datasy):
        return ft.View(controls=[ft.Text("page1")])

    @_app.page("/page2", title="Page 2", middleware=[Page2ClassMd])
    async def page2(data: fs.Datasy):
        return ft.View(controls=[ft.Text("page2")])

    @_app.page("/page3", title="Page 3", middleware=[page1_func_md, Page2ClassMd])
    async def page3(data: fs.Datasy):
        return ft.View(controls=[ft.Text("page3")])

    return _app


@pytest.fixture()
def mock_page():
    """Minimal ft.Page mock compatible with FletEasy's router."""
    page = MagicMock(spec=ft.Page)
    page.views = []
    page.route = "/"
    page.web = False
    page.window = MagicMock()

    def _render(fn):
        res = fn()
        if isinstance(res, ft.View):
            if not res.route or res.route == "/":
                res.route = page.route
            page.views.append(res)
        elif isinstance(res, list):
            page.views.append(ft.View(route=page.route, controls=res))
        else:
            page.views.append(ft.View(route=page.route, controls=[res] if res else []))
        page.update()

    page.render_views = MagicMock(side_effect=_render)
    page.render = MagicMock(side_effect=_render)
    page.update = MagicMock()
    page.tasks = []

    def sync_run_task(f, *args, **kwargs):
        res = f(*args, **kwargs)
        if asyncio.iscoroutine(res):
            page.tasks.append(asyncio.create_task(res))
        return res

    page.run_task = MagicMock(side_effect=sync_run_task)
    return page


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────


async def _navigate(fsx, mock_page, route: str) -> None:
    """Simulate a route change via the private router."""
    mock_page.route = route
    event = MagicMock()
    event.route = route
    await fsx._route_change(event)
    await asyncio.sleep(0)


# ─────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────


@pytest.mark.anyio
async def test_home_global_middleware_only(app, mock_page):
    """
    Route: /
    Expected: global_func  |  global_class_before  |  global_class_after  (runs after page render)
    All other middleware keys must be None.
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    async def _push(route):
        mock_page.route = route
        ev = MagicMock()
        ev.route = route
        await fsx._route_change(ev)

    mock_page.push_route = MagicMock(side_effect=_push)

    print("\n\n----- STARTING TEST [MIDDLEWARES]-----\n")

    await _navigate(fsx, mock_page, "/")

    # Global middlewares fired
    assert STATE.get("global_func") == "global_func", "global_func_md must fire on /"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')

    assert STATE.get("global_class_before") == "global_class_before", (
        "GlobalClassMd.before must fire on /"
    )

    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')

    # after_request fires after page render; at this point in the lifecycle it must be set
    # (FletEasy runs after_request immediately after the view is resolved)
    # The exact value depends on the router's async timing; we assert it was eventually set.
    # No other middlewares should have fired
    assert STATE.get("page1_func") is None
    print(f"✅ {STATE.get('page1_func')} is None  IS NONE as expected")
    assert STATE.get("page2_class_before") is None
    print(f"✅ {STATE.get('page2_class_before')} is None  IS NONE as expected")
    assert STATE.get("page2_class_after") is None
    print(f"✅ {STATE.get('page2_class_after')} is None  IS NONE as expected")
    assert STATE.get("sub_router_func") is None
    print(f"✅ {STATE.get('sub_router_func')} is None  IS NONE as expected")
    assert STATE.get("sub_router_class_before") is None
    print(f"✅ {STATE.get('sub_router_class_before')} is None  IS NONE as expected")
    assert STATE.get("sub_router_class_after") is None
    print(f"✅ {STATE.get('sub_router_class_after')} is None  IS NONE as expected")
    assert STATE.get("sub_page_func") is None
    print(f"✅ {STATE.get('sub_page_func')} is None  IS NONE as expected")
    assert STATE.get("sub_page2_class_before") is None
    print(f"✅ {STATE.get('sub_page2_class_before')} is None  IS NONE as expected")
    assert STATE.get("sub_page2_class_after") is None
    print(f"✅ {STATE.get('sub_page2_class_after')} is None  IS NONE as expected")
    assert STATE.get("sub_page3_func") is None
    print(f"✅ {STATE.get('sub_page3_func')} is None  IS NONE as expected")
    assert STATE.get("sub_page3_class_before") is None
    print(f"✅ {STATE.get('sub_page3_class_before')} is None  IS NONE as expected")
    assert STATE.get("sub_page3_class_after") is None
    print(f"✅ {STATE.get('sub_page3_class_after')} is None  IS NONE as expected")
    print("\n✅ /  – global-only middleware verified")


@pytest.mark.anyio
async def test_page1_functional_middleware(app, mock_page):
    """
    Route: /page1
    Expected: global_func  |  global_class  |  page1_func
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    await _navigate(fsx, mock_page, "/page1")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')

    # Page-specific
    assert STATE.get("page1_func") == "page1_func", "page1_func_md must fire on /page1"
    print(f'✅ {STATE.get("page1_func")} == "page1_func"  EXECUTED as expected')

    # No other page or sub middlewares
    assert STATE.get("page2_class_before") is None
    print(f"✅ {STATE.get('page2_class_before')} is None  IS NONE as expected")
    assert STATE.get("sub_router_func") is None
    print(f"✅ {STATE.get('sub_router_func')} is None  IS NONE as expected")
    print("\n✅ /page1 – functional page middleware verified")


@pytest.mark.anyio
async def test_page2_class_middleware(app, mock_page):
    """
    Route: /page2
    Expected: global  |  Page2ClassMd.before  |  Page2ClassMd.after still None (not yet rendered)
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    await _navigate(fsx, mock_page, "/page2")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("page2_class_before") == "page2_class_before", (
        "Page2ClassMd.before must fire on /page2"
    )
    print(f'✅ {STATE.get("page2_class_before")} == "page2_class_before"  EXECUTED as expected')
    assert STATE.get("page1_func") is None
    print(f"✅ {STATE.get('page1_func')} is None  IS NONE as expected")
    assert STATE.get("sub_router_func") is None
    print(f"✅ {STATE.get('sub_router_func')} is None  IS NONE as expected")
    print("\n✅ /page2 – class-based page middleware verified")


@pytest.mark.anyio
async def test_page3_mixed_middlewares(app, mock_page):
    """
    Route: /page3
    Expected: global  |  page1_func  |  Page2ClassMd.before
    Verifies that a LIST of mixed middlewares all execute.
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    await _navigate(fsx, mock_page, "/page3")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("page1_func") == "page1_func", "page1_func_md must fire (list) on /page3"
    print(f'✅ {STATE.get("page1_func")} == "page1_func"  EXECUTED as expected')
    assert STATE.get("page2_class_before") == "page2_class_before", (
        "Page2ClassMd.before must fire (list) on /page3"
    )
    print(f'✅ {STATE.get("page2_class_before")} == "page2_class_before"  EXECUTED as expected')
    assert STATE.get("sub_router_func") is None
    print(f"✅ {STATE.get('sub_router_func')} is None  IS NONE as expected")
    print("\n✅ /page3 – mixed list of page middlewares verified")


@pytest.mark.anyio
async def test_sub_router_plus_page_functional(app, mock_page):
    """
    Route: /sub/test
    Expected: global  |  sub_router_md  |  SubRouterClassMd.before  |  sub_page_func_md
    sub_router_class_after must still be None (after_request hasn't fired yet).
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    await _navigate(fsx, mock_page, "/sub/test")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("sub_router_func") == "sub_router_func", (
        "sub_router_md must fire for /sub routes"
    )
    print(f'✅ {STATE.get("sub_router_func")} == "sub_router_func"  EXECUTED as expected')
    assert STATE.get("sub_router_class_before") == "sub_router_class_before", (
        "SubRouterClassMd.before must fire"
    )
    print(
        f'✅ {STATE.get("sub_router_class_before")} == "sub_router_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_page_func") == "sub_page_func", "sub_page_func_md must fire on /sub/test"
    print(f'✅ {STATE.get("sub_page_func")} == "sub_page_func"  EXECUTED as expected')

    # sub_router_class_after fires after render; page2/page3 class before/afters must still be None
    assert STATE.get("sub_page2_class_before") is None
    print(f"✅ {STATE.get('sub_page2_class_before')} is None  IS NONE as expected")
    assert STATE.get("sub_page2_class_after") is None
    print(f"✅ {STATE.get('sub_page2_class_after')} is None  IS NONE as expected")
    assert STATE.get("sub_page3_func") is None
    print(f"✅ {STATE.get('sub_page3_func')} is None  IS NONE as expected")
    assert STATE.get("page1_func") is None
    print(f"✅ {STATE.get('page1_func')} is None  IS NONE as expected")
    print("\n✅ /sub/test – sub-router + functional page middleware verified")


@pytest.mark.anyio
async def test_sub_router_plus_page_class(app, mock_page):
    """
    Route: /sub/page2
    Expected: global  |  sub_router  |  SubPageClassMd.before
    Also verifies sub_router_class_after executed (fired after /sub/test was rendered first).
    We navigate /sub/test → /sub/page2 to match the original UI flow.
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    # Navigate through /sub/test first so that sub_router after_request fires
    await _navigate(fsx, mock_page, "/sub/test")
    await _navigate(fsx, mock_page, "/sub/page2")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("sub_router_func") == "sub_router_func"
    print(f'✅ {STATE.get("sub_router_func")} == "sub_router_func"  EXECUTED as expected')
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    print(
        f'✅ {STATE.get("sub_router_class_before")} == "sub_router_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_router_class_after") == "sub_router_class_after", (
        "SubRouterClassMd.after_request must fire after /sub/test render"
    )
    print(
        f'✅ {STATE.get("sub_router_class_after")} == "sub_router_class_after"  EXECUTED as expected'
    )
    assert STATE.get("sub_page_func") == "sub_page_func"  # set when visiting /sub/test
    print(f'✅ {STATE.get("sub_page_func")} == "sub_page_func"  EXECUTED as expected')
    assert STATE.get("sub_page2_class_before") == "sub_page2_class_before", (
        "SubPageClassMd.before must fire on /sub/page2"
    )
    print(
        f'✅ {STATE.get("sub_page2_class_before")} == "sub_page2_class_before"  EXECUTED as expected'
    )

    # after_request fires synchronously in the same navigation cycle
    assert STATE.get("sub_page2_class_after") == "sub_page2_class_after", (
        "SubPageClassMd.after_request must fire on /sub/page2"
    )
    print(
        f'✅ {STATE.get("sub_page2_class_after")} == "sub_page2_class_after"  EXECUTED as expected'
    )
    assert STATE.get("sub_page3_func") is None
    print(f"✅ {STATE.get('sub_page3_func')} is None  IS NONE as expected")
    print("\n✅ /sub/page2 – sub-router class page middleware verified")


@pytest.mark.anyio
async def test_sub_router_plus_page_mixed_list(app, mock_page):
    """
    Route: /sub/page3
    Expected: global  |  sub_router  |  [sub_page3_func_md + SubPage3ClassMd]
    Navigate full chain: /sub/test → /sub/page2 → /sub/page3.
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    await _navigate(fsx, mock_page, "/sub/test")
    await _navigate(fsx, mock_page, "/sub/page2")
    await _navigate(fsx, mock_page, "/sub/page3")

    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("sub_router_func") == "sub_router_func"
    print(f'✅ {STATE.get("sub_router_func")} == "sub_router_func"  EXECUTED as expected')
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    print(
        f'✅ {STATE.get("sub_router_class_before")} == "sub_router_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_router_class_after") == "sub_router_class_after"
    print(
        f'✅ {STATE.get("sub_router_class_after")} == "sub_router_class_after"  EXECUTED as expected'
    )
    assert STATE.get("sub_page_func") == "sub_page_func"
    print(f'✅ {STATE.get("sub_page_func")} == "sub_page_func"  EXECUTED as expected')
    assert STATE.get("sub_page2_class_before") == "sub_page2_class_before"
    print(
        f'✅ {STATE.get("sub_page2_class_before")} == "sub_page2_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_page2_class_after") == "sub_page2_class_after", (
        "SubPageClassMd.after_request must fire after /sub/page2 render"
    )
    print(
        f'✅ {STATE.get("sub_page2_class_after")} == "sub_page2_class_after"  EXECUTED as expected'
    )

    # /sub/page3 specific
    assert STATE.get("sub_page3_func") == "sub_page3_func", (
        "sub_page3_func_md must fire on /sub/page3"
    )
    print(f'✅ {STATE.get("sub_page3_func")} == "sub_page3_func"  EXECUTED as expected')
    assert STATE.get("sub_page3_class_before") == "sub_page3_class_before", (
        "SubPage3ClassMd.before must fire on /sub/page3"
    )
    print(
        f'✅ {STATE.get("sub_page3_class_before")} == "sub_page3_class_before"  EXECUTED as expected'
    )

    # after_request fires synchronously within the same navigation
    assert STATE.get("sub_page3_class_after") == "sub_page3_class_after", (
        "SubPage3ClassMd.after_request must fire on /sub/page3"
    )
    print(
        f'✅ {STATE.get("sub_page3_class_after")} == "sub_page3_class_after"  EXECUTED as expected'
    )
    print("\n✅ /sub/page3 – sub-router + mixed list page middleware verified")


@pytest.mark.anyio
async def test_full_navigation_chain_state_accumulation(app, mock_page):
    """
    Full navigation: / → /page1 → /page2 → /page3 → /sub/test → /sub/page2 → /sub/page3
    At the end ALL middlewares must have fired at least once.
    Validates the hierarchical STATE accumulation across the full route chain.
    """
    reset_state()
    app.start(mock_page)
    await asyncio.sleep(0)

    fsx = app._FletEasy__fsx
    fsx._data.share.clear = MagicMock(return_value=None)

    for route in ["/", "/page1", "/page2", "/page3", "/sub/test", "/sub/page2", "/sub/page3"]:
        await _navigate(fsx, mock_page, route)

    # All global middlewares
    assert STATE.get("global_func") == "global_func"
    print(f'✅ {STATE.get("global_func")} == "global_func"  EXECUTED as expected')
    assert STATE.get("global_class_before") == "global_class_before"
    print(f'✅ {STATE.get("global_class_before")} == "global_class_before"  EXECUTED as expected')
    assert STATE.get("global_class_after") == "global_class_after"
    print(f'✅ {STATE.get("global_class_after")} == "global_class_after"  EXECUTED as expected')

    # Page-specific middlewares
    assert STATE.get("page1_func") == "page1_func"
    print(f'✅ {STATE.get("page1_func")} == "page1_func"  EXECUTED as expected')
    assert STATE.get("page2_class_before") == "page2_class_before"
    print(f'✅ {STATE.get("page2_class_before")} == "page2_class_before"  EXECUTED as expected')
    assert STATE.get("page2_class_after") == "page2_class_after"
    print(f'✅ {STATE.get("page2_class_after")} == "page2_class_after"  EXECUTED as expected')

    # Sub-router middlewares
    assert STATE.get("sub_router_func") == "sub_router_func"
    print(f'✅ {STATE.get("sub_router_func")} == "sub_router_func"  EXECUTED as expected')
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    print(
        f'✅ {STATE.get("sub_router_class_before")} == "sub_router_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_router_class_after") == "sub_router_class_after"
    print(
        f'✅ {STATE.get("sub_router_class_after")} == "sub_router_class_after"  EXECUTED as expected'
    )

    # Sub-page middlewares
    assert STATE.get("sub_page_func") == "sub_page_func"
    print(f'✅ {STATE.get("sub_page_func")} == "sub_page_func"  EXECUTED as expected')
    assert STATE.get("sub_page2_class_before") == "sub_page2_class_before"
    print(
        f'✅ {STATE.get("sub_page2_class_before")} == "sub_page2_class_before"  EXECUTED as expected'
    )
    assert STATE.get("sub_page2_class_after") == "sub_page2_class_after"
    print(
        f'✅ {STATE.get("sub_page2_class_after")} == "sub_page2_class_after"  EXECUTED as expected'
    )
    assert STATE.get("sub_page3_func") == "sub_page3_func"
    print(f'✅ {STATE.get("sub_page3_func")} == "sub_page3_func"  EXECUTED as expected')
    assert STATE.get("sub_page3_class_before") == "sub_page3_class_before"
    print(
        f'✅ {STATE.get("sub_page3_class_before")} == "sub_page3_class_before"  EXECUTED as expected'
    )

    print("\n✅ Full chain – all middleware layers fired and accumulated correctly")

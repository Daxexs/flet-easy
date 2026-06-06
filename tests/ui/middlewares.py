import asyncio
import logging
from typing import Any

import flet as ft

import flet_easy as fs

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

app = fs.FletEasy(route_init="/", logger=True)

# Use a global dictionary to track middleware executions simply and synchronously
STATE: dict[str, Any] = {}


def update_state(key: str, value: Any):
    """Update the global state.
    The value parameter is mandatory and can be any type (int, str, etc.)
    """
    STATE[key] = value


def get_middleware_dashboard():
    """Returns a list of Text controls representing the current status of all middlewares."""
    keys = [
        "global_func",
        "global_class_before",
        "global_class_after",
        "page1_func",
        "page2_class_before",
        "page2_class_after",
        "sub_router_func",
        "sub_router_class_before",
        "sub_router_class_after",
        "sub_page_func",
        "sub_page2_class_before",
        "sub_page2_class_after",
        "sub_page3_func",
        "sub_page3_class_before",
        "sub_page3_class_after",
    ]

    controls = [ft.Text("--- Middleware Status Dashboard ---", weight="bold", size=16)]
    for key in keys:
        val = STATE.get(key)
        color = "green" if val is not None else "red"
        controls.append(ft.Text(f"{key}: {val}", color=color, font_family="monospace"))

    return controls


# --- Middlewares Definition ---


# 1. Global Functional Middleware
async def global_func_md(data: fs.Datasy):
    update_state("global_func", "global_func")
    print(f"-> global_func_md executed for {data.page.route}")


# 2. Global Class Middleware
class GlobalClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("global_class_before", "global_class_before")
        print(f"-> GlobalClassMd.before_request executed for {self.data.page.route}")

    async def after_request(self):
        update_state("global_class_after", "global_class_after")
        print(f"<- GlobalClassMd.after_request executed for {self.data.page.route}")


# 3. Page Functional Middleware (used in /page1)
async def page1_func_md(data: fs.Datasy):
    update_state("page1_func", "page1_func")
    print(f"  -> page1_func_md executed for {data.page.route}")


# 4. Page Class Middleware (used in /page2)
class Page2ClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("page2_class_before", "page2_class_before")
        print(f"  -> Page2ClassMd.before_request executed for {self.data.page.route}")

    async def after_request(self):
        update_state("page2_class_after", "page2_class_after")
        print(f"  <- Page2ClassMd.after_request executed for {self.data.page.route}")


# 5. AddPagesy Modular Functional Middleware (Sub-router)
async def sub_router_md(data: fs.Datasy):
    update_state("sub_router_func", "sub_router_func")
    print(f"    -> sub_router_md (AddPagesy) executed for {data.page.route}")


# 6. AddPagesy Modular Class Middleware (Sub-router)
class SubRouterClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_router_class_before", "sub_router_class_before")
        print(f"    -> SubRouterClassMd.before_request executed for {self.data.page.route}")

    async def after_request(self):
        update_state("sub_router_class_after", "sub_router_class_after")
        print(f"    <- SubRouterClassMd.after_request executed for {self.data.page.route}")


# 7. Sub-page specific functional middleware (used in /sub/test)
async def sub_page_func_md(data: fs.Datasy):
    update_state("sub_page_func", "sub_page_func")
    print(f"      -> sub_page_func_md executed for {data.page.route}")


# 8. Sub-page specific class middleware (used in /sub/page2)
class SubPageClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_page2_class_before", "sub_page2_class_before")
        print(f"      -> SubPageClassMd.before_request executed for {self.data.page.route}")

    async def after_request(self):
        update_state("sub_page2_class_after", "sub_page2_class_after")
        print(f"      <- SubPageClassMd.after_request executed for {self.data.page.route}")


# 9. Sub-page 3 specific functional middleware (used in /sub/page3)
async def sub_page3_func_md(data: fs.Datasy):
    update_state("sub_page3_func", "sub_page3_func")
    print(f"      -> sub_page3_func_md executed for {data.page.route}")


# 10. Sub-page 3 specific class middleware (used in /sub/page3)
class SubPage3ClassMd(fs.MiddlewareRequest):
    async def before_request(self):
        update_state("sub_page3_class_before", "sub_page3_class_before")
        print(f"      -> SubPage3ClassMd.before_request executed for {self.data.page.route}")

    async def after_request(self):
        update_state("sub_page3_class_after", "sub_page3_class_after")
        print(f"      <- SubPage3ClassMd.after_request executed for {self.data.page.route}")


# Add global middlewares
app.add_middleware(global_func_md, GlobalClassMd)

# --- Sub-router (AddPagesy) ---
sub = fs.AddPagesy(route_prefix="/sub", middleware=[sub_router_md, SubRouterClassMd])


@sub.page("/test", title="Sub Page", middleware=sub_page_func_md)
async def sub_page(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") == "page2_class_before"
    assert STATE.get("page2_class_after") == "page2_class_after"
    assert STATE.get("sub_router_func") == "sub_router_func"
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    assert STATE.get("sub_router_class_after") is None
    # Sub pages
    assert STATE.get("sub_page_func") == "sub_page_func"  # This page
    assert STATE.get("sub_page2_class_before") is None
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # End
    data.page.run_task(go_to, data, "/sub/page2")

    return ft.View(
        controls=[
            ft.Text(
                "Sub-router: ✅ All layers (Global + Sub-router + Page [func]) executed",
                size=20,
                color="green",
            ),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /sub/page2 in 1.5s...", weight="bold"),
        ]
    )


@sub.page("/page2", title="Sub Page 2", middleware=[SubPageClassMd])
async def sub_page2(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") == "page2_class_before"
    assert STATE.get("page2_class_after") == "page2_class_after"
    assert STATE.get("sub_router_func") == "sub_router_func"
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    assert (
        STATE.get("sub_router_class_after") == "sub_router_class_after"
    )  # Executed after /sub/test
    # Sub pages
    assert STATE.get("sub_page_func") == "sub_page_func"
    assert STATE.get("sub_page2_class_before") == "sub_page2_class_before"  # This page
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # End
    data.page.run_task(go_to, data, "/sub/page3")

    return ft.View(
        controls=[
            ft.Text("Sub-router Page 2: ✅ Page Class Middleware executed", size=20, color="green"),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /sub/page3 in 1.5s...", weight="bold"),
        ]
    )


@sub.page("/page3", title="Sub Page 3", middleware=[sub_page3_func_md, SubPage3ClassMd])
async def sub_page3(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") == "page2_class_before"
    assert STATE.get("page2_class_after") == "page2_class_after"
    assert STATE.get("sub_router_func") == "sub_router_func"
    assert STATE.get("sub_router_class_before") == "sub_router_class_before"
    assert (
        STATE.get("sub_router_class_after") == "sub_router_class_after"
    )  # Executed after /sub/page2
    # Sub pages
    assert STATE.get("sub_page_func") == "sub_page_func"
    assert STATE.get("sub_page2_class_before") == "sub_page2_class_before"
    assert (
        STATE.get("sub_page2_class_after") == "sub_page2_class_after"
    )  # Executed after /sub/page2
    assert STATE.get("sub_page3_func") == "sub_page3_func"  # This page
    assert STATE.get("sub_page3_class_before") == "sub_page3_class_before"  # This page
    assert STATE.get("sub_page3_class_after") is None

    # End
    data.page.run_task(close_app, data.page)

    return ft.View(
        controls=[
            ft.Text(
                "Sub-router Page 3: ✅ List of Middlewares (Func + Class) executed",
                size=20,
                color="green",
            ),
            *get_middleware_dashboard(),
            ft.Text("All checks passed. Closing app...", weight="bold"),
        ]
    )


app.add_pages(sub)


# --- Helper to auto-navigate ---
async def go_to(data: fs.Datasy, route: str):
    await asyncio.sleep(1.5)
    data.go_route(route)


async def close_app(page: ft.Page):
    await asyncio.sleep(2)
    await page.window.close()


# --- Pages ---


@app.page("/", title="Home")
async def home(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") is None
    assert STATE.get("page1_func") is None
    assert STATE.get("page2_class_before") is None
    assert STATE.get("page2_class_after") is None
    assert STATE.get("sub_router_func") is None
    assert STATE.get("sub_router_class_before") is None
    assert STATE.get("sub_router_class_after") is None
    assert STATE.get("sub_page_func") is None
    assert STATE.get("sub_page2_class_before") is None
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # Auto-navigate to /page1
    data.page.run_task(go_to, data, "/page1")

    return ft.View(
        controls=[
            ft.Text("Home: ✅ Initial page loaded", size=20, color="blue"),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /page1 in 1.5s..."),
        ]
    )


@app.page("/page1", title="Page 1", middleware=page1_func_md)
async def page1(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") is None
    assert STATE.get("page2_class_after") is None
    assert STATE.get("sub_router_func") is None
    assert STATE.get("sub_router_class_before") is None
    assert STATE.get("sub_router_class_after") is None
    assert STATE.get("sub_page_func") is None
    assert STATE.get("sub_page2_class_before") is None
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # Auto-navigate to /page2
    data.page.run_task(go_to, data, "/page2")

    return ft.View(
        controls=[
            ft.Text("Page 1: ✅ Page 1 Func Middleware executed", size=20, color="blue"),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /page2 in 1.5s..."),
        ]
    )


@app.page("/page2", title="Page 2", middleware=[Page2ClassMd])
async def page2(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") == "page2_class_before"
    assert STATE.get("page2_class_after") is None
    assert STATE.get("sub_router_func") is None
    assert STATE.get("sub_router_class_before") is None
    assert STATE.get("sub_router_class_after") is None
    assert STATE.get("sub_page_func") is None
    assert STATE.get("sub_page2_class_before") is None
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # Auto-navigate to /page3
    data.page.run_task(go_to, data, "/page3")

    return ft.View(
        controls=[
            ft.Text("Page 2: ✅ Page 2 Class Middleware executed", size=20, color="blue"),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /page3 in 1.5s..."),
        ]
    )


@app.page("/page3", title="Page 3", middleware=[page1_func_md, Page2ClassMd])
async def page3(data: fs.Datasy):
    # ALL Asserts
    assert STATE.get("global_func") == "global_func"
    assert STATE.get("global_class_before") == "global_class_before"
    assert STATE.get("global_class_after") == "global_class_after"
    assert STATE.get("page1_func") == "page1_func"
    assert STATE.get("page2_class_before") == "page2_class_before"
    assert STATE.get("page2_class_after") == "page2_class_after"
    assert STATE.get("sub_router_func") is None
    assert STATE.get("sub_router_class_before") is None
    assert STATE.get("sub_router_class_after") is None
    assert STATE.get("sub_page_func") is None
    assert STATE.get("sub_page2_class_before") is None
    assert STATE.get("sub_page2_class_after") is None
    assert STATE.get("sub_page3_func") is None
    assert STATE.get("sub_page3_class_before") is None
    assert STATE.get("sub_page3_class_after") is None

    # Auto-navigate to /sub/test
    data.page.run_task(go_to, data, "/sub/test")

    return ft.View(
        controls=[
            ft.Text(
                "Page 3: ✅ Multiple page middlewares supported!",
                size=20,
                color="blue",
            ),
            *get_middleware_dashboard(),
            ft.Text("Navigating to /sub/test in 1.5s..."),
        ]
    )


# Start the application
app.run()

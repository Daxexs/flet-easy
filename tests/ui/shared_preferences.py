import asyncio

import flet as ft

import flet_easy as fs

app = fs.FletEasy(route_init="/", logger=True)  # logger=True for debugging


async def go_test(route: str, data: fs.Datasy) -> None:
    await asyncio.sleep(2)
    data.go_route(route)


async def close_app(page: ft.Page):
    await asyncio.sleep(2)
    print("✅ close app - tests shared_preferences.py success!")
    await page.window.close()


@app.page("/", title="test")
async def test_page(data: fs.Datasy):
    page = data.page

    shared_preferences = hasattr(ft, "SharedPreferences")

    # reset all data
    if shared_preferences:
        await page.shared_preferences.clear()
        await ft.SharedPreferences().clear()
        await data.share.clear()
    else:
        # compatibility with flet 0.28.0 <= flet < 0.80.0
        data.share.clear()

    if shared_preferences:
        # class SharedPreferences is deprecated since version 0.80.0 and will be removed in version 0.90.0. Use SharedPreferences() instead.
        await ft.SharedPreferences().set("Shared", "1")

        # class SessionStorage is deprecated since version 0.80.0 and will be removed in version 0.90.0. Use SharedPreferences() instead.
        await page.shared_preferences.set("page-shared_preferences", "1")

        # Use SharedPreferencesEdit to shared data between pages, and the data will be cleared when the page is closed.
        await data.share.set("data-shared", "1")

    else:
        # compatibility with flet 0.28.0 <= flet < 0.80.0
        data.share.set("data-shared", "1")

    # go route /test in automatic

    data.page.run_task(go_test, "/test", data)

    return ft.View(
        controls=[
            ft.Text("Hello"),
            ft.Row(
                [
                    ft.Text("Shared = 1"),
                    ft.TextField(value=await ft.SharedPreferences().get("Shared")),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("page-shared_preferences = 1"),
                    ft.TextField(
                        value=await page.shared_preferences.get("page-shared_preferences")
                    ),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("data-shared = 1"),
                    ft.TextField(value=await data.share.get("data-shared"))
                    if shared_preferences
                    else ft.TextField(value=data.share.get("data-shared")),
                ]
            ),
            ft.Button("go test 2", on_click=data.go("/test")),
        ]
    )


@app.page("/test", title="test 2")
async def test_page2(data: fs.Datasy):
    page = data.page
    shared_preferences = hasattr(ft, "SharedPreferences")

    if shared_preferences:
        # it should always work with shared_data set to True or False
        assert await ft.SharedPreferences().get("Shared") == "1", (
            "SharedPreferences - It must be saved on all pages"
        )

        # it should always work with shared_data set to True or False
        assert await page.shared_preferences.get("page-shared_preferences") == "1", (
            "page-shared_preferences It must be saved on all pages"
        )

        assert await data.share.get("data-shared") is None, (
            "data-shared should be shared between pages and cleared when the page is closed"
        )

        # send the value of data.share.get("data-shared") to route /test3
        await data.share.set("data-shared-2", "1")
    else:
        # compatibility with flet 0.28.0 <= flet < 0.80.0
        assert data.share.get("data-shared") is None, (
            "data-shared should be shared between pages and cleared when the page is closed"
        )
        # send the value of data.share.get("data-shared") to route /test3
        data.share.set("data-shared-2", "1")

    data.page.run_task(go_test, "/test3", data)

    return ft.View(
        controls=[
            ft.Text("Hello"),
            ft.Row(
                [
                    ft.Text("Shared = 1"),
                    ft.TextField(value=await ft.SharedPreferences().get("Shared")),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("page-shared_preferences = 1"),
                    ft.TextField(
                        value=await page.shared_preferences.get("page-shared_preferences")
                    ),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("data-shared = None"),
                    ft.TextField(
                        value=await data.share.get("data-shared")
                        if shared_preferences
                        else data.share.get("data-shared")
                    ),
                ]
            ),
            ft.Button("go test 3", on_click=data.go("/")),
        ]
    )


@app.page("/test3", title="test 3", share_data=True)
async def test_page3(data: fs.Datasy):
    page = data.page

    shared_preferences = hasattr(ft, "SharedPreferences")

    if shared_preferences:
        # it should always work with shared_data set to True or False
        assert await ft.SharedPreferences().get("Shared") == "1", (
            "SharedPreferences - It must be saved on all pages"
        )

        # it should always work with shared_data set to True or False
        assert await page.shared_preferences.get("page-shared_preferences") == "1", (
            "page-shared_preferences It must be saved on all pages"
        )

        # @app.page("/test2", title="test 2", share_data=False) -  if share_data=False,     data.share.get("data-shared") will be None
        assert await data.share.get("data-shared-2") == "1", (
            "data-shared should be shared between pages and cleared when the page is     closed"
        )

    else:
        # @app.page("/test2", title="test 2", share_data=False) -  if share_data=False,     data.share.get("data-shared") will be None
        assert data.share.get("data-shared-2") == "1", (
            "data-shared should be shared between pages and cleared when the page is     closed"
        )

    # close the app
    page.run_task(close_app, page)

    return ft.View(
        controls=[
            ft.Text("Hello"),
            ft.Row(
                [
                    ft.Text("Shared = 1"),
                    ft.TextField(value=await ft.SharedPreferences().get("Shared")),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("page-shared_preferences = 1"),
                    ft.TextField(
                        value=await page.shared_preferences.get("page-shared_preferences")
                    ),
                ]
                if shared_preferences
                else []
            ),
            ft.Row(
                [
                    ft.Text("data-shared = 1"),
                    ft.TextField(
                        value=await data.share.get("data-shared-2")
                        if shared_preferences
                        else data.share.get("data-shared-2")
                    ),
                ]
            ),
            ft.Button("go test", on_click=data.go("/")),
        ]
    )


app.run()

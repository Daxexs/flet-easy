# Home

[![github](https://img.shields.io/badge/my_profile-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Daxexs)
[![pypi](https://img.shields.io/badge/Pypi-0A66C2?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/flet-easy)
[![Downloads](https://static.pepy.tech/badge/flet-easy)](https://pepy.tech/project/flet-easy) [![socket](https://socket.dev/api/badge/pypi/package/flet-easy/0.2.2#1725204521828)](https://socket.dev/pypi/package/flet-easy)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

<div align="center">
    <img src="assets/images/logo.png" alt="logo" width="250">
</div>

Flet-Easy is a user-friendly add-on package for Flet, offering a cleaner code structure with numerous customizable features like routers, decorators, route protection and more.

---

## Changelog

??? info "New features"
    # **v0.2.0**

    * Optimize code for `flet>=0.21`.
    * Fix async.
    * Automatic routing. [`[See more]`](/flet-easy/0.2.0/add-pages/in-automatic/)
    * Add the `title` parameter to the `page` decorator. [`[See more]`](/flet-easy/0.2.0/how-to-use/#example_1)
    * Add `JWT` support for authentication sessions in the data parameter. [`[See more]`](/flet-easy/0.2.0/basic-JWT/)
    * Add a `Cli` to create a project structure based on the MVC design pattern. [`[See more]`](/flet-easy/0.2.0/cli-to-create-app/)
    * Middleware Support. [`[See more]`](/flet-easy/0.2.0/middleware/)
    * Add more simplified Ref control. [`[See more]`](/flet-easy/0.2.0/ref/)
    * Enhanced Documentation.
    * Ruff Integration.

    ## **Changes in the api:**
    * The `async` methods have been removed, as they are not necessary.   
    * Change `update_login` method to `login` of Datasy. [`[See more]`](/flet-easy/0.2.0/customized-app/route-protection/#login)
    * Change `logaut` method to `logout` of Datasy. [`[See more]`](/flet-easy/0.2.0/customized-app/route-protection/#logout)
    * Changed function parameter decorated on `login` | `(page:ft.Page -> data:fs:Datasy)` [`[See more]`](/flet-easy/0.2.0/customized-app/route-protection/)
    * Changed function parameter decorated on `config_event_handler` | `(page:ft.Page -> data:fs:Datasy)` [`[See more]`](/flet-easy/0.2.0/customized-app/events)

    # **0.2.1**

    * Fix page loading twice 

    # **v0.2.2**

    * Fix sensitivity in url with capital letters.
    * Fix 'back' button in dashboard page app bar not working.
    * Fix error caused by `Timeout waiting invokeMethod`.

    # **v0.2.4**

    * ⚡ The speed of the router is improved to more than twice as fast.
    * Ways to install Flet-Easy. [`[See more]`](/flet-easy/0.2.0/installation/)
    * Supporting the use of class to create a view. [`[See more]`](/flet-easy/0.2.0/add-pages/through-classes)versions. [`[See more]`](/flet-easy/0.2.0/add-pages/by-means-of-functions/#pagesy)
    * New more responsive fs `cli`. [`[See more]`](/flet-easy/0.2.0/cli-to-create-app/)
    * Now `page.go()` and `data.go()` work similarly to go to a page (`View`), the only difference isthat `data.go   ()` checks for url redirects when using `data.redirect()`. [`[See more]`](/flet-easy/0.2.0/how-to-use/#datasy-data)
    * Bug fixes found in previous changes.
    *New method added in Datasy (data) [`[See more]`](/flet-easy/0.2.0/how-to-use/#datasy-data)
        * `history_routes` : Get the history of the routes.
        * `go_back` : Method to go back to the previous route.
    
    # **v0.2.6**
    * Fix route error page 404. [`[See more]`](/flet-easy/0.2.0/customized-app/page-404/)
    * Add route checker without dependency. [`[See more]`](/flet-easy/0.2.0/dynamic-routes/)

    # **v0.2.7**
    * Fix error in non-dynamic routing. ([#30](https://github.com/Daxexs/flet-easy/issues/30))
    * Add page without creating an instance of `AddPagesy` class. ([#31](https://github.com/Daxexs/flet-easy/issues/31))

    # **v0.2.8**
    * Support for `Flet>=0.25.*`.
    * New methods to initialize and obtain by the application. [`[See more]`](/flet-easy/0.2.0/run-the-app/#use-flet-easy-in-an-existing-app)

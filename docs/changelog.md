# Flet-Easy changelog

## v0.3.0.dev26 (../05/26)

* **Package Reorganization:** Restructured the `flet-easy` package into logical subpackages (`core/`, `security/`, `ui/`) to improve maintainability, while preserving 100% backward compatibility for existing imports.

* **Core Refactoring:** Refactored `fletEasy.py` into `core/app.py`, extracting route-building logic, removing duplicate execution paths, and simplifying middleware handling.
* compatibility with `flet >= 0.27.*` (see [flet-easy/issues/51](https://github.com/Daxexs/flet-easy/issues/51))

* compatibility with `flet >= 0.80.*` witch change the api. (see [flet-easy/issues/51](https://github.com/Daxexs/flet-easy/issues/51))

* Optimize routes loading and middleware execution ([#40](https://github.com/Daxexs/flet-easy/issues/40))

* Fix for compatibility with Python 3.9 ([#47](https://github.com/Daxexs/flet-easy/issues/47))

* Improved and fixed error response when JWT libraries are not installed.

* Improved error handling for `login`, `login_async`, `decode`, and `decode_async` methods in `Datasy`. ([#50](https://github.com/Daxexs/flet-easy/issues/50))

### New features

* Support for rendering new Flet Declarative UI Components (`@ft.component`) as native routes, bridging URL parameters and `Datasy` seamlessly into declarative objects. (see [#51](https://github.com/Daxexs/flet-easy/issues/51)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/add-pages/through-decorators/#using-declarative-components-ftcomponent)] - [[Docs](https://daxexs.github.io/flet-easy/dev/guide/routing/declarative/)]

* Add support for using `@ft.component` gracefully directly on the `build()` method of class-based views. `Flet-Easy` will automatically instantiate the class and inject the `self.data` property, removing the need for an explicit `__init__(self, data: fs.Datasy)`. [[Docs](https://daxexs.github.io/flet-easy/dev/guide/add-pages/through-decorators/#using-declarative-components-ftcomponent)]

* **Backwards Compatibility**: Class-based views can now optionally define parameters in their `build` method, such as `def build(self, data: fs.Datasy):`. The router will dynamically inspect the signature and pass `data` and URL parameters if expected, making `data` truly optional while preserving compatibility with older codebases.

* Add Middlewares to `AddPagesy` ([#37](https://github.com/Daxexs/flet-easy/issues/37)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/add-pages/through-decorators/#middleware)]

* Add support for the middleware class in the add_middleware method of `FletEasy`. ([#38](https://github.com/Daxexs/flet-easy/issues/38)) [[Docs](https://daxexs.github.io/flet-easy/dev/advanced/middleware/#class-based-middleware)]

* Add support for the middleware class in the add_middleware method of `AddPagesy`. ([#38](https://github.com/Daxexs/flet-easy/issues/38)) [[Docs](https://daxexs.github.io/flet-easy/dev/advanced/middleware/#for-each-page)]

* Implement optional use of per-page cache ([#39](https://github.com/Daxexs/flet-easy/issues/39)) [[Docs](https://daxexs.github.io/flet-easy/dev/advanced/page-caching)]

* Add routing using `NavigationBar` ([#41](https://github.com/Daxexs/flet-easy/issues/41)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/routing/navigation/)]

* **Enhanced Page Return Support:** Greatly expanded the range of supported return types from `@app.page`-decorated functions and classes. While `ft.View` remains recommended, `flet-easy` now automatically manages and wraps the following:
  * `ft.Text`
  * `list[ft.Control]`
  * `str` (automatically wrapped in `ft.Text`)
  * `Class` with a `build()` method
  * Declarative Flet Components (`@ft.component`)

* **Flexible Page Signatures:** The `data: fs.Datasy` parameter is now optional in all page functions and class `build()` methods.

### Pagesy

* `index` : Define the index of the page, use in controls like `ft.NavigationBar` and `ft.CupertinoNavigationBar`. ([#41](https://github.com/Daxexs/flet-easy/issues/41)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/pagesy/#index)]

* `cache` : Boolean that preserves page state when navigating. Controls retain their values instead of resetting. (Optional) ([#39](https://github.com/Daxexs/flet-easy/issues/39)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/pagesy/#cache)]

### Datasy (data)

#### New methods

* `page_reload()` : Use this method to reload the page, restores the default values of the page. ([#49](https://github.com/Daxexs/flet-easy/issues/49)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#page_reload)]

* `dynamic_control()` : Adds dynamic control to the page, allowing real-time updates when caching is enabled on the page. ([#41](https://github.com/Daxexs/flet-easy/issues/41)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#dynamic_controlcontrol-func_update)]

* `go_navigation_bar()` : Handles navigation bar changes. Use this method in the on_change event of 'ft.NavigationBar' or 'ft.CupertinoNavigationBar' controls. ([#41](https://github.com/Daxexs/flet-easy/issues/41)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#go_navigation_bar-e)]

* `go_route(route: str)` : Use this method to navigate to a specific route. It executes directly, unlike the `data.go()` method, which returns a lambda function. ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#go_route-route)]

* `decode_jwt(key)`: Decode JWT synchronously from `Datasy` (Replaces `fs.decode()`). ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/advanced/basic-jwt/#decode_jwt)]

* `decode_jwt_async(key)`: Decode JWT asynchronously — preferred in `async` login decorators (Replaces `fs.decode_async()`). ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/advanced/basic-jwt/#decode_jwt_async)]

* `login_async(key: str, value: Any, next_route: str)`: Use this method to create a login session asynchronously. It registers the key and value in the client's storage.

* `confirm_pop(e: ViewPopEvent)`: Use this method to confirm a pop view event and seamlessly go back to the previous route in the history.

#### Changes in the api

* `login(key: str, value: Any, next_route: str)`: The `next_route` parameter is now mandatory. This ensures an immediate and safe redirection to the specified route (e.g., dashboard) right after registering the session.

* `go_back()`: Use this method to return to the previous path. The method is executed directly without returning a lambda function. ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#go_back)]

* `logout(key: str, next_route: str = None)`: Use this method to close all sessions on all devices or on the device currently in use, which was previously configured with the `login` method. The method executes directly without returning a lambda function. A new parameter, `next_route`, has also been included to redirect to a router other than the login router. ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#logoutkey-next_route)]

* `data.redirect(route: str)`: Use this method to redirect to a specific route. It executes directly, unlike the `data.go()` method. Method added available in functions decorated with `@page(...)`. ([#50](https://github.com/Daxexs/flet-easy/issues/50)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#redirect-route)]

* `go(route: str)`: Use this method to navigate to a specific route. It returns an asynchronous lambda function, unlike `go_route()`, which executes directly. This method is available in functions decorated with `@page(...)`. ([#50](https://github.com/Daxexs/flet-easy/issues/500)) [[Docs](https://daxexs.github.io/flet-easy/dev/guide/core/datasy/#go_route-route)]

* `data.share.set()`: Starting from version `0.80.*`, the `await` keyword is required as it now utilizes `SharedPreferences` by default.

* `cache`: Currently supported in imperative routing; declarative routing support is not yet available.

----

### Other changes

* **PEP 585 Modernization:** Standardized the entire codebase to use Python 3.9+ built-in generics (`dict`, `list`, `tuple`), eliminating deprecation warnings and future-proofing the library.
* **Core Logic Consolidation:** Deduplicated mission-critical methods in `router.py` and flattened the package structure for improved performance and maintainability.
* **Enhanced Compatibility:** Implemented robust fallback mechanisms for `RouteUrlStrategy`, `CupertinoAppBar`, and `CupertinoNavigationBar` to ensure 100% compatibility with Flet versions as old as 0.27.*.
* **Bug Fixes:** Resolved critical type errors, Flet version compatibility issues, `on_error` event logic, and declarative rendering bugs while adding safety guards for parameters and messages.

### Build & Testing

* **CI/CD Automation:** Refactored `noxfile.py` to use robust native parametrization instead of error-prone runtime combinations, improving pipeline stability and test coverage granularity across different environments.
* **Router Tests Expansion:** Created a robust test suite using Pytest covering key core functionalities:
  * **Routing:** Route handling and view generation for both imperative functions and declarative components (`@ft.component`).
  * **Sub-routers:** Proper registration and URL parameter inheritance using `AddPagesy`.
  * **Middlewares:** Execution, validation, and interception logic at both global and sub-router levels.
  * **Datasy & SharedPreferences:** Mocking and validation of session data, login flows, and shared preference interactions.
  * **Class-based Views:** Validation of optional `data` parameter injections and `build()` method behaviors.

----

## v0.2.9 (25/01/25)

### Bug fixes

* Fix error when using login() method in async function ([#34](https://github.com/Daxexs/flet-easy/issues/34))
* Fix and improve error message in fs.decode (async) ([#35](https://github.com/Daxexs/flet-easy/issues/35))

## v0.2.8 (21/12/24)

* Support for `Flet>=0.25.*`.
* Switching to `uv` as package manager.
* New methods to initialize and obtain by the application. ([#33](https://github.com/Daxexs/flet-easy/issues/33)) [[Docs](https://daxexs.github.io/flet-easy/0.2.0/run-the-app/#use-flet-easy-in-an-existing-app)]
* Update of the tests code for flet 0.25.*

## v0.2.7 (29/10/24)

* Fix error in non-dynamic routing. ([#30](https://github.com/Daxexs/flet-easy/issues/30)) [[Docs](https://daxexs.github.io/flet-easy/latest/add-pages/through-decorators/#without-instantiating-addpagesy)]
* Add page without creating an instance of `AddPagesy` class. ([#31](https://github.com/Daxexs/flet-easy/issues/31))

## 0.2.6 (19/10/24)

* Fix route error page 404. ([#28](https://github.com/Daxexs/flet-easy/issues/28))
* Add route checker without dependency. ([#29](https://github.com/Daxexs/flet-easy/issues/29))

## 0.2.4 (03/09/24)

* ⚡The speed of the router is improved to more than twice as fast. ([#20](https://github.com/Daxexs/flet-easy/issues/20))
  
* Ways to install Flet-Easy. ([#25](https://github.com/Daxexs/flet-easy/issues/25)) [[Doc](https://daxexs.github.io/flet-easy/0.2.4/installation/)]
  
* Add `go_back` method. ([#21](https://github.com/Daxexs/flet-easy/issues/21)) [[Doc](https://daxexs.github.io/flet-easy/0.2.4/how-to-use/#methods/)]
  
* Ruff configuration update (>=0.4.4) ([#22](https://github.com/Daxexs/flet-easy/issues/22))
  
* Supporting the use of class to create a view ([#24](https://github.com/Daxexs/flet-easy/issues/24)) [[Doc](https://daxexs.github.io/flet-easy/0.2.4/add-pages/through-classes/)]
  
* Bug fixes found in previous changes.
  
* Documentation improvements and updates. ([#26](https://github.com/Daxexs/flet-easy/issues/22)) [[view](https://daxexs.github.io/flet-easy/)]

### **Changes in the api:**

New method added in Datasy (data) [[Doc](https://daxexs.github.io/flet-easy/0.2.4/how-to-use/#datasy-data/)]

* `history_routes` : Get the history of the routes.
* `go_back` : Method to go back to the previous route.

### **Note**

* Now `page.go()` and `data.go()` work similarly to go to a page (View), the only difference is that `data.go()` checks for url redirects when using `data.redirect()`.
* The 'clear' parameter of `Pagesy` and the `page` decorator is deprecated, it will be removed in future versions.

### 0.2.2 (04/05/24)

* Fix sensitivity in url with capital letters ([#15](https://github.com/Daxexs/flet-easy/issues/15))
* Fix 'back' button in dashboard page app bar not working ([#18](https://github.com/Daxexs/flet-easy/issues/18))
* Fix error caused by `Timeout waiting invokeMethod` ([#19](https://github.com/Daxexs/flet-easy/issues/19))
  
### 0.2.1 (25/04/24)

* Fix page loading twice ([#14](https://github.com/Daxexs/flet-easy/issues/14))

### 0.2.0 (17/04/24)

* Optimize code for flet >0.21 ([#4](https://github.com/Daxexs/flet-easy/issues/4))

* Fix async.

* Automatic routing ([#11](https://github.com/Daxexs/flet-easy/issues/11)) [Docs](https://daxexs.github.io/flet-easy/0.2/Add-pages/In-automatic/)

* Add the `title` parameter to the `page` decorator ([#5](https://github.com/Daxexs/flet-easy/issues/5)) [Docs](https://daxexs.github.io/flet-easy/0.2/How-to-use/#example_1)

* Add `JWT` support for authentication sessions in the data parameter ([#6](https://github.com/Daxexs/flet-easy/issues/6)) [Docs](https://daxexs.github.io/flet-easy/0.2/Basic-JWT/)

* Add a `Cli` to create a project structure based on the MVC design pattern ([#7](https://github.com/Daxexs/flet-easy/issues/7)) [Docs](https://daxexs.github.io/flet-easy/0.2/CLI-to-create-app/)

* Middleware Support ([#9](https://github.com/Daxexs/flet-easy/issues/9)) [Docs](https://daxexs.github.io/flet-easy/0.2/Middleware/)

* Add more simplified Ref control ([commit](https://github.com/Daxexs/flet-easy/commit/907380ed56e646ffe3ec48b81d7b35a9385e5f5d))

* Enhanced Documentation ([commit](https://github.com/Daxexs/flet-easy/commit/a742e6790cf72f17c416147f899c74bcd512ab54))

* Ruff Integration ([commit](https://github.com/Daxexs/flet-easy/commit/9de267eb6601d6afb2757d90e5a26e51f2325f2e))

**Changes in the api:**

* The `async` methods have been removed, as they are not necessary.
  
* Change `update_login` method to `login` of Datasy. ([Docs](https://daxexs.github.io/flet-easy/0.2/Customized-app/Route-protection/#login))
  
* Change `logaut` method to `logout` of Datasy. ([Docs](https://daxexs.github.io/flet-easy/0.2/Customized-app/Route-protection/#logout))

* Changed function parameter decorated on `login` | `(page:ft.Page -> data:fs:Datasy)` ([Docs](https://daxexs.github.io/flet-easy/0.2/Customized-app/Route-protection/))

* Changed function parameter decorated on `config_event_handler` | `(page:ft.Page -> data:fs:Datasy)` ([Docs](https://daxexs.github.io/flet-easy/0.2/Customized-app/Events/))
  
### 0.1.3 (11/03/2024)

* Flet installation is required to use Flet-Easy.
* Fixed error when running the application with flet 0.21 ([#3](https://github.com/Daxexs/flet-easy/issues/3)).
* Fixed packing when compiling an apk ([#2](https://github.com/Daxexs/flet-easy/issues/2)).
  
### 0.1.1 (31/01/2024)

* Small improvements in the code and documentation.
* Parameter `proctect_route` changed to `protected_route` of `page` decorator ([Docs](https://daxexs.github.io/flet-easy/0.1.3/Customized-app/Route-protection/))
* Added functionality to share data between pages in a more controlled way ([Docs](https://daxexs.github.io/flet-easy/0.1.3/Data-sharing-between-pages/))
* Added a more ordered documentation ([Docs](https://daxexs.github.io/flet-easy/))

### 0.1.0

Initial commit

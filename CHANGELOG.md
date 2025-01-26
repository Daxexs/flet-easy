# Flet-Easy changelog

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

### **🔎Note**

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

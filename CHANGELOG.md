# Flet-Easy changelog

### 0.2.1 (25/04/24)
* Fix page loading twice ([#14](https://github.com/Daxexs/flet-easy/issues/14))

### 0.2.0 (17/04/24)
* Optimize code for flet >0.21 ([#4](https://github.com/Daxexs/flet-easy/issues/4))

* Fix async.

* Automatic routing ([#11](https://github.com/Daxexs/flet-easy/issues/11)) [Docs](https://daxexs.github.io/flet-easy/0.2/Add-pages/In-automatic/)

* Add the `title` parameter to the `page` decorator ([#5](https://github.com/Daxexs/flet-easy/issues/5)) [Docs](https://daxexs.github.io/flet-easy/0.2/How-to-use/#example_1)

* Add `JWT` support for authentication sessions in the data parameter ([#6](https://github.com/Daxexs/flet-easy/issues/6)) [Docs](https://daxexs.github.io/flet-easy/0.2/Basic-JWT/)

* Add a `Cli` to create a project structure based on the MVC design pattern ([#7](https://github.com/Daxexs/flet-easy/issues/7)) [Docs](https://daxexs.github.io/flet-easy/0.2/CLI-to-create-app/)

* Middleware Support ([#9](https://github.com/Daxexs/flet-easy/issues/9)) [Docs](https://daxexs.github.io/flet-easy/0.2/Midleware/)

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
To run the application we use an object method already instantiated by Flet-Easy, there are three ways to run the application (you can customize its method parameters as required):

!!! note
    Each method is used to what you want to use in the page globally, so you don't have problems with `page_update` and `page.update_async`.

* `run` **(normal)**
* `run_async` **(asynchronous)**
* `fastapi` **(asynchronous)** : Returns a value to be able to run the app, for more information on its attributes  [view](https://flet.dev/docs/guides/python/deploying-web-app/running-flet-with-fastapi#how-it-works)

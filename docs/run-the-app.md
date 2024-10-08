# Run the app

To run the application we use an object method already instantiated by [`FletEasy`](/flet-easy/0.1.0/how-to-use/#fleteasy) (you can customize the parameters of method according to your needs):

## Methods

### run

![FletEasy run](assets/images/v0.1.0/method_run.png "FletEasy run()")

### run_async

![FletEasy run](assets/images/v0.1.0/method_run_async.png "FletEasy run_async()")

### Use with fastapi

To get the main of the app and be able to add Fastapi to it.

![run fastapi](assets/images/v0.1.0/method_fastapi.png "run fastapi()")

## customize as it is executed

![run view](assets/images/run_view.png "run view")

!!! warning "If there are problems in `build web`"
    Use:
    ```python
    import flet as ft

    ft.app(app.fastapi())
    ```

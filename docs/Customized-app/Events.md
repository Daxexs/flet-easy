## Configure custom [events](https://flet.dev/docs/controls/page#events)
`config_event_handler` Decorator to add `Flet` event configurations -> [More information](https://flet.dev/docs/controls/page#events). The decorated function must receive the page parameter to be able to manipulate the app elements.

### **Example**
!!! example ""
    * Handle the event when the app is disconnected
  
```python hl_lines="1 6"
@app.config_event_handler
def event_handler(page: ft.Page):
    def on_disconnect(e):
        print("Disconnect test application")

    page.on_disconnect = on_disconnect
```

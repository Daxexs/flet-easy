# Events

## Configure custom [events](https://flet.dev/docs/controls/page#events)

`config_event_handler` Decorator to add [`Flet` event configurations](https://flet.dev/docs/controls/page#events). The decorated function must receive the [[data:Datasy](/flet-easy/0.2.0/how-to-use/#datasy-data)] parameter to be able to manipulate the app elements.

### **Example**

!!! example ""
    * Handle the event when the app is disconnected
  
```python hl_lines="1-2 8"
@app.config_event_handler
def event_handler(data: fs.Datasy):
    page = data.page

    def on_disconnect(e):
        print("Disconnect test application")

    page.on_disconnect = on_disconnect
```

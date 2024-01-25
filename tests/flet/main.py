import flet_easy as fs
from views.index import index
from views.counter import counter
from core.config import ConfigApp

app = fs.FletEasy(
    route_init="/home"
    )

app.add_pages([index, counter])
ConfigApp(app)

# We run the application
app.run()

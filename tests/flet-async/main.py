import flet_easy as fs
from views.index import index
from views.counter import counter

app = fs.FletEasy(route_prefix="/flet-easy", route_init="/flet-easy/home")

app.add_pages([index, counter])

# We run the applications
app.run_async()

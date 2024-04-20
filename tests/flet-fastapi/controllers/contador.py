from flet_core.constrained_control import ConstrainedControl
from flet_easy import Keyboardsy, Resizesy
from model import ModelTest


class ContadorC:
    def __init__(
        self,
        _self: ConstrainedControl,
        on_resize: Resizesy = None,
        on_keyboard: Keyboardsy = None,
    ) -> None:
        self.model = ModelTest()
        self.x = _self

    async def min(self, e):
        x = self.x
        x.numero.text = str(int(x.numero.text) - 1)
        print(self.model.test())
        await x.update_async()

    async def max(self, e):
        self.x.numero.text = str(int(self.x.numero.text) + 1)
        await self.x.update_async()

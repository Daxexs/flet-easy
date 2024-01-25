from flet_core.constrained_control import ConstrainedControl
from flet_easy import Controllersy, Resizesy, Keyboardsy
from model import ModelTest

class ContadorC(Controllersy):
    
    def __init__(self, _self: ConstrainedControl, on_resize: Resizesy = None, on_keyboard: Keyboardsy = None) -> None:
        super().__init__(_self, on_resize, on_keyboard)
        self.model = ModelTest()

    async def min(self,e):
        x = self.x
        x.numero.text = str(int(x.numero.text) - 1)
        print(self.model.test())
        await x.update_async()

    async def max(self,e):
        self.x.numero.text = str(int(self.x.numero.text) + 1)
        await self.x.update_async()
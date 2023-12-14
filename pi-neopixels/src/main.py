import asyncio
from functools import wraps
import time
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence

# from rpi_ws281x import Adafruit_NeoPixel
from typing_extensions import Self
from viam.components.generic import Generic
from viam.logging import getLogger
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.resource.types import Model, ModelFamily
from viam.module.module import Module

import time
# import board
# import busio
# from rainbowio import colorwheel
# from adafruit_seesaw import seesaw, neopixel

LOGGER = getLogger(__name__)


class Neopixel(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "pi-neopixels")

    def __init__(self, name: str):
        super().__init__(name)
        # self.i2c = busio.I2C(board.SCL, board.SDA)
        # self.ss = seesaw.Seesaw(i2c, addr=0x60)
        # self.neo_pin = 15
        # self.num_pixels = 64
        # self.pixels = neopixel.NeoPixel(ss, neo_pin, num_pixels, brightness = 0.1)
        # self.color_offset = 0
        
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        result = {}
        LOGGER.info(f"received {command=}.")
        print("neopixel.py do_command reached")
        # for name, args in command.items():
        #     if name == "test":
        #         for j in range(255):
        #             for i in range(self.num_pixels):
        #                 rc_index = (i * 256 // self.num_pixels) + color_offset
        #                 await self.set_pixel_color(i, colorwheel(rc_index & 255))
        #             await self.show()
        #             color_offset += 1
        #             time.sleep(0.01)
        #         result[name] = True
        #     if name == "set_pixel_color":
        #         await self.set_pixel_color(*args)
        #         result[name] = True
        #     if name == "show":
        #         await self.show()
        #         result[name] = True
        return result

    # async def set_pixel_color(self, i, color):
    #     self.pixels[i] = colorwheel(rc_index & 255)

    # async def show(self):
    #     self.pixels.show()
    
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        module = cls(config.name)
        module.reconfigure(config, dependencies)
        return module
    
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        pass

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        print("neopixel.py validate_config reached")
        return []
    
async def main():
    """This function creates and starts a new module, after adding all desired resource models.
    Resource creators must be registered to the resource registry before the module adds the resource model.
    """
    Registry.register_resource_creator(Generic.SUBTYPE, Neopixel.MODEL, ResourceCreatorRegistration(Neopixel.new, Neopixel.validate_config))

    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, Neopixel.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())

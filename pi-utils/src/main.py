import asyncio
from functools import wraps
import time, os
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
LOGGER = getLogger(__name__)


class PiUtils(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "pi-utils")

    def __init__(self, name: str):
        super().__init__(name)
        
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        result = {}
        LOGGER.info(f"received {command=}.")
        print("pi-utils do_command reached")
        
        if "get_temp" in command:
            temp = await self.get_temp()
            result["temp"] = temp
        
        return result

    async def get_temp(self):
        temp = os.popen("vcgencmd measure_temp").readline()
        return temp.replace("temp=", "").replace("'C", "").strip()
            
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
        LOGGER.info("pi-utils reconfigure reached")
        pass

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        LOGGER.info("pi-utils validate_config reached")
        return []
    
async def main():
    """This function creates and starts a new module, after adding all desired resource models.
    Resource creators must be registered to the resource registry before the module adds the resource model.
    """
    Registry.register_resource_creator(Generic.SUBTYPE, PiUtils.MODEL, ResourceCreatorRegistration(PiUtils.new, PiUtils.validate_config))

    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, PiUtils.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())

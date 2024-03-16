from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self
from typing import Final

from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

# from ..service_base import ServiceBase

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.generic import Generic
from viam.logging import getLogger
from viam.utils import ValueTypes

import time
import asyncio

import paho.mqtt.client as mqtt

LOGGER = getLogger(__name__)

class mqttService(Generic, Reconfigurable):
    
    """
    Generic service, which represents any type of service that can execute arbitrary commands
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "mqtt-service")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    url: str
    client: mqtt.Client

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        url = config.attributes.fields['url'].string_value
        if url == "":
            raise Exception("A URL must be defined")
        return

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.url = str(config.attributes.fields['url'].string_value)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)    
        try:
            self.client.connect(self.url, 1883, 60)  # Connect to your MQTT broker
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            # Handle the exception as appropriate for your application
        return
    
    async def do_command(
                self,
                command: Mapping[str, ValueTypes],
                *,
                timeout: Optional[float] = None,
                **kwargs
            ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        
        for (name, args) in command.items():
            if name == 'publish':
                topic = command["publish"]["topic"]
                message = command["publish"]["message"]
                self.client.publish(topic, message)
                result[name] = True
            elif "subscribe" in command:
                await self.subscribe(command[name]["topic"], command[name]["method"])
                result[name] = True
        
        return result
    
    async def subscribe(self, topic, method):
        """ Pass the topic and the method to be called when a message is received
            method should be a function that takes 3 arguments, client, userdata and message
        """
        self.client.subscribe(topic)
        self.client.message_callback_add(topic, method)
        self.client.loop_start()
        return self.client
    
    from typing import Final

from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

# from ..service_base import ServiceBase


# class Generic(ServiceBase):
#     """
#     Generic service, which represents any type of service that can execute arbitrary commands

#     This acts as an abstract base class for any drivers representing generic services.
#     This cannot be used on its own. If the ``__init__()`` function is overridden, it must call the ``super().__init__()`` function.

#     To create a Generic service (an arbitrary service that can process commands), this ``Generic`` service should be subclassed
#     and the ``do_command`` function implemented.

#     Example::

#         class ComplexService(Generic):

#             async def do_command(
#                 self,
#                 command: Mapping[str, ValueTypes],
#                 *,
#                 timeout: Optional[float] = None,
#                 **kwargs
#             ) -> Mapping[str, ValueTypes]:
#                 result = {key: False for key in command.keys()}
#                 for (name, args) in command.items():
#                     if name == 'set_val':
#                         self.set_val(*args)
#                         result[name] = True
#                     if name == 'get_val':
#                         result[name] = self.val
#                     if name == 'complex_command':
#                         self.complex_command(*args)
#                         result[name] = True
#                 return result

#             def set_val(self, val: int):
#                 self.val = val

#             def complex_command(self, arg1, arg2, arg3):
#                 ...

#     To execute commands, simply call the ``do_command`` function with the appropriate parameters.
#     ::

#         await service.do_command({'set_val': 10})
#         service.val  # 10
#         await service.do_command({'set_val': 5})
#         service.val  # 5
#     """

#     SUBTYPE: Final = Subtype(  # pyright: ignore [reportIncompatibleVariableOverride]
#         RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, "generic"
#     )


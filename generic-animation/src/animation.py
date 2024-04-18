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
from pubsub_python import Pubsub

import time
import asyncio
import json
import os.path
from time import sleep

LOGGER = getLogger(__name__)


class animation(Generic, Reconfigurable):
    
    """
    Generic service, which represents any type of service that can execute arbitrary commands
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "animation")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    # some_pin: int
    path: str
    mqtt: Pubsub

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
        # some_pin = config.attributes.fields["some_pin"].number_value
        # if some_pin == "":
            # raise Exception("A some_pin must be defined")
        path = config.attributes.fields['path'].string_value
        if path == "":
            raise Exception("A path must be defined")
        mqtt = config.attributes.fields["mqtt"].string_value
        if mqtt == "":
            raise Exception("mqtt service must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        # self.some_pin = int(config.attributes.fields["some_pin"].number_value)
        self.path = str(config.attributes.fields['path'].string_value)
        # pub.subscribe(self.animate, "animate")
        
        
        mqtt = config.attributes.fields["mqtt"].string_value
        actual_mqtt = dependencies[Pubsub.get_resource_name(mqtt)]
        self.mqtt = cast(Pubsub, actual_mqtt)
        LOGGER.info('[ANIMATION] MQTT service defined')
        
        def mqttSend(msg: str):
            LOGGER.info('[ANIMATION] mqttSend')
            LOGGER.info('[ANIMATION] ' + str(msg))
            deserialized_json = eval(msg)
            LOGGER.info('[ANIMATION] ' + str(deserialized_json.get('action')))
            asyncio.ensure_future(self.animate(deserialized_json.get('action')))
        
        async def sub():
            await self.mqtt.subscribe("animation/send", mqttSend)

        asyncio.ensure_future(sub())
        
        LOGGER.info('[ANIMATION] Subscribed to MQTT topic')
        
        return

    """ Implement the methods the Viam RDK defines for the Generic API (rdk:service:generic) """
    
    async def do_command(
                self,
                command: Mapping[str, ValueTypes],
                *,
                timeout: Optional[float] = None,
                **kwargs
            ) -> Mapping[str, ValueTypes]:
                result = {key: False for key in command.keys()}
                for (name, args) in command.items():
                    if name == 'animate':
                        result[name] = await self.animate(*args)
                return result

    async def animate(self, action):
        """
        Move pan and tilt servos in sequence defined by given file
        :param filename: animation file in path specified in init
        """
        LOGGER.info('[ANIMATION] animate')
        file = self.path + action + '.json'
        if not os.path.isfile(file):
            raise ValueError('Animation does not exist: ' + file)
        
        with open(file, 'r') as f:
            parsed = json.load(f)
            
        #list of instructions
        instructions = []
        
        # async def pub():
        #     await asyncio.sleep(1)
        #     await self.mqtt.publish("test/topic", "test message", 0)

        # asyncio.ensure_future(pub())
        
        for step in parsed:
            LOGGER.info('[ANIMATION] ' + str(step.keys()) + ' ' + str(step.values()))
            cmd = list(step.keys())[0]
            args = list(step.values())
            if 'servo:' in cmd:
                split = cmd.split(':')
                type = 'servo' if split[2] == 'mvabs' else 'servo_relative'
                args = {
                        'type': type,
                        'identifier': split[1],
                        'message': list(step.values())[0]
                    }
                await self.mqtt.publish('serial/send', str(args), 0)
                instructions.append((cmd, args))
            elif 'sleep' == cmd:
                sleep(args[0])
            elif 'animate' == cmd:
                await self.mqtt.publish('animate/send', str(args), 0)
            elif 'led:' in cmd:
                await self.mqtt.publish('led/send', str(args), 0)
            elif 'speak' == cmd:
                await self.mqtt.publish('speak/send', str(args), 0)
            elif 'pin' in cmd:
                await self.mqtt.publish('pin/read', str(args), 0)
        return instructions

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


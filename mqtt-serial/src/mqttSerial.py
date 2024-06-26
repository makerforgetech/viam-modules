from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self
from typing import Final

from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.generic import Generic
from viam.logging import getLogger
from pubsub_python import Pubsub

import time
import asyncio

from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_i16, read_i32, read_order
from robust_serial.utils import open_serial_port

LOGGER = getLogger(__name__)

class mqttSerial(Generic, Reconfigurable):
    
    """
    Generic service, which represents any type of service that can execute arbitrary commands
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "mqtt-serial")
    
    type_map=['led', 'servo', 'servo_relative', ' pin', 'read']
    DEVICE_LED = 0
    DEVICE_SERVO = 1
    DEVICE_PIN = 2
    DEVICE_PIN_READ = 3
    DEVICE_SERVO_RELATIVE = 4
    ORDER_RECEIVED = 5
    
    serial_file: Any
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
        mqtt = config.attributes.fields["mqtt"].string_value
        if mqtt == "":
            raise Exception("mqtt service must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        self.serial_file = open_serial_port(baudrate=115200, timeout=None)
        # pub.subscribe(self.send, 'serial')
        LOGGER.info('[SERIAL] Serial port opened')
        
        mqtt = config.attributes.fields["mqtt"].string_value
        actual_mqtt = dependencies[Pubsub.get_resource_name(mqtt)]
        self.mqtt = cast(Pubsub, actual_mqtt)
        LOGGER.info('[SERIAL] MQTT service defined')
        
        async def sub():
            await self.mqtt.subscribe("serial/send", self.mqttSend)

        asyncio.ensure_future(sub())
        
        LOGGER.info('[SERIAL] Subscribed to MQTT topic')
            
        return

    """ Implement the methods the Viam RDK defines for the Generic API (rdk:service:generic) """
    def mqttSend(self, msg: str):
        LOGGER.info('[SERIAL] mqttSend ' + msg)
        deserialized_json = eval(msg)
        self.send(deserialized_json.get('type'), deserialized_json.get('identifier'), deserialized_json.get('message'))
        
    def read(self):
        return read_i8(self.serial_file)

    def read16(self):
        return read_i16(self.serial_file)
        
    def send(self, type, identifier, message):
        """
        Examples:
        # send(mqttSerial.DEVICE_SERVO, 18, 20)
        # send(mqttSerial.DEVICE_LED, 1, (20,20,20))
        # send(mqttSerial.DEVICE_LED, range(9), (20,20,20))
        :param type: one of the DEVICE_ types
        :param identifier: an identifier or list / range of identifiers, pin or LED number
        :param message: the packet to send to the arduino
        """
        if self.serial_file is None:
            return

        # pub.sendMessage('led', identifiers='status5', color='blue')
        # print('[serial] ' + str(mqttSerial.type_map[type]) + ' id: ' + str(identifier) + ' val: ' + str(message))

        LOGGER.info('[SERIAL] type: ' + self.type_map[type] + ' id: ' + str(identifier) + ' val: ' + str(message))
        if type == mqttSerial.DEVICE_SERVO or type == 'servo':
            write_order(self.serial_file, Order.SERVO)
            write_i8(self.serial_file, identifier)
            write_i16(self.serial_file, int(message))
            LOGGER.info('[SERIAL] Moved value from Arduino: ' + str(self.read16()))
        if type == mqttSerial.DEVICE_SERVO_RELATIVE or type == 'servo_relative':
            write_order(self.serial_file, Order.SERVO_RELATIVE)
            write_i8(self.serial_file, identifier)
            write_i16(self.serial_file, int(message))
            LOGGER.info('[SERIAL] Moved value from Arduino: ' + str(self.read16()))
        elif type == mqttSerial.DEVICE_LED or type == 'led':
            write_order(self.serial_file, Order.LED)
            if isinstance(identifier, list) or isinstance(identifier, range):
                # write the number of leds to update
                write_i8(self.serial_file, len(identifier))
                for i in identifier:
                    write_i8(self.serial_file, i)
            else:
                write_i8(self.serial_file, 1)
                write_i8(self.serial_file, identifier)

            if isinstance(message, tuple):
                for v in message:
                    write_i8(self.serial_file, v)
            else:
                write_i16(self.serial_file, message)

        elif type == mqttSerial.DEVICE_PIN or type == 'pin':
            write_order(self.serial_file, Order.PIN)
            write_i8(self.serial_file, identifier)
            write_i8(self.serial_file, message)

        elif type == mqttSerial.DEVICE_PIN_READ or type == 'pin_read':
            # pub.sendMessage('led', identifiers='status5', color='green')
            write_order(self.serial_file, Order.READ)
            write_i8(self.serial_file, identifier)
            # pub.sendMessage('led', identifiers='status5', color='off')
            return read_i16(self.serial_file)
        # pub.sendMessage('led', identifiers='status5', color='off')
        
    from typing import Final

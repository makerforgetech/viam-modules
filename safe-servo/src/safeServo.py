from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, Mapping, Optional

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.servo import Servo
from viam.logging import getLogger

import time
import asyncio

from pubsub import pub
from gpiozero import AngularServo


LOGGER = getLogger(__name__)

class safeServo(Servo, Reconfigurable):
    
    """
    Servo represents a physical servo.
    """

    # @todo retrieve from arduino serial module
    DEVICE_SERVO = 1
    DEVICE_SERVO_RELATIVE = 4

    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "safe-servo")
    
    # create any class parameters here
    pin: int
    identifier: str
    index: int
    range: Tuple[int, int]
    start: int
    pos: int
    serial: bool
    # servo: AngularServo

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
        pin = config.attributes.fields["pin"].number_value
        if pin == None:
            raise Exception("A pin must be defined")
        identifier = config.attributes.fields["identifier"].string_value
        if identifier == None:
            raise Exception("An identifier must be defined")
        index = config.attributes.fields["index"].number_value
        if index == None:
            raise Exception("An index must be defined")
        range_min = config.attributes.fields["range_min"].number_value
        if range_min == None:
            raise Exception("A range_min must be defined")
        range_max = config.attributes.fields["range_max"].number_value
        if range_max == None:
            raise Exception("A range_max must be defined")
        start_pos = config.attributes.fields["start_pos"].number_value
        if start_pos == None:
            raise Exception("A start_pos must be defined")
        
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        self.pin = int(config.attributes.fields["pin"].number_value)
        self.identifier = config.attributes.fields["identifier"].string_value
        self.index = int(config.attributes.fields["index"].number_value)
        self.range = (int(config.attributes.fields["range_min"].number_value), int(config.attributes.fields["range_max"].number_value))
        self.start = int(config.attributes.fields["start_pos"].number_value)
        if (self.start == ""):
            self.start = 50
        
        self.pos = int(self.percentage_to_angle(self.start))
        
        self.serial = config.attributes.fields["serial"].bool_value
        self.servo = None # Used for gpiozero servo
        
        pub.subscribe(self.mvabs, 'servo:' + self.identifier + ':mvabs')
        pub.subscribe(self.mv, 'servo:' + self.identifier + ':mv')
        return

    """ Implement the methods the Viam RDK defines for the Servo API (rdk:component:servo) """
    
    async def move(self, angle: int, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        """
        Move the servo to the provided angle.

        ::

            my_servo = Servo.from_robot(robot=robot, name="my_servo")

            # Move the servo from its origin to the desired angle of 10 degrees.
            await my_servo.move(10)

            # Move the servo from its origin to the desired angle of 90 degrees.
            await my_servo.move(90)

        Args:
            angle (int): The desired angle of the servo in degrees.
        """
        if self.range[0] > angle or self.range[1] < angle:
            LOGGER.error('[Servo] %s Angle out of range: %d' % (self.identifier, angle))
            pub.sendMessage('log:error', msg='[Servo] %s Angle out of range: %d' % (self.identifier, angle))
            return False
        self.pos = int(angle)
        pub.sendMessage('log:info', msg='[Servo] %s Moving to %d' % (self.identifier, angle))
        LOGGER.info('[Servo] %s Moving to %d' % (self.identifier, angle))
        if (self.serial):
            pub.sendMessage('serial', type=self.DEVICE_SERVO, identifier=self.index, message=self.angle_to_percentage(angle))   
        else:
            if self.servo is None:
                self.servo = AngularServo(self.pin, min_angle=self.range[0], max_angle=self.range[1], initial_angle=self.start)
            self.servo.angle = angle                # Changes the angle (to move the servo)
            time.sleep(1)                                # @TODO: Remove this sleep
            self.servo.detach()                     # Detaches the servo (to stop jitter)
        
    async def mvabs(self, percentage: int):
        await self.move(self.percentage_to_angle(percentage))
    
    async def mv(self, percentage: int):
        await self.move(self.pos + self.percentage_to_angle(percentage))
        
    def percentage_to_angle(self, value):
        # Figure out how 'wide' each range is
        leftSpan = 100 - 0
        rightSpan = self.range[1] - self.range[0]

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return self.range[0] + (valueScaled * rightSpan)
    
    def angle_to_percentage(self, value):
        # Figure out how 'wide' each range is
        leftSpan = self.range[1] - self.range[0]
        rightSpan = 100 - 0

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - self.range[0]) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return 0 + (valueScaled * rightSpan)

    
    async def get_position(self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> int:
        """
        Get the current angle (degrees) of the servo.

        ::

            my_servo = Servo.from_robot(robot=robot, name="my_servo")

            # Move the servo from its origin to the desired angle of 10 degrees.
            await my_servo.move(10)

            # Get the current set angle of the servo.
            pos1 = await my_servo.get_position()

            # Move the servo from its origin to the desired angle of 20 degrees.
            await my_servo.move(20)

            # Get the current set angle of the servo.
            pos2 = await my_servo.get_position()

        Returns:
            int: The current angle of the servo in degrees.
        """
        return self.pos

    
    async def stop(self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        """
        Stop the servo. It is assumed that the servo stops immediately.

        ::

            my_servo = Servo.from_robot(robot=robot, name="my_servo")

            # Move the servo from its origin to the desired angle of 10 degrees.
            await my_servo.move(10)

            # Stop the servo. It is assumed that the servo stops moving immediately.
            await my_servo.stop()
        """
        return True

    
    async def is_moving(self) -> bool:
        """
        Get if the servo is currently moving.

        ::

            my_servo = Servo.from_robot(robot=robot, name="my_servo")

            print(my_servo.is_moving())


        Returns:
            bool: Whether the servo is moving.
        """
        return False

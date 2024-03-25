"""
This file registers the model with the Python SDK.
"""

from viam.components.servo import Servo
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .safeServo import safeServo

Registry.register_resource_creator(Servo.SUBTYPE, safeServo.MODEL, ResourceCreatorRegistration(safeServo.new, safeServo.validate))

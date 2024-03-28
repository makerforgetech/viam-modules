"""
This file registers the model with the Python SDK.
"""

from viam.components.servo import Servo
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .mqttServo import mqttServo

Registry.register_resource_creator(Servo.SUBTYPE, mqttServo.MODEL, ResourceCreatorRegistration(mqttServo.new, mqttServo.validate))

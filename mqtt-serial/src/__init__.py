"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .mqttSerial import mqttSerial

Registry.register_resource_creator(Generic.SUBTYPE, mqttSerial.MODEL, ResourceCreatorRegistration(mqttSerial.new, mqttSerial.validate))

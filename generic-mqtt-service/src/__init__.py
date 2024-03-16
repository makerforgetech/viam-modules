"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .mqttService import mqttService

Registry.register_resource_creator(Generic.SUBTYPE, mqttService.MODEL, ResourceCreatorRegistration(mqttService.new, mqttService.validate))

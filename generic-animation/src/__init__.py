"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .animation import animation

Registry.register_resource_creator(Generic.SUBTYPE, animation.MODEL, ResourceCreatorRegistration(animation.new, animation.validate))

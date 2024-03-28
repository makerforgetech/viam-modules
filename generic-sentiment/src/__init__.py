"""
This file registers the model with the Python SDK.
"""

from viam.services.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .sentiment import sentiment

Registry.register_resource_creator(Generic.SUBTYPE, sentiment.MODEL, ResourceCreatorRegistration(sentiment.new, sentiment.validate))

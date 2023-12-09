"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import VisionClient
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .sentiment import Sentiment

Registry.register_resource_creator(VisionClient.SUBTYPE, Sentiment.MODEL, ResourceCreatorRegistration(Sentiment.new_sentiment, Sentiment.validate_config))
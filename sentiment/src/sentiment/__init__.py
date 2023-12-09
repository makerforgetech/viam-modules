"""
This file registers the sentiment subtype with the Viam Registry, as well as the specific models.
"""

from viam.resource.registry import Registry, ResourceCreatorRegistration, ResourceRegistration

#from .api import SpeechClient, SpeechRPCService, SpeechService
#from .speechio import SpeechIOService

from sentiment import SentimentAnalyisModule

Registry.register_subtype(ResourceRegistration(SentimentAnalyisModule, lambda name))

Registry.register_resource_creator(SpeechService.SUBTYPE, SpeechIOService.MODEL, ResourceCreatorRegistration(SpeechIOService.new))
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

import time
import asyncio

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from viam.proto.common import DoCommandRequest, DoCommandResponse
from viam.utils import ValueTypes, dict_to_struct, struct_to_dict
from numpy.typing import NDArray

from viam.proto.service.mlmodel import Metadata
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

from viam.services.mlmodel import MLModelClient

LOGGER = getLogger(__name__)

class sentiment(Generic, Reconfigurable):
    
    """
    Generic service, which represents any type of service that can execute arbitrary commands
    """


    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "sentiment")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    # some_pin: int
    analyzer: SentimentIntensityAnalyzer

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
        # some_pin = config.attributes.fields["some_pin"].number_value
        # if some_pin == "":
            # raise Exception("A some_pin must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        nltk.download('vader_lexicon')
        # initialize NLTK sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()
        return

    """ Implement the methods the Viam RDK defines for the Generic API (rdk:service:generic) """

    async def do_command(
                self,
                command: Mapping[str, ValueTypes],
                *,
                timeout: Optional[float] = None,
                **kwargs
            ) -> Mapping[str, ValueTypes]:
                result = {key: False for key in command.keys()}
                for (name, args) in command.items():
                    if name == 'sentiment':
                        text = args[0]
                        LOGGER.info(f"Running sentiment analysis on: {text}")
                        scores = self.analyzer.polarity_scores(text)
                        result[name] =  scores
                return result
            
    from typing import Final

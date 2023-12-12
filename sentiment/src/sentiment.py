import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast
from grpclib.client import Channel

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes, dict_to_struct, struct_to_dict

from viam.logging import getLogger

from viam.proto.common import DoCommandRequest, DoCommandResponse


from numpy.typing import NDArray

from viam.proto.service.mlmodel import Metadata
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

from viam.services.mlmodel import MLModelClient

LOGGER = getLogger(__name__)

class Sentiment(MLModelClient, Reconfigurable):
    # Here is where we define our new model's colon-delimited-triplet
    # (acme:demo:mybase) acme = namespace, demo = repo-name,
    # mybase = model name.
    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "sentiment")

    def __init__(self, name: str, channel: Channel):
        super().__init__(name, channel)
        # Do this the first time
        nltk.download('vader_lexicon')

        # initialize NLTK sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()


    # Constructor
    @classmethod
    def new_sentiment(cls,
                 config: ComponentConfig,
                 dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sentiment = cls(config.name)
        sentiment.reconfigure(config, dependencies)
        return sentiment

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        return []

    # Handles attribute reconfiguration
    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        pass
        # left_name = config.attributes.fields["motorL"].string_value
        # right_name = config.attributes.fields["motorR"].string_value

        # left_motor = dependencies[Motor.get_resource_name(left_name)]
        # right_motor = dependencies[Motor.get_resource_name(right_name)]

        # self.left = cast(Motor, left_motor)
        # self.right = cast(Motor, right_motor)

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Mapping[str, ValueTypes]:
        request = DoCommandRequest(name=self.name, command=self.get(command.command))
        response: DoCommandResponse = await self.client.DoCommand(request, timeout=timeout)
        return struct_to_dict(response.result)
    
    # create get_sentiment function
    async def get(self, text: str) -> str:
        scores = self.analyzer.polarity_scores(text)
        print(scores)
        return scores['compound']
    
    async def infer(self, input_tensors: Dict[str, NDArray], *, timeout: Optional[float]) -> Dict[str, NDArray]:
        raise NotImplementedError()
    
    async def metadata(self, *, timeout: Optional[float]) -> Metadata:
        raise NotImplementedError()

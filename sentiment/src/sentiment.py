import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam.logging import getLogger

from numpy.typing import NDArray

from viam.proto.service.mlmodel import Metadata
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype

from viam.services.mlmodel import MLModel

LOGGER = getLogger(__name__)


class Sentiment(MLModel, Reconfigurable):
    """
    MyBase implements a base that only supports set_power
    (basic forward/back/turn controls) is_moving (check if in motion), and stop
    (stop all motion).

    It inherits from the built-in resource subtype Base and conforms to the
    ``Reconfigurable`` protocol, which signifies that this component can be
    reconfigured. Additionally, it specifies a constructor function
    ``MyBase.new_base`` which confirms to the
    ``resource.types.ResourceCreator`` type required for all models.
    """

    # Here is where we define our new model's colon-delimited-triplet
    # (acme:demo:mybase) acme = namespace, demo = repo-name,
    # mybase = model name.
    MODEL: ClassVar[Model] = Model(ModelFamily("makerforge", "viam-modules"), "sentiment")

    def __init__(self, name: str, left: str, right: str):
        super().__init__(name, left, right)
        # Do this the first time
        nltk.download('all')

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

    """
    Implement the methods the Viam RDK defines for the base API
    (rdk:component:base)
    """
    
    # create get_sentiment function
    async def get(self, text):
        scores = self.analyzer.polarity_scores(text)
        print(scores)
        return scores['compound']
    
    async def infer(self, input_tensors: Dict[str, NDArray], *, timeout: Optional[float]) -> Dict[str, NDArray]:
        raise NotImplementedError()
    
    async def metadata(self, *, timeout: Optional[float]) -> Metadata:
        raise NotImplementedError()

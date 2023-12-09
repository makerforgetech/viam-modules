import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from typing import Final, ClassVar, Mapping
from viam.services.service_base import ServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.resource.types import Model

from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model

from viam import logging
LOGGER = logging.getLogger(__name__)
CACHEDIR = "/tmp/cache"

import json

from typing_extensions import Self




class SentimentAnalysisModule(ServiceBase):
    
    SUBTYPE: Final = Subtype("makerforge", RESOURCE_TYPE_SERVICE, "sentiment")
    MODEL: ClassVar[Model] = Model.from_string("makerforge:viam-modules:sentiment")
    
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sentiment = cls(config.name)
        LOGGER.debug(json.dumps(sentiment.__dict__))
        return sentiment

    def __init__(self):
        # Do this the first time
        nltk.download('all')

        # initialize NLTK sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    # create get_sentiment function
    def get(self, text):
        scores = self.analyzer.polarity_scores(text)
        print(scores)
        return scores['compound']

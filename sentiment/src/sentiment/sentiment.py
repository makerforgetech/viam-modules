import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from typing import Final, ClassVar
from viam.services.service_base import ServiceBase
from viam.resource.types import RESOURCE_TYPE_SERVICE, Subtype
from viam.resource.types import Model


class SentimentAnalysisModule(ServiceBase):
    
    SUBTYPE: Final = Subtype("makerforge", RESOURCE_TYPE_SERVICE, "sentiment")
    MODEL: ClassVar[Model] = Model.from_string("makerforge:viam-modules:sentiment")

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

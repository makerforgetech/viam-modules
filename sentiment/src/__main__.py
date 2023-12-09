import asyncio
import sys

from viam.services.vision import VisionClient
from viam.module.module import Module
from .sentiment import Sentiment

async def main():
    module = Module.from_args()
    module.add_model_from_registry(VisionClient.SUBTYPE, Sentiment.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
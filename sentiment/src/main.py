import asyncio

from viam.services.mlmodel import MLModel
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from sentiment import Sentiment


async def main():
    """
    This function creates and starts a new module, after adding all desired
    resource models. Resource creators must be registered to the resource
    registry before the module adds the resource model.
    """
    Registry.register_resource_creator(
        MLModel.SUBTYPE,
        Sentiment.MODEL,
        ResourceCreatorRegistration(Sentiment.new_sentiment, Sentiment.validate_config))
    module = Module.from_args()

    module.add_model_from_registry(MLModel.SUBTYPE, Sentiment.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
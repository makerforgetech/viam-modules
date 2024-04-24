import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.generic import Generic
from pubsub_python import Pubsub

# These must be set. You can get them from your robot's 'Code sample' tab. 
import os
# Set by including 'export ROBOT_API_KEY=<your_key>' in your .bashrc file
robot_api_key = os.getenv('ROBOT_API_KEY') or ''
# Set by including 'export ROBOT_API_KEY_ID=<your_key_id>' in your .bashrc file
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
# Set by including 'export ROBOT_ADDRESS=<your_robot_address>' in your .bashrc file
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=robot_api_key,
      api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)

async def main():
    robot = await connect()

    # print('Resources:')
    # print(robot.resource_names)
    
    # Change name of the service to match the name of the service you are using
    api = Pubsub.from_robot(robot, name="mqtt-service")

    async def pub():
        # Topic includes identifier of the servo defined in the configuration (leg_l_hip in this example)
        await api.publish('servo/leg_l_hip/mv' , str({"percentage": 10}), 2)

    await pub()
        
    await asyncio.sleep(2)

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
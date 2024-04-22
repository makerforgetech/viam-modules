import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.generic import Generic


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

    print('Resources:')
    print(robot.resource_names)
    
    service = Generic.from_robot(robot, "sentiment-service")

    # Uncomment to show failure    
    # response = await animation.do_command({"animate": ["not_an_animation"]})
    
    response = await service.do_command({"sentiment": ["this is my happy message"]})
    # print(f"The response is {response}")
    print(response)
    

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
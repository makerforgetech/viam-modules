import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.generic import Generic

import setenv # Set below environment variables
# These must be set. You can get them from your robot's 'Code sample' tab
robot_api_key = os.getenv('ROBOT_API_KEY') or ''
robot_api_key_id = os.getenv('ROBOT_API_KEY_ID') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key=robot_api_key,
      api_key_id=robot_api_key_id
    )
    return await RobotClient.at_address(robot_address, opts)
def on_message(client, userdata, message):
    print("test")
    # print(f"message received {str(message.payload.decode('utf-8'))}")

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
    
    mqttBroker = Generic.from_robot(robot, "mqtt-service1")

    # Uncomment to show failure    
    # response = await animation.do_command({"animate": ["not_an_animation"]})
    
    response = await mqttBroker.do_command({"subscribe": {"topic": "testTopic", "method": on_message}})
    print(f"The response is {response['subscribe']}")
    # response['subscribe'].message_callback_add('testTopic', on_message)
    
    response = await mqttBroker.do_command({"publish": {"topic": "testTopic", "message": "something"}})
    print(f"The response is {response['publish']}")
    
    
    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())

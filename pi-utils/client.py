import asyncio
import time

from viam.components.generic import Generic
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor

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

    print("Resources:")
    print(robot.resource_names)
    
    led = Generic.from_robot(robot, "pi-utilities")
    response = await led.do_command({"get_temp": []})
    print(f"The reading is {response}")
    
    response = await led.do_command({"pin:high": [22]})
    print(f"Pin changed is {response}")
    # for color in [65280, 0]:
    #     for pixel in range(7):
    #         await led.do_command({"set_pixel_color": [pixel, color]})
    #         await led.do_command({"show": []})
    #         time.sleep(1)

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
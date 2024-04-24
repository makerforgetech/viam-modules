# MQTT-Servo Module

Communicate with a servo motor over MQTT using percentage values.

This module is built for use with the [Maker Forge Modular Biped Robot](https://github.com/makerforgetech/modular-biped).

For support join the Maker Forge Discord server: [Join Discord](https://bit.ly/makerforge-community)

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:servo:makerforge:viam-modules:mqtt-servo` model from the [`makerforge:viam-modules:mqtt-servo` module](https://app.viam.com/module/rdk/makerforge:viam-modules:mqtt-servo).

This module requires the mqtt-serial module to be running on the same machine when using serial communication. [See details](https://github.com/makerforgetech/viam-modules/tree/main/mqtt-serial)

## Configure your Servo

> [!NOTE]  
> Before configuring your servo, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `servo` type, then select the `makerforge:viam-modules:mqtt-servo` model. 
Enter a name for your servo and click **Create**.

On the new component panel, copy and paste the following attribute template into your servo’s **Attributes** box:

```json
{
  "identifier": <string>,
  "index": <int>,
  "pin": <int>,
  "range_max": <int>,
  "range_min": <int>,
  "serial": <bool>,
  "start": <int>,
  "mqtt": <string>
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:servo:makerforge:viam-modules:mqtt-servo` servos:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `identifier` | string | **Required** |  The human readable identifier for the servo, e.g. leg_l_hip |
| `index` |  int  | **Reqired** |  An index of the servo, e.g. 0 |
| `pin` | int | **Required** | The GPIO pin number the servo is connected to |
| `range_max` | int | **Required** | The maximum angle the servo can rotate to |
| `range_min` | int | **Required** | The minimum angle the servo can rotate to |
| `serial` | bool | **Required** | Whether the servo is connected via serial |
| `start` | int | **Required** | The percentage the servo should start at (0-100) |
| `mqtt` | string | **Required** | The MQTT service to use for communication |

### Example Configuration

```json
{
  "identifier": "leg_l_hip",
  "index": 0,
  "pin": 1,
  "range_max": 180,
  "range_min": 0,
  "serial": true,
  "start": 50,
  "mqtt": "mqtt-service"
}
```

### Usage

Interact with the servo via the MQTT service. The following topics are available:

- `servo/<identifier>/mv` - Set the angle of the servo relative to it's current position. Pass a JSON object with the `percentage` key and the desired angle percentage.
- `servo/<identifier>/mvabs` - Set the absolute angle of the servo. Pass a JSON object with the `percentage` key and the desired angle percentage.

Example:

```python

from pubsub_python import Pubsub

api = Pubsub.from_robot(robot, name="mqtt-service")

async def pub():
    await api.publish('servo/leg_l_hip/mv' , str({"percentage": 10}), 0)

await pub()
    
await asyncio.sleep(2)

```

See `client.py` for a working example. 
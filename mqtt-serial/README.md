# MQTT Serial Module

Communicate with a microcontroller over serial using MQTT events.

This module is built for use with the [Maker Forge Modular Biped Robot](https://github.com/makerforgetech/modular-biped).

For support join the Maker Forge Discord server: [Join Discord](https://bit.ly/makerforge-community)

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:generic:makerforge:viam-modules:serial` model from the [`makerforge:viam-modules:serial` module](https://app.viam.com/module/rdk/makerforge:viam-modules:serial).

## Configure your MQTT Serial Service

> [!NOTE]  
> Before configuring your service, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `generic` type, then select the `makerforge:viam-modules:serial` model. 
Enter a name for your generic and click **Create**.

On the new component panel, copy and paste the following attribute template into your generic’s **Attributes** box:

```json
{
  "mqtt": <string>
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:generic:makerforge:viam-modules:serial` generics:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `mqtt-service` | string | **Required** |  Define the MQTT service to use for communication |

### Example Configuration

```json
{
  "mqtt": "mqtt-service"
}
```

### Usage

See `client.py` for a working example:
  
```python

api = Pubsub.from_robot(robot, name="mqtt-service")

async def pub():
    await asyncio.sleep(1)
    json = {
        "type": "servo",
        "identifier": 1,
        "message": 90
    }
    await api.publish("serial/send", str(json), 0)

await pub()
    
await asyncio.sleep(2)
```

## Troubleshooting

_Add troubleshooting notes here._

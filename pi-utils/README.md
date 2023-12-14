# Installation

Config -> Components -> Create Component -> Select makerforge:viam-modules:pi-utils -> Set name to `pi-utilities`.

# Usage

Copy setenv.py.example into your script's directory as `setenv.py`, set the environment variables and save. The `client.py` script will use this file to connect to Viam.

## Get CPU temperature

```
util = Generic.from_robot(robot, "pi-utilities")
response = await util.do_command({"get_temp": []})
print(f"The reading is {response['temp']}")
```

See client.py for more detailed examples.

# Home Assistant Add-on: MQTT Discord Bot
![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

![Current version][version]

This Home Assistant add-on runs a Python script that listens for Discord events and sends them to MQTT-Broker.

## Create an Discord-App
The following guide describes in "Step 1" how to create a Discord app. Relevant points are the app name and the token. If necessary, the scope can also be adjusted to limit permissions.

#### [discord.com/docs/getting-started](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app)


## AddOn-Configuration
Set the AddOn-Settings
- mqtt broker url
- mqtt port
- mqtt user
- mqtt password
- discord token
- discord guild id (serverid)

## Sensor
To take a look, which arguments available, use developer-tools and search for discord_event.
The MQTT-Sensor is splitted into a second sensor to map the events. For example: the join/left event become the online/offline status
Add the following Sensors into your configuration.yaml:

### MQTT-Sensor
```
mqtt:
  sensor:
    - name: "Discord Event"
      unique_id: "discord"
      state_topic: "discord/events"
      value_template: "{{ value_json.action }}"
      json_attributes_topic: "discord/events"
      json_attributes_template: "{{ value_json | tojson }}"
```

### Template-Sensor
Sensor-Example to get User-Voice-Status of <nickname>
It's a remapping of your mqtt-sensor with rules
```
template:
  - sensor:
      # Remapping of mqtt-sensor.
      - name: "Discord <nickname>"
        device_class: "enum"
        state: >
          {% if state_attr('sensor.discord_event', 'member_name') == '<nickname>' %}
            {% if state_attr('sensor.discord_event', 'action') == 'joined' %}
              Online
            {% elif state_attr('sensor.discord_event', 'action') == 'left' %}
              Offline
            {% else %}
              unknown
            {% endif %}
          {% else %}
            {{ states('sensor.discord_<nickname>') }}
          {% endif %}
        attributes:
          options: "{{ ['Online', 'Offline'] }}"
          # optional:
          action: "{{ state_attr('sensor.discord_event', 'action') }}"
          member_name: "{{ state_attr('sensor.discord_event', 'member_name') }}"
          member_id: "{{ state_attr('sensor.discord_event', 'member_id') }}"
          status: "{{ state_attr('sensor.discord_event', 'status') }}"
          channel_name: "{{ state_attr('sensor.discord_event', 'channel_name') }}"
          channel_id: "{{ state_attr('sensor.discord_event', 'channel_id') }}"
          guild_name: "{{ state_attr('sensor.discord_event', 'guild_name') }}"
          guild_member_count: "{{ state_attr('sensor.discord_event', 'guild_member_count') }}"
          timestamp: "{{ state_attr('sensor.discord_event', 'timestamp') }}"
          current_members: "{{ state_attr('sensor.discord_event', 'current_members') }}"
          participant_count: "{{ state_attr('sensor.discord_event', 'participant_count') }}"
          avatar_url: "{{ state_attr('sensor.discord_event', 'avatar_url') }}"
```

---

## Alternative: Running Add-On standalone (not in HA)
On different docker-host without installing as Add-On in HA.

This is not needed when using Home-Assistant AddOn

```
git clone https://github.com/ZackEndboss/hassio-addons
cd hassio-addons/mqtt-dicosrd-bot
nano options.json
```

Create 'options.json':
```
# options.json
{
    "mqtt_broker": "localhost",
    "mqtt_port": 1883,
    "mqtt_username": "user",
    "mqtt_password": "password",
    "discord_token": "your_discord_token",
    "discord_guild_id": "your_server_id"
}
```

### Docker Build
Create a Docker-Image and start Docker-Container

#### Mapping Architektur to YAML-Schlüssel
```
ARCH=$(uname -m); \
if [ "$ARCH" = "x86_64" ]; then YAML_ARCH="amd64"; \
elif [ "$ARCH" = "aarch64" ]; then YAML_ARCH="aarch64"; \
elif [ "$ARCH" = "armv7l" ]; then YAML_ARCH="armv7"; \
else echo "Unsupported architecture: $ARCH"; exit 1; fi;
```

#### Parse build_from-Value from build.yaml
```
BUILD_FROM=$(grep "$YAML_ARCH:" build.yaml | sed 's/.*: "\(.*\)"/\1/')
TEMPIO_VERSION=$(grep "TEMPIO_VERSION:" build.yaml | sed 's/.*: "\(.*\)"/\1/')
```

#### Start Docker-Build with Build-Arguments
```docker build --build-arg BUILD_FROM=$BUILD_FROM --build-arg TEMPIO_VERSION=$TEMPIO_VERSION --build-arg BUILD_ARCH=$YAML_ARCH -t mqtt-dicosrd-bot .```

#### Docker Run
```docker run -it --rm --name mqtt-dicosrd-bot -v /path/to/options.json:/data/options.json mqtt-dicosrd-bot```

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[version]: https://img.shields.io/badge/version-v1.0.15-blue.svg
# MQTT Discord Bot

This Home Assistant add-on runs a Python script that listens for Discord events and sends them to MQTT-Broker.


[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FZackEndboss%2FHA_discord2mqtt)


## Add-ons

This repository contains the following add-ons

### [mqtt-discord-bot add-on](./mqtt-discord-bot)


# Sensor
To take a look, which arguments available, use developer-tools and search for discord_event.
The MQTT-Sensor is splitted into a second sensor to map the events. For example: the join/left event become the online/offline status
Add the following Sensors into your configuration.yaml:

## MQTT-Sensor
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

## Template-Sensor
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


# Running Add-On standalone
On different docker-host without installing as Add-On in HA

```cd mqtt-dicosrd-bot```

create 'options.json':
```
{
    "mqtt_broker": "localhost",
    "mqtt_port": 1883,
    "mqtt_username": "user",
    "mqtt_password": "password",
    "discord_token": "your_discord_token",
    "discord_guild_id": "your_server_id"
}
```

## Docker Build
Create a Docker-Image and start Docker-Container:

### Mapping Architektur to YAML-Schlüssel
```
ARCH=$(uname -m); \
if [ "$ARCH" = "x86_64" ]; then YAML_ARCH="amd64"; \
elif [ "$ARCH" = "aarch64" ]; then YAML_ARCH="aarch64"; \
elif [ "$ARCH" = "armv7l" ]; then YAML_ARCH="armv7"; \
else echo "Unsupported architecture: $ARCH"; exit 1; fi;
```

### Parse build_from-Value from build.yaml
```
BUILD_FROM=$(grep "$YAML_ARCH:" build.yaml | sed 's/.*: "\(.*\)"/\1/')
TEMPIO_VERSION=$(grep "TEMPIO_VERSION:" build.yaml | sed 's/.*: "\(.*\)"/\1/')
```

### Start Docker-Build with Build-Arguments
```docker build --build-arg BUILD_FROM=$BUILD_FROM --build-arg TEMPIO_VERSION=$TEMPIO_VERSION --build-arg BUILD_ARCH=$YAML_ARCH -t mqtt-dicosrd-bot .```

### Docker Run
```docker run -it --rm --name mqtt-dicosrd-bot -v /path/to/options.json:/data/options.json mqtt-dicosrd-bot```

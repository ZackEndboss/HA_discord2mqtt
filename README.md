# Repository
You can add the Repository into your Home-Assistant Add-On Store to add and auto. update your Add-Ons

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FZackEndboss%2Fhassio-addons)

## Add-ons

This repository contains the following add-ons

#### [mqtt-discord-bot add-on](./mqtt-discord-bot)
#### [borgmatic add-on](./borgmatic)

---
---

# MQTT Discord Bot

This Home Assistant add-on runs a Python script that listens for Discord events and sends them to MQTT-Broker.

# borgmatic - pre-state is borg only

This Add-on backup the contents of `/backup` to a remote [Borg Backup](https://www.borgbackup.org/) server.
The Pre-Version of this addon is using borg only - in second step it will be transform into borgmatic
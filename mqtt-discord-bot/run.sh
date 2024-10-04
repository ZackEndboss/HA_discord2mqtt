#!/usr/bin/with-contenv bash

#with-contenv
#s6-setuidgid nobody

cd /usr/src/app
exec python /usr/src/app/discord_mqtt.py
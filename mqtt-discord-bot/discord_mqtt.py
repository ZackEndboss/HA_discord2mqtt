import discord
import json
from paho.mqtt import client as mqtt_client
from datetime import datetime
import time
import logging
import os

# Logger konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if os.path.isfile(".env"):
    abs_path = os.path.abspath('.env')
    logging.info(f"loading local {abs_path}")
    from dotenv import load_dotenv
    load_dotenv(abs_path)

# MQTT Broker Informationen
topic       = "discord/events"
broker      = os.getenv('MQTT_BROKER', 'localhost')
port        = os.getenv('MQTT_PORT', 1883)
username    = os.getenv('MQTT_USERNAME', '') # Ersetzen Sie diesen mit Ihrem MQTT-Benutzernamen
password    = os.getenv('MQTT_PASSWORD', '') # Ersetzen Sie diesen mit Ihrem MQTT-Passwort
guild_id    = os.getenv('DISCORD_GUILD_ID', '') # Die ID des Servers, für den der Bot arbeiten soll
# Discord Bot Token
token       = os.getenv('DISCORD_TOKEN', '')

if isinstance(port, str) and port.isdecimal():
    port = int(port)

logging.info(f"Connecting to MQTT broker at {broker}:{port} with username {username} on discord-serverid {guild_id}")

# MQTT Client Setup
def connect_mqtt():
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected MQTT disconnection. Will auto-reconnect")
        try:
            client.reconnect()  # Manuell wiederverbinden
        except Exception as e:
            logging.error(f"Failed to reconnect: {e}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.error(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()
    client.username_pw_set(username, password)  # Benutzername und Passwort setzen
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port, keepalive=60)  # Keep-Alive auf 60 Sekunden setzen
    client.reconnect_delay_set(min_delay=1, max_delay=120)  # Wiederverbindungsintervall definieren
    #client.loop_forever()
    
    # Set MQTT-Client logging level
    client.enable_logger(logging.getLogger())  # MQTT-Client verwendet den globalen Logger
    return client

mqtt_client = connect_mqtt()
mqtt_client.loop_start()

def check_mqtt_connection():
    while True:
        if not mqtt_client.is_connected():
            logging.warning("Connection lost, attempting to reconnect...")
            mqtt_client.reconnect()
        time.sleep(20)  # alle 10 Sekunden überprüfen

# Discord Bot Setup
intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)
#client.socket().settimeout(100)  # Setzt ein Timeout von 5 Minuten für den Socket - noch nicht getestet

@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')


@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == int(guild_id):
        event_time = datetime.utcnow().isoformat() + 'Z'
        channel = after.channel if after.channel else before.channel
        current_members = [m.name for m in channel.members] if channel else []
        data = {
            'member_name': member.name,
            'member_id': member.id,
            'action': 'joined' if before.channel is None else 'left',
            'channel_name': channel.name if channel else 'None',
            'channel_id': channel.id if channel else 'None',
            'guild_name': member.guild.name,
            'guild_member_count': member.guild.member_count,
            'timestamp': event_time,
            'status': str(member.status),
            'participant_count': len(channel.members) if channel else 0,
            'is_muted': member.voice.mute if member.voice else False,
            'is_deaf': member.voice.deaf if member.voice else False,
            'avatar_url': str(member.display_avatar.url),
            'current_members': current_members  # Liste der Mitglieder im Channel nach dem Event
        }
        mqtt_client.publish(topic, json.dumps(data))
        logging.info(f"{member.name} {'joined' if after.channel else 'left'} {channel.name if channel else 'None'} at {event_time}")

client.run(token)

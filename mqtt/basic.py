import paho.mqtt.client as mqtt
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

USERNAME = os.environ.get('ADAFRUIT_USERNAME')
KEY = os.environ.get('ADAFRUIT_KEY')
FEED = os.environ.get('ADAFRUIT_FEED')

SERVER = 'io.adafruit.com'
PORT = 1883
KEEPALIVE = 3600

PATH = USERNAME + '/f/' + FEED

def on_connect(client, userdata, flags, rc):
    print('Connected!')
    client.subscribe(PATH)
    print('Subscribed to path {0}!'.format(PATH))

def on_disconnect(client, userdata, rc):
    print('Disconnected!')

def on_message(client, userdata, msg):
    print('Received on {0}: {1}'.format(msg.topic, msg.payload.decode('utf-8')))


# Create MQTT client and connect to Adafruit IO.
client = mqtt.Client()
client.username_pw_set(USERNAME, KEY)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(SERVER, port=PORT, keepalive=KEEPALIVE)

client.loop_forever()
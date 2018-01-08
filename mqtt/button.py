from Adafruit_IO import *
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

USERNAME = os.environ.get('ADAFRUIT_USERNAME')
KEY = os.environ.get('ADAFRUIT_KEY')
FEED = os.environ.get('ADAFRUIT_FEED')

# Callbacks
def onConnected(client):
    print('Connected')
    client.publish(FEED, 'OFF')
    client.subscribe(FEED)

def onDisconnected(client):
    print('Disconnected')

def onMessage(client, feed, message):
    print('{0}: {1}'.format(feed, message))

client = MQTTClient(USERNAME, KEY)
client.on_connect = onConnected
client.on_disconnect = onDisconnected
client.on_message = onMessage

client.connect()
client.loop_blocking()
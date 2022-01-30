from datetime import datetime
import json
import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    """The callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def main():
    room = "room1"
    sensor = "sensor1"
    client = mqtt.Client(f"{sensor}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async("127.0.0.1", 1883, 60)
    client.loop_start()

    try:
        while True:
            time.sleep(5)
            topic = f"home/{room}/{sensor}"
            payload = json.dumps({"date": str(datetime.now()), "data": 25})
            client.publish(topic, payload)
    except (KeyboardInterrupt):
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()

import json
import time

import paho.mqtt.client as mqqtt
import pytest

payload = None


def on_connect(client, userdata, flags, rc):
    """The callback for when the client receives a CONNACK response from the server."""
    print("Connected with result code " + str(rc))
    client.subscribe("home/room1/sensor1/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    global payload
    payload = json.loads(msg.payload)


def test_simulated_sensor():
    client = mqqtt.Client("tester")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async("127.0.0.1", 1883, 60)
    client.loop_start()
    global payload
    start_time = time.monotonic()
    timeout = 0
    while not payload and timeout < 5:
        time.sleep(0.1)
        timeout = time.monotonic() - start_time

    assert payload
    assert payload["data"] == 25


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

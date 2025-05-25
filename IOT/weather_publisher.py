from sense_hat import SenseHat
import time, json
import paho.mqtt.client as mqtt

sense = SenseHat()
client = mqtt.Client()
client.connect("localhost", 1883)

while True:
    data = {
        "temperature": round(sense.get_temperature(), 2),
        "humidity": round(sense.get_humidity(), 2),
        "pressure": round(sense.get_pressure(), 2),
        "timestamp": time.time()
    }
    client.publish("weather/data", json.dumps(data))
    print("Published:", data)
    time.sleep(5)

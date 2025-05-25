import paho.mqtt.client as mqtt
import csv
import json
from datetime import datetime
import os

csv_filename = "weather_log.csv"

# Create file and write header if not exists
if not os.path.exists(csv_filename):
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
import paho.mqtt.client as mqtt
import csv
import json
from datetime import datetime
import os

csv_filename = "weather_log.csv"

# Create the CSV file with a header if it doesn't exist
if not os.path.exists(csv_filename):
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature", "humidity", "pressure"])

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("weather/data")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    ts = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    temp = data["temperature"]
    hum = data["humidity"]
    pres = data["pressure"]

    # Print nicely labeled output
    print(f"Received: [{ts}] Temperature: {temp}°C | Humidity: {hum}% | Pressure: {pres} hPa")

    # Save to CSV
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([ts, temp, hum, pres])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)
client.loop_forever()






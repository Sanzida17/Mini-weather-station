from flask import Flask, render_template
import csv
from datetime import datetime

app = Flask(__name__)

def read_weather_data():
    rows = []
    try:
        with open('weather_log.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows

@app.route('/')
def home():
    rows = read_weather_data()

    if not rows:
        avg_temp = avg_hum = avg_pres = "N/A"
    else:
        temperatures = [float(row['temperature']) for row in rows]
        humidities = [float(row['humidity']) for row in rows]
        pressures = [float(row['pressure']) for row in rows]

        avg_temp = round(sum(temperatures) / len(temperatures), 2)
        avg_hum = round(sum(humidities) / len(humidities), 2)
        avg_pres = round(sum(pressures) / len(pressures), 2)

    return render_template("home.html", avg_temp=avg_temp, avg_hum=avg_hum, avg_pres=avg_pres)

@app.route('/dashboard')
def dashboard():
    rows = read_weather_data()
    if not rows:
        return "No data available"

    timestamps = [row['timestamp'] for row in rows]
    temperatures = [float(row['temperature']) for row in rows]
    humidities = [float(row['humidity']) for row in rows]
    pressures = [float(row['pressure']) for row in rows]

    return render_template("dashboard.html", labels=timestamps,
                           temperatures=temperatures,
                           humidities=humidities,
                           pressures=pressures)

@app.route('/table')
def table():
    rows = read_weather_data()
    return render_template("table.html", rows=rows)

@app.route('/temperature')
def temperature_chart():
    rows = read_weather_data()
    labels = [row['timestamp'] for row in rows]
    data = [float(row['temperature']) for row in rows]
    return render_template('single_chart.html', labels=labels, data=data, title='Temperature (°C)', color='red')

@app.route('/humidity')
def humidity_chart():
    rows = read_weather_data()
    labels = [row['timestamp'] for row in rows]
    data = [float(row['humidity']) for row in rows]
    return render_template('single_chart.html', labels=labels, data=data, title='Humidity (%)', color='blue')

@app.route('/pressure')
def pressure_chart():
    rows = read_weather_data()
    labels = [row['timestamp'] for row in rows]
    data = [float(row['pressure']) for row in rows]
    return render_template('single_chart.html', labels=labels, data=data, title='Pressure (hPa)', color='green')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


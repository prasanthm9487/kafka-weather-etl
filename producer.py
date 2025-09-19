from kafka import KafkaProducer
import json
import time
import requests # type: ignore

# Connect to Kafka broker
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Weather API configuration
LATITUDE = 12.9716
LONGITUDE = 77.5946
API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m"

# Send messages
while True:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        current_weather = data.get("current", {})
        temperature = current_weather.get("temperature_2m")
        humidity = current_weather.get("relative_humidity_2m")

        if temperature is not None and humidity is not None:
            weather_data = {
                "city": "Bangalore",
                "temperature": temperature,
                "humidity": humidity
            }
            producer.send("weather", weather_data)
            print(f"Sent: {weather_data}")
        else:
            print("Weather data not found in API response.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")

    time.sleep(1)

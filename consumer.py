from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import os

load_dotenv()

consumer = KafkaConsumer(
    "weather",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",   # or "latest"
    enable_auto_commit=True,
    group_id="weather-consumer-group",
    value_deserializer=lambda v: v.decode("utf-8") if v else None
)

con = create_engine(os.getenv("DB_URI","sqlite:///weather.db"))

print("Listening for messages...")

for message in consumer:
    try:
        if message.value:  # Only parse if not empty
            data = json.loads(message.value)
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Received: {data}")
            data = pd.DataFrame([data])
            data.to_sql('streaming_weather', con=con, if_exists='append', index=False)
        else:
            print("⚠️ Skipped empty message")
    except Exception as e:
        print(f"⚠️ Failed to parse: {message.value}, error: {e}")

# Real-time Weather Data Streaming with Kafka

This project demonstrates a simple real-time data streaming pipeline using Apache Kafka. It consists of a producer that fetches real-time weather data and sends it to a Kafka topic, and a consumer that reads the data from the topic and stores it in a database.

## Components

### 1. Producer (`producer.py`)

- Connects to a Kafka broker.
- Fetches real-time weather data (temperature and humidity) for Bangalore, India using the [Open-Meteo API](https://open-meteo.com/).
- Serializes the data to JSON format.
- Sends the data to the `weather` Kafka topic every 2 seconds.

### 2. Consumer (`consumer.py`)

- Subscribes to the `weather` Kafka topic.
- Deserializes incoming messages from JSON.
- Adds a timestamp to each received data point.
- Stores the weather data in a database table named `streaming_weather`.

## Prerequisites

- Python 3
- Docker and Docker Compose
- A running database supported by SQLAlchemy (e.g., PostgreSQL, MySQL, SQLite).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Start Kafka and Zookeeper:**
    Use the provided `docker-compose.yml` to start the Kafka and Zookeeper services.
    ```bash
    docker-compose up -d
    ```

3.  **Install Python dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Configure the database connection:**
    Create a `.env` file in the root of the project and add your database connection URI:
    ```
    DB_URI=postgresql://user:password@host:port/database
    ```

## How to Run

1.  **Start the consumer:**
    Open a terminal and run the consumer script. It will start listening for messages from the `weather` topic.
    ```bash
    python consumer.py
    ```

2.  **Start the producer:**
    Open another terminal and run the producer script. It will start fetching and sending live weather data.
    ```bash
    python producer.py
    ```

You should see the consumer terminal printing the received messages and storing them in the database.

## Database Schema

The consumer will create a table named `streaming_weather` with the following columns:

- `city` (TEXT)
- `temperature` (FLOAT)
- `humidity` (INTEGER)
- `time` (TIMESTAMP)

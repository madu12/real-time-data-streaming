import requests
from kafka import KafkaProducer
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka Configuration
KAFKA_TOPIC = "iss_location"
KAFKA_BROKER = "localhost:9092"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Function to fetch real-time ISS location data
def fetch_iss_location():
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")
    return None

# Stream data to Kafka
def stream_to_kafka():
    logging.info("Starting Kafka Producer...")
    try:
        while True:
            data = fetch_iss_location()
            if data:
                producer.send(KAFKA_TOPIC, value=data)
                logging.info(f"Sent to Kafka: {data}")
            else:
                logging.warning("No data fetched. Retrying in 5 seconds...")
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Kafka Producer stopped by user.")
    finally:
        producer.close()
        logging.info("Kafka Producer connection closed.")

if __name__ == "__main__":
    stream_to_kafka()

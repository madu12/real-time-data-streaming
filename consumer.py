from kafka import KafkaConsumer
import pandas as pd
import json
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka Configuration
KAFKA_TOPIC = "iss_location"
KAFKA_BROKER = "localhost:9092"

# Database Configuration
DATABASE_URI = "sqlite:///iss_location.db"  # SQLite Database for storage
engine = create_engine(DATABASE_URI)

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# Initialize DataFrame to store streaming data
data_buffer = []  # Buffer for batching inserts
BUFFER_SIZE = 10  # Insert into the database every 10 records

logging.info("Starting Kafka Consumer...")

try:
    for message in consumer:
        # Parse the message
        record = message.value
        try:
            timestamp = record["timestamp"]
            latitude = float(record["iss_position"]["latitude"])
            longitude = float(record["iss_position"]["longitude"])
            
            # Add the record to the buffer
            data_buffer.append({"timestamp": timestamp, "latitude": latitude, "longitude": longitude})
            print("\nReceived:" , record)
            
            # Display Descriptive Statistics if we have at least 2 records
            if len(data_buffer) >= 2:
                df = pd.DataFrame(data_buffer)
                stats = df[["latitude", "longitude"]].describe().to_string()
                print("\nDescriptive Statistics:\n" + stats)

            # Insert into the database when buffer is full
            if len(data_buffer) >= BUFFER_SIZE:
                df = pd.DataFrame(data_buffer)
                df.to_sql("iss_location", engine, if_exists="append", index=False)
                print(f"Saved {len(data_buffer)} records to database.")
                data_buffer.clear()  # Clear the buffer

        except KeyError as e:
            logging.error(f"Malformed message: {record}. Error: {e}")

except KeyboardInterrupt:
    logging.info("Kafka Consumer interrupted. Closing...")
    # Final buffer flush before exit
    if data_buffer:
        df = pd.DataFrame(data_buffer)
        df.to_sql("iss_location", engine, if_exists="append", index=False)
        logging.info(f"Final flush: Saved {len(data_buffer)} records to database.")
    logging.info("Kafka Consumer stopped.")

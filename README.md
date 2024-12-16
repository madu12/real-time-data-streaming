# Real-Time Data Streaming using Kafka

## Description
This project demonstrates real-time data streaming using **Apache Kafka** and Python. It fetches live data from the International Space Station (ISS) location API (`http://api.open-notify.org/iss-now.json`), streams it to a Kafka topic, processes it in real-time with a Kafka consumer, and provides descriptive statistics while saving the data to persistent storage.

---

## Project Structure
```
real-time-data-streaming/
├── producer.py         # Kafka producer script for fetching ISS data
├── consumer.py         # Consumer script for display data, stats, and storage
├── requirements.txt    # List of required Python packages
├── README.md           # Documentation for the project
├── iss_location.db     # SQLite database storing streamed data
```

---

## Installation and Setup

### Prerequisites
Ensure the following tools are installed on your system:
- **Python** (version 3.6 or higher)
- **Apache Kafka** (download from [Kafka Quickstart](https://kafka.apache.org/quickstart))
- **Java** (required for Kafka; version 8 or higher)
- **pip** (Python package installer)

---

### Step 1: Clone the Repository
Download the project:
```bash
git clone https://github.com/madu12/real-time-data-streaming.git
cd real-time-data-streaming
```

---

### Step 2: Set Up Python Environment
1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

2. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
   If you face issues with `kafka-python`, use the latest development version:
   ```bash
   pip install git+https://github.com/dpkp/kafka-python.git
   ```

---

### Step 3: Set Up Apache Kafka
1. **Download Kafka**:
   Download the latest release from the [Kafka Quickstart](https://kafka.apache.org/quickstart) page.

2. **Start ZooKeeper**:
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

3. **Start Kafka Broker**:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

4. **Create Kafka Topic**:
   ```bash
   bin/kafka-topics.sh --create --topic iss_location --bootstrap-server localhost:9092
   ```

---

## Steps to Run

### Step 1: Start the Producer
Run the Kafka producer to fetch live ISS location data and send it to the Kafka topic:
```bash
python producer.py
```

### Step 2: Start the Consumer
Run the Kafka consumer to display streaming data, calculate statistics, and save data into SQLite:
```bash
python consumer.py
```

---

## Requirements

### Python Dependencies
The following Python libraries are required (listed in `requirements.txt`):
- `kafka-python`
- `pandas`
- `sqlalchemy`
- `requests`

Install them using:
```bash
pip install -r requirements.txt
```

---

## Example Outputs

### Producer:
- On successful data fetch:
  ```
  2024-12-16 14:00:00 - INFO - Sent to Kafka: {'timestamp': '1689312312', 'iss_position': {'latitude': '12.3456', 'longitude': '-45.6789'}, 'message': 'success'}
  ```
- On API failure:
  ```
  2024-12-16 14:00:05 - WARNING - Failed to fetch data. HTTP Status Code: 500
  ```
- When stopped with `Ctrl+C`:
  ```
  2024-12-16 14:05:00 - INFO - Kafka Producer stopped by user.
  ```

### Consumer with Statistics and Storage:
```
Received: {'timestamp': '1689312312', 'iss_position': {'latitude': '12.3456', 'longitude': '-45.6789'}}
Descriptive Statistics:
       latitude  longitude
count   2.00000 -45.676150
mean   12.34675 -45.676150
std     0.00234   0.003889
min    12.34560 -45.678900
max    12.34890 -45.673400
Saved to database: [{'timestamp': '1689312312', 'latitude': 12.3456, 'longitude': -45.6789}]
```

---

## Notes
- The producer fetches new data every 5 seconds. You can adjust this interval in the `producer.py` script.
- Make sure Kafka services (ZooKeeper and Kafka broker) are running before starting the producer or consumer.

---

## License
This project is open-source and free to use for educational purposes.

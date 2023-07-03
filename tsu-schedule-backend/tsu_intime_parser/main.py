import json
import time
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.errors import KafkaError, NoBrokersAvailable

def consume_from_topic(consumer, topic):
    consumer.subscribe(topic)
    for message in consumer:
        # Process the consumed message here
        data = json.loads(message.value.decode('utf-8'))

        schedule = parse_schedule(data)

        request_id = data['request_id']
        forward_to_topic(schedule, request_id)

        save_to_db(data['token'], schedule)

def parse_schedule(data):
    print(f"Parsing group = {data['groupNumber']} and faculty =  {data['faculty']}.")
    with open("schedule.json", 'r', encoding="utf-8") as file:
        schedule = json.load(file)
        return schedule

def forward_to_topic(schedule, request_id):
    data = {
        'schedule': schedule,
        'request_id': request_id
    }
    print(data)
    producer.send('parser-to-parser-topic', value=json.dumps(data).encode('utf-8'))
    producer.flush()

def save_to_db(token, schedule):
    pass

if __name__ == '__main__':
    print("Starting tsu-intime-parser...")
    # Kafka consumer configuration
    consumer_config = {
        'bootstrap_servers': 'kafka:9092',
        'group_id': 'test-consumer-group',
        'auto_offset_reset': 'earliest'
    }

    # Kafka producer configuration
    producer_config = {
        'bootstrap_servers': 'kafka:9092'
    }

    while True:
        try:
            # Create Kafka producer instance
            producer = KafkaProducer(**producer_config)
            break  # Break out of the loop if the producer is successfully created
        except NoBrokersAvailable:
            print("No brokers available. Retrying in 3 seconds...")
            time.sleep(3)

    # Create Kafka consumer instance
    consumer = KafkaConsumer(**consumer_config)

    # Define the topic to consume from
    topic = 'controller-parser-topic'

    while True:
        try:
            # Check if the topic exists
            partitions = consumer.partitions_for_topic(topic)
            if partitions is not None:
                print(f"'{topic} is available'. Subscribing...")
                # Consume messages from the topic
                consume_from_topic(consumer, [topic])
            else:
                print(f"Topic '{topic}' does not exist. Retrying in 1 second...")
                # Add a delay of 1 second before retrying
                time.sleep(3)
        except KafkaError as e:
            print(f"An error occurred: {e}. Retrying in 1 second...")
            consumer.close()
            time.sleep(1)

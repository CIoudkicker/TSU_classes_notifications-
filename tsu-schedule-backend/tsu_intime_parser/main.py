import json
from kafka import KafkaConsumer, KafkaProducer

def consume_from_topic(consumer, topic):
    consumer.subscribe(topic)
    for message in consumer:
        # Process the consumed message here
        data = json.loads(message.value.decode('utf-8'))
        schedule = parse_schedule(data)
        forward_to_topic(schedule)

def parse_schedule(data):
    print(f"Parsing group = {data['groupNumber']} and faculty =  {data['faculty']}.")
    with open("file.json", 'r', encoding="utf-8") as file:
        schedule = json.load(file)
        return schedule

def forward_to_topic(schedule):
    producer.send('parser-to-parser-topic', value=json.dumps(schedule).encode('utf-8'))
    producer.flush()


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

    # Create Kafka consumer and producer instances
    consumer = KafkaConsumer(**consumer_config)
    producer = KafkaProducer(**producer_config)

    consume_from_topic(consumer, ['controller-parser-topic'])

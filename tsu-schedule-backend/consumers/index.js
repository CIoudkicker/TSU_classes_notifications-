const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['localhost:29092']
});

// Create a consumer instance
const consumer = kafka.consumer({ groupId: 'my-consumer-group' });

// Connect to the Kafka cluster
const run = async () => {
  await consumer.connect();

  // Subscribe to the topic(s) you want to consume from
  await consumer.subscribe({ topic: 'my-topic', fromBeginning: true });

  // Start consuming messages
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log(`Received message: ${message.value.toString()} from topic ${topic}`);
      // Process the message as needed
    },
  });
};

run().catch(console.error);
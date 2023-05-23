const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['localhost:29092']
});

const producer = kafka.producer();

const produceMessage = async () => {
  try {
    await producer.connect();

    const message = {
      key: 'my-key',
      value: 'Hello!'
    };

    await producer.send({
      topic: 'my-topic',
      messages: [message]
    });

    console.log('Message sent successfully');
  } catch (error) {
    console.error('Error producing message:', error);
  } finally {
    await producer.disconnect();
  }
};

produceMessage();
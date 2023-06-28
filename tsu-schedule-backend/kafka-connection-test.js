const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['localhost:29092'], // 指定Kafka集群的地址和端口
});

async function runProducer() {
  const producer = kafka.producer();
  await producer.connect();
  
  const topic = 'my-topic';
  const message = 'This is a test message';

  await producer.send({
    topic,
    messages: [{ value: message }],
  });

  console.log('消息发送成功。Message sent successfully.');

  await producer.disconnect();
}

runProducer().catch((error) => {
  console.error('发送消息时出错。Error while sending message:', error);
  process.exit(1);
});

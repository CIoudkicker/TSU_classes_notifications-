const { Kafka } = require('kafkajs');

const kafkaBrokers = ['localhost:29092']; 
const kafkaTopic = 'my-topic'; 

async function runProducer() {
  const producer = new Kafka({
    brokers: kafkaBrokers,
  }).producer();

  await producer.connect();

  const messages1 = [
    { value: 'Message 1' },
    { value: 'Message 2' },
    { value: 'Message 3' },
    { value: 'Message 4' },
    { value: 'Message 5' },
  ];

  const messages2 = [
    { value: 'Message 6' },
    { value: 'Message 7' },
    { value: 'Message 8' },
    { value: 'Message 9' },
    { value: 'Message 10' },
  ];

  await producer.send({
    topic: kafkaTopic,
    messages: messages1,
  });

  console.log('第一批消息发送成功。First batch of messages sent successfully.');

  // 等待10秒wait 10 seconds
  await delay(10000);

  await producer.send({
    topic: kafkaTopic,
    messages: messages2,
  });

  console.log('第二批消息发送成功。Second batch of messages sent successfully.');

  await producer.disconnect();
}

// 延时函数delay function
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

runProducer().catch((error) => {
  console.error('发送消息时出错。Error while sending message:', error);
  process.exit(1);
});

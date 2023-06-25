// 导入所需的库
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['localhost:29092'], // 指定Kafka集群的地址和端口
});

// 设置消费者组和主题
const consumer = kafka.consumer({ groupId: 'my-consumer-group' });
const topic = 'my-topic';

// 建立连接并发送/接收消息
async function run() {
  // 连接到Kafka集群
  await consumer.connect();
  await consumer.subscribe({ topic });

  // 发送测试消息
  const producer = kafka.producer();
  await producer.connect();
  await producer.send({
    topic,
    messages: [{ value: 'This is a test message' }],
  });

  // 接收并验证消息
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      // 验证接收到的消息内容是否与发送的消息内容一致
      const receivedMessage = message.value.toString();
      const expectedMessage = 'This is a test message';
      if (receivedMessage === expectedMessage) {
        console.log('接收到的消息与发送的消息内容一致。测试通过！The received message is consistent with the content of the sent message. Test passed!');
      } else {
        console.log('接收到的消息与发送的消息内容不一致。测试不通过！The received message does not match the content of the sent message. Test failed!');
      }
    },
  });
}

// 运行测试
run().catch((error) => {
  console.error('测试失败Test failed:', error);
  process.exit(1);
});

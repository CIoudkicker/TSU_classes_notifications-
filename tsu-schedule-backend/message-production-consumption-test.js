// 引入所需的Kafka客户端库
const { Kafka } = require('kafkajs');

// Kafka集群的连接参数
const kafkaBrokers = ['localhost:29092']; // 替换为您的Kafka集群地址
const kafkaTopic = 'my-topic'; // 替换为您的Kafka主题

// 创建生产者
const producer = new Kafka({
  brokers: kafkaBrokers
}).producer();

// 创建消费者
const consumer = new Kafka({
  brokers: kafkaBrokers
}).consumer({ groupId: 'my-consumer-group' });

// 发送消息函数
async function sendMessages() {
  await producer.connect();
  await producer.send({
    topic: kafkaTopic,
    messages: [
      { value: 'Message 1' },
      { value: 'Message 2' },
      { value: 'Message 3' }
    ]
  });
  await producer.disconnect();
}

// 接收并验证消息函数
async function receiveMessages(sentMessages) {
  let receivedMessages = []; // 清空已接收的消息数组

  await consumer.connect();
  await consumer.subscribe({ topic: kafkaTopic, fromBeginning: true });

  await new Promise((resolve, reject) => {
    consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        receivedMessages.push(message.value.toString());

        console.log(`Received message: ${message.value}`);

        if (receivedMessages.length === sentMessages.length) {
          consumer.stop(); // 停止消费者
          resolve(); // 所有消息已经处理完毕，解析 Promise
        }
      },
      eachBatchAutoResolve: false // 禁用自动提交偏移量
    }).catch(reject); // 捕捉异常情况
  });

  return receivedMessages;
}

// 测试函数
async function runTest() {
  // 确保在发送消息之前，消费者已被正确关闭，以便在接收消息时重新创建并订阅主题
  await consumer.disconnect();

  console.log('Starting Kafka test...');
  console.log('Sending messages...');
  await sendMessages();
  console.log('Messages sent.');
  console.log('Receiving messages...');
  const sentMessages = ['Message 1', 'Message 2', 'Message 3'];
  
  const receivedMessages = await receiveMessages(sentMessages);
  console.log(receivedMessages);
  console.log('Messages received and verified.');

  // 验证消息的一致性
  
  let testPassed = true;

  for (let i = 0; i < sentMessages.length; i++) {
    if (sentMessages[i] !== receivedMessages[i]) {
      // 如果发送的消息与接收的消息不一致，则测试失败
      testPassed = false;
      break;
    }
  }

  // 根据测试结果输出相应的消息
  if (testPassed) {
    console.log('测试通过Test passed!');
  } else {
    console.log('测试失败Test failed!');
  }
}

// 执行测试
runTest().catch((error) => {
  console.error('Test failed:', error);
});

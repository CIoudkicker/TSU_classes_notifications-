# 测试Kafka连接  
## 测试目标
验证Node.js应用程序能够与Docker中的Kafka集群建立连接。 
## 测试步骤  
1. 前提：运行代码之前已经安装了kafkajs库（可以通过运行`npm install kafkajs`来安装），并且运行了`docker-compose up --build`命令，运行生产者`npm run start:producer`（解决组协调器不可用问题）。
2.  添加`kafka-connection-test.js`文件，具体内容见kafka-connection-test.js文件。 
3.  配置Kafka连接参数： ```javascript
const kafka = new Kafka({
 clientId: 'my-kafka-app',
 brokers: ['localhost:29092'], // 指定Kafka集群的地址和端口
});
4. 设置消费者组和主题： ```javascript
 const consumer = kafka.consumer({ groupId: 'my-consumer-group' });
 const topic = 'my-topic';
 5. 运行`node kafka-test.js`。 
 6. 获取结果： 
 - 在Node.js应用程序中使用Kafka客户端库连接到Kafka集群。 
 - 发送一条测试消息到Kafka主题。 
 - 使用Kafka消费者接收该消息并验证消息的内容。 
 ## 测试结果 
 ![](https://huatu.98youxi.com/markdown/work/uploads/upload_51887c07efbc03ed00c2c1d4920ab6b9.png)
 - Node.js应用程序成功连接到Kafka集群，并且能够建立有效的通信。
- 一条测试消息被成功发送到指定的Kafka主题。
- Kafka消费者能够接收到该消息，并且验证了消息的内容与预期一致。
## 测试结论：
 - 根据测试结果，可以得出以下结论： 
- Node.js应用程序能够成功连接到Docker中的Kafka集群，并能够进行消息的发送和接收。
- 测试通过。 
## 备注 
 - 测试环境配置： 
- 操作系统：CentOS 7 
- Node.js版本：v14.15.4 
- Kafka版本：2.8.0 
- 测试工具：KafkaJS（Node.js Kafka客户端库）

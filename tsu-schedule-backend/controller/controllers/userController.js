const ApiError = require('../errors/ApiError');
const jwt = require('jsonwebtoken')
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['kafka:9092']
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'my-group' });

const generateJwt = (id, email) => {
  return jwt.sign({ id, email }, process.env.JWT_KEY, { expiresIn: '24h' })/* экспайрс ин, это срок годности токена, чтобы если токен украли, он устарел за этот срок*/
}

const consumeMessage = async (topic_sub) => {
  try {
    await consumer.connect();
    await consumer.subscribe({ topic: topic_sub, fromBeginning: true });
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        console.log(`Received message: ${message.value.toString()} from topic ${topic}`);
        // Process the message as needed
        return message;
      },
    });

  } catch (error) {
    console.error('Error consuming message:', error);
  } finally {
    await consumer.disconnect();
  }
};

const produceMessage = async (data) => {
  try {
    await producer.connect();

    const message = {
      key: "data",
      value: JSON.stringify(data)
    };

    await producer.send({
      topic: 'controller-parser-topic',
      messages: [message]
    });

    console.log('Message sent successfully');
  } catch (error) {
    console.error('Error producing message:', error);
  } finally {
    await producer.disconnect();
  }
};


class UserController {

  async login(req, res, next) {
    const { email, password } = req.body
    if (!email || !password ) return next(ApiError.internal('вы не ввели данные'))

    // look up in db for user_id, but we don't, cause not to complicate things
    const id = Math.floor(Math.random() * 1000000); 

    const token = generateJwt(id, email);

    // Send the token in the response
    return res.json({ token });
  }


  async getSchedule(req, res, next) {
    const groupNumber = "932209"
    const faculty = "Институт прикладной математики и компьютерных наук"

    await produceMessage({ groupNumber, faculty })

    return await consumeMessage("controller-parser-topic");
  }

  
 async getSchedulestat(req, res, next) {
    const groupNumber = "932209"
    const faculty = "Институт прикладной математики и компьютерных наук"
     try {
   const jsonData = fs.readFileSync("../../tsu_intime_parser/file.json", 'utf-8');
   const json = JSON.parse(jsonData);
    res.json(json);
   } catch (error) {
    console.error('Ошибка при чтении JSON файла:', error);
    res.status(500).send('Ошибка при чтении JSON файла.');
  }
  });

  





}
module.exports = new UserController()

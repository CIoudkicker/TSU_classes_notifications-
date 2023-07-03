const ApiError = require('../errors/ApiError');
const jwt = require('jsonwebtoken')
const { Kafka } = require('kafkajs');
const fs = require('fs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['kafka:9092']
});

const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: 'my-group' });

const generateJwt = (id, email) => {
  return jwt.sign({ id, email }, process.env.JWT_KEY, { expiresIn: '24h' })/* экспайрс ин, это срок годности токена, чтобы если токен украли, он устарел за этот срок*/
}

const consumeMessage = async (topic_sub, request_id) => {
  try {
    await consumer.connect();
    await consumer.subscribe({ topic: topic_sub, fromBeginning: true });

    return new Promise((resolve, reject) => {
      consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
          const receivedMessage = message.value.toString();
          const parsedMessage = JSON.parse(receivedMessage);

          if (parsedMessage.request_id === request_id) {
            console.log(`Received message: ${receivedMessage} from topic ${topic}`);
            const schedule = parsedMessage.schedule;
            resolve(schedule);
            consumer.disconnect();
          }
        },
      }).catch((error) => {
        reject(error);
      });
    });
  } catch (error) {
    console.error('Error consuming message:', error);
    throw error;
  }
};


const produceMessage = async (data, request_id, token)  => {
  try {
    await producer.connect();

    const message = {
      key: "data",
      value: JSON.stringify({...data, request_id, token})
    };

    await producer.send({
      topic: 'controller-parser-topic',
      messages: [message]
    });

    console.log(`Message sent ${JSON.stringify({...data, request_id, token})} successfully`);
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
    const request_id = Math.random().toString(36).substring(7);
    
    try {
      console.log(req.headers.authorization)
      const token = req.headers.authorization.split(' ')[1];

      await produceMessage({ groupNumber, faculty }, request_id, token)

      const schedule_json = await consumeMessage("parser-controller-topic", request_id);
      
      return res.json({ schedule: schedule_json });
    } catch (error) {
      console.error('Error:', error);
      return res.status(500).send('An error occurred.');
    }
  }
}
  

module.exports = new UserController()

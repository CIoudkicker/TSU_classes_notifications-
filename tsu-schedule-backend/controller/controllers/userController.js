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
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const receivedMessage = message.value.toString();
        const parsedMessage = JSON.parse(receivedMessage);

        if (parsedMessage.request_id === request_id) {
          console.log(`Received message: ${receivedMessage} from topic ${topic}`);
          // Process the message
        }
      },
    });

  } catch (error) {
    console.error('Error consuming message:', error);
  } finally {
    await consumer.disconnect();
  }
};

const produceMessage = async (data, request_id)  => {
  try {
    await producer.connect();

    const message = {
      key: "data",
      value: JSON.stringify({...data, request_id})
    };

    await producer.send({
      topic: 'controller-parser-topic',
      messages: [message]
    });

    console.log(`Message sent ${JSON.stringify({...data, request_id})} successfully`);
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

    await produceMessage({ groupNumber, faculty }, request_id)

    return await consumeMessage("controller-parser-topic", request_id);
  }

  
 async getSchedulestat(req, res, next) {
    const groupNumber = "932209"
    const faculty = "Институт прикладной математики и компьютерных наук"
     try {
   const jsonData = fs.readFileSync("E:/Magistratura/Sem2/APS/Lab4/TSU_classes_notifications-/tsu-schedule-backend/tsu_intime_parser/file.json", 'utf-8');
   const json = JSON.parse(jsonData);
    res.json(json);
   } catch (error) {
    console.error('Ошибка при чтении JSON файла:', error);
    res.status(500).send('Ошибка при чтении JSON файла.');
  }
  };



   async getalarmestat(req, res, next) {
    const groupNumber = "932209"
    const faculty = "Институт прикладной математики и компьютерных наук"

    try {
      await produceMessage({ groupNumber, faculty })
      const json = await consumeMessage("controller-parser-topic");

      const now = moment();
      const currentDay = now.format('dddd'); // Текущий день недели
      const currentTime = now.format('HH:mm'); // Текущее время

      const currentDaySchedule = json.find(day => day.day === currentDay);

      if (!currentDaySchedule) {
        return res.json({ message: "Сегодня пар нет" });
      }

      const nextLesson = currentDaySchedule.lessons.find(lesson => lesson.startTime >= currentTime);

      if (!nextLesson) {
        return res.json({ message: "На сегодня пары уже закончились" });
      }

      if (moment(nextLesson.startTime, 'HH:mm').diff(now, 'minutes') <= 5) {
        return res.json({ message: "Пара начинается через 5 минут!", lesson: nextLesson, lessonLink: nextLesson.lessonLink });
      } else {
        return res.json({ message: "Следующая пара нескоро", nextLesson, lessonLink: nextLesson.lessonLink });
      }
    } catch (error) {
      console.error('Error:', error);
      return res.status(500).send('An error occurred.');
    }
  }




  
}
  

module.exports = new UserController()

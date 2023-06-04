const { use } = require("express/lib/application");
const ApiError = require('../errors/ApiError');
const bcrypt = require('bcrypt')
const jwt = require('jsonwebtoken')
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'my-kafka-app',
  brokers: ['localhost:29092']
});

const producer = kafka.producer();
const consumer = kafka.consumer();
//const {User, Class}= require ('../models/model')
const generateJwt=(id,email,role)=>{
    return jwt.sign({id , email, role},process.env.jwt_key,{expiresIn: '24h'})/* экспайрс ин, это срок годности токена, чтобы если токен украли, он устарел за этот срок*/

}
const consumeMessage = async (topic_sub) => {
  try { await consumer.connect();
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

const produceMessage = async (credentials) => {
    try {
      await producer.connect();
  
      const message = {
        key: "credentials",
        value: JSON.stringify(credentials)
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


class UserController {
   




    /*async registration(req,res,next) 
    {const {login, password, role,name,lname,mname,comm }= req.body
        if(!login||!password){
            return next(ApiError.badrequest('некорректный логин или пароль'))
        }
        const candidate = await User.findOne({where:{login}})
        if(candidate){
            return next(ApiError.badrequest('такой логин уже существует'))
        }
        const hashPassword = await bcrypt.hash(password,8)
        const user = await User.create({login, role, password:hashPassword,name,lname,mname,comm })
        
        const token= generateJwt(user.id,user.login,user.role)


        return res.json({token})
    }*/
    
    async login_pseudo(req, res, next) 
    {
      const { login, password } = req.body
      if (!login || !password) return next(ApiError.internal('вы не ввели данные'))

      await produceMessage({ login, password })
      


      return await consumeMessage("my-topic")
  }

  
    async login(req, res, next) {
        const { login, password } = req.body
        if (!login || !password) return next(ApiError.internal('вы не ввели данные'))
        

        await produceMessage({ login, password })
 

        return await consumeMessage("my-topic")
    }

    



}
module.exports= new UserController()
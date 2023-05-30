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

//const {User, Class}= require ('../models/model')
const generateJwt=(id,email,role)=>{
    return jwt.sign({id , email, role},process.env.jwt_key,{expiresIn: '24h'})/* экспайрс ин, это срок годности токена, чтобы если токен украли, он устарел за этот срок*/

}

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
   




    async registration(req,res,next) 
    {const {email, password, role,name,lname,mname,comm }= req.body
        if(!email||!password){
            return next(ApiError.badrequest('некорректный логин или пароль'))
        }
        const candidate = await User.findOne({where:{email}})
        if(candidate){
            return next(ApiError.badrequest('такой логин уже существует'))
        }
        const hashPassword = await bcrypt.hash(password,8)
        const user = await User.create({email, role, password:hashPassword,name,lname,mname,comm })
        
        const token= generateJwt(user.id,user.email,user.role)


        return res.json({token})
    }

    async login(req, res, next) {
        const { email, password } = req.body
        if (!email && !password) return next(ApiError.internal('вы не ввели данные'))
        // const user = await User.findOne({ where: { email } })
        // if (!user) {
        //     return next(ApiError.internal('пользователь не найден. Возможно, вы ввели неправильные данные '))
        // }
        // let comparePassword = bcrypt.compareSync(password, user.password)
        // if (!comparePassword) {
        //     return next(ApiError.internal('указан неверный пароль'))
        // }
        // const token = generateJwt(user.id, user.email, user.role)

        produceMessage({ email, password })

        return res.json()
    }

    



}
module.exports= new UserController()
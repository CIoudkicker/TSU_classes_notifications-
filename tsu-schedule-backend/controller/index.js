require('dotenv').config()
const express = require("express");


const PORT = process.env.PORT || 5500;

const app = express();
const cors = require('cors');


const router = require("./routers/userRouter");
const errorHandler = require('./middleware/ErrorHandlingMiddleware')

app.use(cors())
app.use(express.json())

app.use('/api', router) //работает на адресе апи, что очевидно, судя по всему можно добавить дополнительные адреса и повстраивать своих штучек

app.use(errorHandler) //Обработка ошибок, должен идти строго последним

app.get('/', (req, res) => {
    res.status(200).json({ message: 'соединение успешно' }) //код 200 значит что все отработало как надо если чо
    console.log("кто то зашел в /арi")
})

const start = async () => {
    try {
        app.listen(PORT, () => console.log("server start on port ", + PORT));
    }
    catch (e) {
        console.log(e)
    }
 }


start() 
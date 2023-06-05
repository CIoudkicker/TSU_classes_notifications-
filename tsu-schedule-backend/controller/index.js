// const sequelize = require('./db')
// const models = require('./models/model')// потом надо будет поменять на маврмодель!!!!!!!!!!!!!!!!!!!!!!!
//const XLSX = require("xlsx")
// const fileUpload = require('express-fileupload')

require('dotenv').config()
const express = require("express");


const PORT = process.env.PORT || 5500;

const app = express();
const cors = require('cors');


const router = require("./routers/userRouter");
const errorHandler = require('./middleware/ErrorHandlingMiddleware')

app.use(cors())
app.use(express.json())

// app.use(express.static(path.resolve(__dirname, 'static')))
//app.use(XLSX())
// app.use(fileUpload( {}))

app.use('/api', router) //работает на адресе апи, что очевидно, судя по всему можно добавить дополнительные адреса и повстраивать своих штучек

app.use(errorHandler) //Обработка ошибок, должен идти строго последним

app.get('/', (req, res) => {
    res.status(200).json({ message: 'соединение успешно' }) //код 200 значит что все отработало как надо если чо
    console.log("кто то зашел в /арi")
})

const start = async () => {
    try {
        // await sequelize.authenticate()
        // await sequelize.sync({ force: true })

        //await sequelize.sync({ alter: true })
        // await sequelize.sync()
        app.listen(PORT, () => console.log("server start on port ", + PORT));
    }
    catch (e) {
        console.log(e)
    }
 }


start() 
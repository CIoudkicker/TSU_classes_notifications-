const Router = require ('express')
const userController = require('../controllers/userController')
const router = new Router()

const authMiddleware = require('../middleware/authMiddleware')

//router.post('/registration',userController.registration)
router.post('/login', userController.login)
router.get('/getSchedule', authMiddleware ,userController.getSchedule)
router.get('/getSchedulestat', authMiddleware ,userController.getSchedulestat)
router.get('/getalarmestat', authMiddleware ,userController.getalarmestat)
module.exports = router
